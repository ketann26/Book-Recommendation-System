from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open("model.pkl",'rb'))
book_pivot = pickle.load(open("book_pivot.pkl",'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form.get('title')

    # recommendation
    res = []
    book_id = np.where(book_pivot.index == title)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id].values.reshape(1,-1), n_neighbors=6)
    print(suggestions)
    for i in range(len(suggestions[0])):
        if i!=0:
            res.append(book_pivot.index[suggestions[0][i]])

    return render_template("index.html", res=res)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)