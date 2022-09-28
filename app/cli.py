import datetime
import random
import click

from app.models import Pelanggan, Obat, Jual, ItemJual, User

MAX_P = 198
MAX_O = 1208

def register(app):
    @app.cli.command('list-user')
    def list_user():
        users = User.select().order_by(User.username)
        click.echo('User ({})'.format(users.count()))
        for u in users:
            click.echo('{} {} {}'.format(u.id, u.username, u.role))
        
    @app.cli.command('list-jual')
    def list_jual():
        juals = Jual.select().order_by(Jual.tanggal.desc())
        click.echo('Penjualan: {}\n'.format(juals.count()))
        for jual in juals:
            click.echo(' {} {}\t{}'.format(jual.tanggal, jual.pelanggan.nama[:11], jual.itemjual_set.count()))
        click.echo('Sebanyak: {}'.format(juals.count()))
        
    @app.cli.command('create-sample')
    def create_sample():
        for i in range(100):
            plg = Pelanggan.get(random.randrange(1, MAX_P))
            s = '{} {}'.format(i, plg.nama)
            click.echo(s)
            num = random.randrange(1, 6)
            s = '  Num order: {}'.format(num)
            click.echo(s)
            jam = random.randrange(8, 17)
            bulan = random.randrange(1, 13)
            tanggal = datetime.datetime(2022, bulan, random.randrange(1,28), jam)
            jtempo = tanggal + datetime.timedelta(days=35)
            jual = Jual.create(pelanggan=plg, tanggal=tanggal, jatuh_tempo=jtempo)
            for j in range(num):
                obat = Obat.get(random.randrange(1, MAX_O))
                s = '  {} {}'.format(j+1, obat.nama)
                click.echo(s)
                item = ItemJual.create(pesananin=jual, obat=obat.nama + ' | ' + obat.satuan, 
                                       banyak=random.randrange(1, 10), harga=100)