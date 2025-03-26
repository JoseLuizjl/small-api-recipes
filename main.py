from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

df = pd.read_csv("dataset/dataset.csv")
df = df.drop(['Unnamed: 0', 'link', 'source'], axis=1)
df = df.dropna()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    new_image = Image(image_path=filepath)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Image uploaded successfully', 'image_path': filepath}), 200

@app.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    image_paths = [image.image_path for image in images]
    return jsonify(image_paths), 200

@app.route('/random_recipe', methods=['GET'])
def get_random_recipe():
    random_recipe = df.sample(n=1).iloc[0]
    
    return jsonify({
        "title": random_recipe['title'],
        "ingredients": eval(random_recipe['ingredients']),
        "directions": eval(random_recipe['directions'])
    })

if __name__ == '__main__':
    app.run()
