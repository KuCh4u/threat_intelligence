import schedule
import time
import feedparser
from datetime import datetime
from app.models import Feed, Keyword, Article
from app.db import session
import sys
import os
from web_scraper import (
    scrape_github_security,
    scrape_cve_org,
    scrape_cisco_security,
    scrape_fortinet_blog
)

# Asegurar importación desde raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

LOG_FILE = "scraper.log"

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def get_feeds():
    return session.query(Feed).all()

def get_keywords():
    return [k.word.lower() for k in session.query(Keyword).all()]

def fetch_and_store_news():
    feeds = get_feeds()
    keywords = get_keywords()

    total_new = 0
    log("🚀 Iniciando scraping...")

    for feed in feeds:
        added = 0
        parsed_feed = feedparser.parse(feed.url)
        for entry in parsed_feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            if session.query(Article).filter_by(link=link).first():
                continue

            content = f"{title} {summary}".lower()
            if any(kw in content for kw in keywords):
                article = Article(
                    title=title,
                    summary=summary,
                    link=link,
                    source=feed.name
                )
                session.add(article)
                added += 1
                total_new += 1

        if added:
            log(f"{feed.name}: {added} noticia(s) nueva(s) agregada(s).")
        else:
            log(f"{feed.name}: sin coincidencias esta vez.")

    session.commit()
    log(f"Scraping completo. Total nuevas: {total_new}.\n")

# Ejecutar cada 5 minutos
schedule.every(5).minutes.do(fetch_and_store_news)
schedule.every(5).minutes.do(scrape_github_security)
schedule.every(5).minutes.do(scrape_cve_org)
schedule.every(5).minutes.do(scrape_cisco_security)
schedule.every(5).minutes.do(scrape_fortinet_blog)

# Primera ejecución inmediata
fetch_and_store_news()

# Loop
while True:
    schedule.run_pending()
    time.sleep(1)
