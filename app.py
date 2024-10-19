import os
from datetime import datetime
from os.path import dirname, join

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


# base url home
@app.route("/")
def home():
    return render_template("index.html")


# base url show diary
@app.route("/diary", methods=["GET"])
def show_diary():
    # sample_receive = request.args.get("sample_give")
    # print(sample_receive)

    articles = list(db.diary.find({}, {"_id": False}))
    return jsonify({"articles": articles})


# base url save diary
@app.route("/diary", methods=["POST"])
def save_diary():
    # sample_receive = request.form.get("sample_give")
    # print(sample_receive)

    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")

    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

    file = request.files["file_give"]
    """
    - file.filename: nama asli file diupload
    - split("."): memisahkan nama file berdasarkan tanda titik
    - [-1]: mengakses angka terakhir dari list hasil split
    """
    file_extension = file.filename.split(".")[-1]
    # membuat path untuk penyimpanan file
    file_name = f"static/post-{mytime}.{file_extension}"
    # method save menyimpan file ke path yang dibuat
    file.save(file_name)

    profile = request.files["profile_give"]
    profile_extension = profile.filename.split(".")[-1]
    profile_name = f"static/profile-{mytime}.{profile_extension}"
    profile.save(profile_name)

    time = today.strftime("%a, %Y-%m-%d")

    doc = {
        "file": file_name,
        "profile": profile_name,
        "title": title_receive,
        "content": content_receive,
        "time": time,
    }
    db.diary.insert_one(doc)

    return jsonify({"msg": "Diary saved successfully!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
