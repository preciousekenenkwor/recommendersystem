from flask import Flask, render_template, request
from model.recommender import MusicRecommender

# ✅ Define the Flask app first
app = Flask(__name__)

# ✅ Create an instance of your recommender
recommender = MusicRecommender('music_data.csv')

# ✅ Route for homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    song = ""
    if request.method == 'POST':
        song = request.form['song']
        results = recommender.recommend(song)
    return render_template('index.html', song=song, results=results)

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
