from flask import Blueprint, render_template, url_for

bp = Blueprint('api', __name__)

from app.api import tokens, errors, auth, users, obats, pelanggan, jual, absen, search
