from flask import render_template, request, redirect, url_for, jsonify
from app import app
from app.models import Feed, Keyword, Article
from app.db import session

@app.route("/")
def index():
    news = session.query(Article).order_by(Article.id.desc()).limit(50).all()
    return render_template("index.html", news=news)

@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        feed_name = request.form.get("feed_name")
        feed_url = request.form.get("feed_url")
        keyword = request.form.get("keyword")

        if feed_name and feed_url:
            session.add(Feed(name=feed_name, url=feed_url))
        if keyword:
            session.add(Keyword(word=keyword))

        session.commit()
        return redirect(url_for("config"))

    feeds = session.query(Feed).all()
    keywords = session.query(Keyword).all()
    return render_template("config.html", feeds=feeds, keywords=keywords)

@app.route("/log")
def view_log():
    try:
        with open("scraper.log", "r", encoding="utf-8") as f:
            log_content = f.readlines()
    except FileNotFoundError:
        log_content = ["No hay logs aún."]

    return render_template("log.html", log=log_content[::-1])  # Mostrar de más nuevo a más antiguo

@app.route("/export/json")
def export_json():
    articles = session.query(Article).order_by(Article.id.desc()).limit(100).all()
    data = [
        {
            "title": a.title,
            "summary": a.summary,
            "link": a.link,
            "source": a.source
        }
        for a in articles
    ]
    return jsonify(data)
