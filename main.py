from flask import Flask, jsonify
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_csv("dataset/dataset.csv")
df = df.drop(['Unnamed: 0', 'link', 'source'], axis=1)
df = df.dropna()

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
