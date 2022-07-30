from flask import Flask, request, render_template, url_for, redirect, jsonify, json
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from BirdClassificationModel.main import predict_bird_species
import wikipedia
import pandas as pd
import requests

UPLOAD_FOLDER = '/Users/adityapise/HackathonProjects/BirdDex/BirdDex/static/uploaded_image'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birddex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret-key"

db = SQLAlchemy(app)


class BirdsCatalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    latin_name = db.Column(db.String(200), unique=True)
    img_url = db.Column(db.String(200), unique=True)
    sound_url = db.Column(db.String(200))
    description = db.Column(db.String())


db.create_all()


def get_latin_name(common_name: str) -> str:
    df = pd.read_csv("birds_latin_names.csv")
    latin_name = df[df['class'] == common_name.upper()]["SCIENTIFIC NAME"].values[0]
    return latin_name


def get_sound_bird(common_name: str) -> str:
    params = {
        "query": common_name
    }
    xeno_sound_url = "https://xeno-canto.org/sounds/uploaded/"
    sound_data = requests.get(url="https://xeno-canto.org/api/2/recordings", params=params).json()['recordings'][0]
    sound_file = sound_data['file-name']
    temp = xeno_sound_url.replace("https:", '')
    sub_folder = sound_data['sono']['small'].replace(temp, '').split('/')[0]
    full_path = xeno_sound_url + sub_folder + "/" + sound_file
    return full_path


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img_url = f"static/uploaded_image/{filename}"
        species = predict_bird_species(file_path).title()
        description = wikipedia.summary(species)
        latin_name = get_latin_name(species)
        sound_url = get_sound_bird(species)
        new_bird = BirdsCatalog(name=species,
                                latin_name=latin_name,
                                img_url=img_url,
                                sound_url=sound_url,
                                description=description)
        db.session.add(new_bird)
        db.session.commit()
    return render_template('index.html')


@app.route('/get_bird_data')
def get_birds_data():
    bird_dict = {}
    bird_list = BirdsCatalog.query.all()
    for bird in bird_list:
        bird_dict[bird.id] = {
            "name": bird.name,
            "latin_name": bird.latin_name,
            "img_url": bird.img_url,
            "sound_url": bird.sound_url,
            "description": bird.description
        }
    return jsonify(bird_dict)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
