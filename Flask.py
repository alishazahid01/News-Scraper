from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, render_template, request

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AlishaZahid:123456789alisha@cybernews.uvgy6mw.mongodb.net/")
db = client.SecurityNewsAggregator
News = db.News

def fuzzy_matching(keyword):
    result = News.aggregate([
        {
            "$search": {
                "index": "SearchNews",
                "text": {
                    "query": keyword,
                    "path": ["title",'link'],
                    "fuzzy": {}
                }
            }
        }
    ])
    return list(result)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        search_results = fuzzy_matching(keyword)
        return render_template("index.html", search_results=search_results, keyword=keyword)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
