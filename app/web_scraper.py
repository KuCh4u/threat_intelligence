import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.models import Article
from app.db import session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def scrape_github_security():
    print(f"[{datetime.now()}] 🔍 Scrape GitHub Security Advisories")
    url = "https://github.com/advisories"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a GitHub Advisories: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("article.Box-row")[:10]  # Top 10 entradas

    for card in cards:
        title_tag = card.select_one("a.Link--primary")
        if not title_tag:
            continue

        title = title_tag.text.strip()
        link = "https://github.com" + title_tag['href']
        summary = card.select_one("p").text.strip() if card.select_one("p") else ""

        # Verifica si ya existe
        if session.query(Article).filter_by(link=link).first():
            continue

        article = Article(
            title=title,
            summary=summary,
            link=link,
            source="GitHub Advisories"
        )
        session.add(article)
        print(f"Noticia agregada desde GitHub: {title}")

    session.commit()

def scrape_cve_org():
    print(f"[{datetime.now()}] 🔍 Scrape CVE.org News")
    url = "https://www.cve.org/News/AllNews"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a CVE.org: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".view-news-listing .views-row")

    for card in cards:
        title_tag = card.select_one("a")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link = "https://www.cve.org" + title_tag['href']
        summary_tag = card.select_one(".views-field-field-news-body")
        summary = summary_tag.text.strip() if summary_tag else ""

        if session.query(Article).filter_by(link=link).first():
            continue

        article = Article(
            title=title,
            summary=summary,
            link=link,
            source="CVE.org"
        )
        session.add(article)
        print(f"CVE.org: {title}")

    session.commit()

def scrape_cisco_security():
    print(f"[{datetime.now()}] 🔍 Scrape Cisco Security Advisories")
    url = "https://tools.cisco.com/security/center/publicationListing.x"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a Cisco: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("div.pubListing div.pubTitle a")[:10]

    for tag in rows:
        title = tag.text.strip()
        link = "https://tools.cisco.com" + tag['href']
        summary = "Aviso de seguridad de Cisco"

        if session.query(Article).filter_by(link=link).first():
            continue

        article = Article(
            title=title,
            summary=summary,
            link=link,
            source="Cisco Security"
        )
        session.add(article)
        print(f"Cisco: {title}")

    session.commit()

def scrape_fortinet_blog():
    print(f"[{datetime.now()}] 🔍 Scrape Fortinet Blog")
    url = "https://www.fortinet.com/blog"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a Fortinet: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".blog-post-card")

    for card in cards[:10]:
        title_tag = card.select_one("h3 a")
        if not title_tag:
            continue

        title = title_tag.text.strip()
        link = "https://www.fortinet.com" + title_tag['href']
        summary = card.select_one("p").text.strip() if card.select_one("p") else ""

        if session.query(Article).filter_by(link=link).first():
            continue

        article = Article(
            title=title,
            summary=summary,
            link=link,
            source="Fortinet Blog"
        )
        session.add(article)
        print(f"Fortinet: {title}")

    session.commit()
