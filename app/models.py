import datetime
import base64
import os
from enum import unique
from flask import url_for
from flask_login import UserMixin
from bcrypt import checkpw, hashpw, gensalt
import peewee as pw
from playhouse.flask_utils import FlaskDB, PaginatedQuery

db = FlaskDB()

'''
macbook air: 11 Ags 2022
==> opensearch
Data:    /opt/homebrew/var/lib/opensearch/
Logs:    /opt/homebrew/var/log/opensearch/opensearch_homebrew.log
Plugins: /opt/homebrew/var/opensearch/plugins/
Config:  /opt/homebrew/etc/opensearch/

To restart opensearch after an upgrade:
  brew services restart opensearch
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/opensearch/bin/opensearch
'''

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': query.count(),
                'total_items': query.count()
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs),
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs)
            }
        }
        return data
    
class Note(db.Model):
    object_type = pw.CharField()
    object_id = pw.IntegerField()
    note = pw.TextField()
    username = pw.CharField(max_length=35)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    
class Obat(PaginatedAPIMixin, db.Model):
    nama = pw.CharField(max_length=60)
    satuan = pw.CharField(null=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'nama': self.nama,
            'satuan': self.satuan,
            '_links': {
                'self': url_for('api.get_obat', id=self.id)
            }
        }
        return data

class MutasiObat(db.Model):
    obat = pw.ForeignKeyField(Obat)    
    object_type = pw.CharField()
    object_id = pw.IntegerField()
    
class Pelanggan(PaginatedAPIMixin, db.Model):
    kode = pw.CharField(max_length=10, null=True)
    nama = pw.CharField(max_length=50)
    alamat = pw.CharField(max_length=255, null=True)
    telp = pw.CharField(max_length=35, null=True)
    kota = pw.CharField(max_length=35, null=True)
    badan_usaha = pw.CharField(max_length=20, null=True)
    jatuh_tempo = pw.IntegerField(default=30) # hari, batas bayar
    plafon = pw.IntegerField(null=True) # ribuan, Batas maksimum stok
    sia = pw.CharField(max_length=35, null=True) # Surat Ijin Apotik
    sia_sd = pw.DateField(null=True) # SIA berlaku sampai dengan
    npwp = pw.CharField(max_length=30, null=True)
    pkp = pw.CharField(max_length=50, null=True)
    nama_pajak = pw.CharField(max_length=50, null=True)
    alamat_pajak = pw.CharField(max_length=100, null=True)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'kode': self.kode,
            'nama': self.nama,
            'alamat': self.alamat,
            'badan_usaha': self.badan_usaha,
            'jatuh_tempo': self.jatuh_tempo,
            'plafon': self.plafon,
            'kota': self.kota,
            '_links': {
                'self': url_for('api.get_pelanggan', id=self.id)
            }
        }
        return data

class Jual(db.Model):
    pelanggan = pw.ForeignKeyField(Pelanggan)
    tanggal = pw.DateField()
    sales = pw.CharField(null=True) # username
    jatuh_tempo = pw.DateField()
    diskon = pw.IntegerField(default=0)
    status = pw.IntegerField(default=0) # 0: pesanan, 1: tagihan, 8: Batal, 9: lunas/Close
    
class ItemJual(db.Model):
    pesananin = pw.ForeignKeyField(Jual)
    obat = pw.CharField()
    banyak = pw.IntegerField()
    harga = pw.IntegerField()
    diskon = pw.IntegerField(default=0)
    batch_no = pw.CharField(null=True)
    
class User(UserMixin, db.Model):
    username = pw.CharField(unique=True, max_length=12)
    password = pw.CharField(max_length=255)
    role = pw.IntegerField(default=1) # 0 super, 1 sales, 2 gudang, 3 keuangan
    is_active = pw.BooleanField(default=True)
    hp = pw.CharField(max_length=20, null=True)
    tz = pw.CharField(max_length=35, default='Asia/Jakarta')
    last_login = pw.DateTimeField(null=True)
    last_seen = pw.DateTimeField(null=True)
    token = pw.CharField(max_length=32, null=True)
    token_expiration = pw.DateTimeField(null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    
    class Meta:
        table_name = 'users'
    
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen and self.last_seen.isoformat() or None,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def check_password(self, password):
        return checkpw(password.encode(), self.password.encode())
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt())
        
    def get_token(self, expires_in=3600):
        now = datetime.datetime.utcnow()
        if self.token and self.token_expiration > now + datetime.timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + datetime.timedelta(seconds=expires_in)
        self.save()
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.datetime.now() - datetime.timedelta(seconds=1)
        
    @staticmethod
    def check_token(token):
        try:
            user = User.get(User.token==token)
            if user.token_expiration < datetime.datetime.utcnow():
                return user
        except User.DoesNotExist:
            pass
        return None

