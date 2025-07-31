from flask import render_template, request, redirect, url_for
from app import app
from app.models import Feed, Keyword
from app.db import session

@app.route("/")
def index():
    return "<h1>Sistema Threat Intelligence</h1>"

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
