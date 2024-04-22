import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('dashboard.html')

@app.route('/fruit', methods=['GET'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template('index.html', fruit=fruit)

@app.route('/addfruit', methods=['GET', 'POST'])
def addfruit():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']

        if gambar:
            namaGambarAsli = gambar.filename
            namaFileGambar = namaGambarAsli.split('/')[-1]
            file_path = os.path.join('static', 'assets', 'imgGambar', namaFileGambar)
            gambar.save(file_path)
        else:
            namaFileGambar = None

        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi,
            'gambar': namaFileGambar
        }
        db.fruit.insert_one(doc)
        return redirect(url_for("fruit"))
    
    return render_template('Addfruit.html')

@app.route('/editfruit/<_id>', methods=['GET', 'POST'])
def editfruit(_id):
    if request.method == 'POST':
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']
        
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi,
        }

        if nama_gambar:
            namaGambarAsli = nama_gambar.filename
            namaFileGambar = namaGambarAsli.split('/')[-1]
            file_path = os.path.join('static', 'assets', 'imgGambar', namaFileGambar)
            nama_gambar.save(file_path)
            doc['gambar'] = namaFileGambar

        db.fruit.update_one({"_id": ObjectId(_id)}, {"$set": doc})
        return redirect(url_for("fruit"))
    

    id = ObjectId(_id)
    data = list(db.fruit.find({"_id": id}))
    return render_template('EditFruit.html', data=data)

@app.route('/delete/<_id>', methods=['GET'])
def delete(_id):
    db.fruit.delete_one({"_id":ObjectId(_id)})
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)