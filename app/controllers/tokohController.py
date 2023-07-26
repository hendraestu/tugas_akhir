from flask import request, jsonify, redirect, flash, send_file
from flask.templating import render_template
from app import app
from app.models.dataTokohModel import db, Tokoh
from app.models.riwayatModel import db, Riwayat
from flask_marshmallow import Marshmallow
import re, config

ma = Marshmallow(app)

class RiwayatSchema(ma.Schema):
    class Meta:
        fielfs = ('id', 'id_nama', 'nama', 'positif', 'negatif', 'netral', 'update_at')

riwayat_schema = RiwayatSchema()
riwayats_schema = RiwayatSchema(many=True)

class TokohSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama', 'positif', 'negatif', 'netral', 'akurasi', 'image', 'update_at')

tokoh_schema = TokohSchema()
tokohs_schema = TokohSchema(many=True)

DATA_PATH = config.DATA_PATH

def getAllTokoh():
    konten = Tokoh.query.all()
    tokos= tokohs_schema.dump(konten)
    images = Tokoh.query.all()
    imagess= tokohs_schema.dump(images)
    return render_template('index.html', data = tokos,image = imagess)
    
def getDetailTokoh(id):
    id_nama = id
    konten = Tokoh.query.get(id)
    kontens = tokoh_schema.dump(konten)
    riwayat = Riwayat.query.filter_by(id_nama=id_nama).all()
    riwayats= riwayat_schema.dump(riwayat)
    print(id_nama)
    print(riwayat)
    return render_template("tokohAdmin.html", data= kontens, data2 = riwayat)
    # con = tokohs_schema.dump(konten)
    # return jsonify (con)


def updateTokoh(id):
    tokoh = Tokoh.query.get(id)
    nama = request.form['nama']
    nama = request.form['nama']
    positif = request.form['positif']
    negatif = request.form['negatif']
    netral = request.form['netral']
    akurasi = request.form['akurasi']

    tokoh.nama = nama
    tokoh.positif = positif
    tokoh.negatif = negatif
    tokoh.netral = netral
    tokoh.akurasi = akurasi

    db.session.commit()
    tokohUpdate = tokoh_schema.dump(tokoh)
    return jsonify({"msg": "Success update tokoh", "status": 200, "data": tokohUpdate})

def getAllTokohUser():
    konten = Tokoh.query.all()
    tokos= tokohs_schema.dump(konten)
    images = Tokoh.query.all()
    imagess= tokohs_schema.dump(images)
    # print(tokos)
    return render_template('users.html', data = tokos,image = imagess)
    
def getDetailTokohUser(id):
    id_nama = id
    konten = Tokoh.query.get(id)
    kontens = tokoh_schema.dump(konten)
    riwayat = Riwayat.query.filter_by(id_nama=id_nama).all()
    riwayats= riwayat_schema.dump(riwayat)
    print(id_nama)
    print(riwayat)
    return render_template("tokohUser.html", data= kontens, data2 = riwayat)

def deleteTokoh(id):
    tokoh = Tokoh.query.get(id)
    db.session.delete(tokoh)
    db.session.commit()
    flash('Tokoh Berhasil Dihapus!')
    # tokohDelete = tokohs_schema.dump(tokoh)
    return redirect ('/updateData')

def getAllTokohUser1():
    konten = Tokoh.query.all()
    tokos= tokohs_schema.dump(konten)
    images = Tokoh.query.all()
    imagess= tokohs_schema.dump(images)
    return render_template('percobaan.html', data = tokos,image = imagess)

def download_file():
    nama = request.form['nama']
    nama1 = re.sub(' ', '-', nama)
    # Tentukan path file yang ingin diunduh (pastikan path sesuai dengan file di server)
    file_path = DATA_PATH + nama1+'.csv'
    print(file_path)
    return send_file(file_path, as_attachment=True)