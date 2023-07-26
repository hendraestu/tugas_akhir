from datetime import datetime
from app import db

class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_nama = db.Column(db.String(100))
    nama = db.Column(db.String(100))
    positif = db.Column(db.String(100))
    negatif = db.Column(db.String(100))
    netral = db.Column(db.String(100))
    update_at = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __init__(self, id_nama, nama, positif, negatif, netral):
        self.nama = nama
        self.id_nama = id_nama
        self.positif = positif
        self.negatif = negatif
        self.netral = netral