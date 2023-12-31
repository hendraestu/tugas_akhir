from app import app
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import request, jsonify, redirect, flash
from flask.templating import render_template
import cloudinary.uploader
import os, csv, re, config, pickle
from werkzeug.utils import secure_filename
from app.models.dataTokohModel import db, Tokoh
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class TokohSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama', 'positif', 'negatif', 'netral', 'akurasi', 'image', 'update_at')

tokoh_schema = TokohSchema()
tokohs_schema = TokohSchema(many=True)

DATASET_PATH = config.DATASET_PATH
MODEL_PATH = config.MODELS_PATH

ALLOWED_EXTENSIONS = set(['csv', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createModel():

    files = request.files['files']
    nama = request.form['nama']

    if 'image' not in request.files:
        resp = jsonify({"msg": "No body files attached in request"})
        resp.status_code = 501
        return resp
    image = request.files['image']
    print(image.filename)
    if image.filename == '':
        resp = jsonify({'msg': "No file image selected"})
        resp.status_code = 505
        return resp

    if image and allowed_file(image.filename):
        # filename = secure_filename(image.filename)
        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_result = cloudinary.uploader.upload(image)
        urlImage = upload_result["secure_url"]
        print(upload_result["secure_url"])
        success = True
    else:
        error[image.filename] = 'File type is not allowed'

    if 'files' not in request.files:
        resp = jsonify({'msg': "No body files attached in request"})
        resp.status_code = 501
        return resp

    if files.filename == '':
        resp = jsonify({'msg': "No file files selected"})
        resp.status_code = 404
        return resp
     
    error = {}
    # success = False
         
    if files and allowed_file(files.filename):
        filename = secure_filename(files.filename)
        files.save(os.path.join(DATASET_PATH, files.filename))
        success = True
    else:
        error[files.filename] = "File type is not allowed"
 
    if success and error:
        flash('Dataset yang dimasukan tidak sesuai')
        return redirect('/buatModel')
    if success:
        nama1 = re.sub(' ', '-', nama)
        model_path1 = os.path.join(MODEL_PATH, f'{nama1}.pkl')
        model_path2 = os.path.join(MODEL_PATH, f'{nama1}-vector.pkl')
        dataset_path = os.path.join(DATASET_PATH, filename)

        file_path = f"tweets-data/{nama1}.csv"
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["full_text"]
        
            writer.writerow(field)

        df = pd.read_csv(dataset_path)
        
        data=df['tweet'].fillna(' ')
        labels=df['label']

        data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2, random_state=42)

        vectorizer = TfidfVectorizer()
        features_train = vectorizer.fit_transform(data_train)

        svm_model = svm.SVC(kernel='sigmoid', C=1)
        svm_model.fit(features_train, labels_train)

        features_test = vectorizer.transform(data_test)

        predictions = svm_model.predict(features_test)

        akurasi = accuracy_score(labels_test, predictions)*100

        file = model_path1
        pickle.dump(svm_model, open(file, 'wb'))

        file = model_path2
        pickle.dump(vectorizer, open(file, 'wb'))

        newTokoh = Tokoh(nama, akurasi, urlImage)
        db.session.add(newTokoh)
        db.session.commit()
        tokohs = tokoh_schema.dump(newTokoh)
        konten = Tokoh.query.all()
        tokos= tokohs_schema.dump(konten)
        return render_template('updateData.html', data=tokos)
    else:
        flash('Dataset yang dimasukan tidak sesuai')
        return redirect('/buatModel')
        # return jsonify({"msg": "Success buat model", "status": 200, "data": tokohs})

def getAllTokoh():
    konten = Tokoh.query.all()
    tokos= tokohs_schema.dump(konten)
    return render_template('updateData.html', data = tokos)