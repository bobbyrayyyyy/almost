import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

TARGET_KEYWORDS = {
    "about": ["about", "who-we-are", "mission", "team"],
    "services": ["services", "solutions", "products", "offerings"],
    "news": ["news", "press", "updates", "insights", "blog"]
}

def match_keywords(url, keywords):
    return any(kw in url.lower() for kw in keywords)

def find_target_links(start_url, soup):
    base_domain = urlparse(start_url).netloc
    links = {"about": set(), "services": set(), "news": set()}

    for a in soup.find_all("a", href=True):
        href = urljoin(start_url, a["href"])
        parsed_href = urlparse(href)

        if parsed_href.netloc == "" or parsed_href.netloc == base_domain:
            for section, keywords in TARGET_KEYWORDS.items():
                if match_keywords(href, keywords):
                    links[section].add(href)
    return links

def scrape_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = [tag.get_text(strip=True) for tag in soup.find_all(["h1", "h2", "h3", "p", "li"])]
        clean_text = "\n".join([t for t in texts if len(t.split()) > 3])
        return clean_text[:2000]
    except:
        return ""

def scrape_target_sections(base_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        base_html = requests.get(base_url, headers=headers, timeout=10).text
        soup = BeautifulSoup(base_html, "html.parser")
        section_links = find_target_links(base_url, soup)

        output = {}
        for section, urls in section_links.items():
            texts = []
            for url in list(urls)[:3]:
                text = scrape_text_from_url(url)
                if text:
                    texts.append(text)
                    time.sleep(0.5)
            output[section] = "\n\n--- PAGE BREAK ---\n\n".join(texts)
        return output

    except Exception:
        return {"about": "", "services": "", "news": ""}