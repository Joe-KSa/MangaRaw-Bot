import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://rawkuma.com"

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

def load_page():
    url = f"{BASE_URL}/manga/?page=1&order=update"
    soup = get_soup(url)
    
    mangas_info = []
    
    if soup:
        mangas = soup.find_all('div', class_='bsx')
        for manga in mangas[:3]:
            img = manga.find('img')
            url = manga.find('a').get('href')
            if img:
                title = img.get('title')
                img_url = img.get('src')
                mangas_info.append((title, url, img_url))
    
    return mangas_info

def find_manga(name):
    manga_name = name.replace(' ', '-').replace('–', '-')  # Reemplazar el guion largo por guion normal
    url = f"{BASE_URL}/{manga_name}/"
    soup = get_soup(url)
    
    chapters_info = []
    
    if soup:
        items = soup.find('ul', class_="clstyle")
        if items:
            chapters = items.find_all('li')
            
            # Obtener los 10 capítulos más recientes
            recent_chapters = chapters[:10]
            for chapter in recent_chapters:
                title = chapter.find('span', class_='chapternum')
                url = chapter.find('a').get('href')
                if title:
                    chapters_info.append((title.text.strip(), url))
            
            # Obtener los 10 capítulos más antiguos si hay suficientes capítulos
            if len(chapters) > 10:
                old_chapters = chapters[-10:]
                for chapter in old_chapters:
                    title = chapter.find('span', class_='chapternum')
                    url = chapter.find('a').get('href')
                    if title:
                        chapters_info.append((title.text.strip(), url))
    
    return chapters_info

def reader_cap(url):
    soup = get_soup(url)
    images_urls = []
    
    if soup:
        reader_container = soup.find('div', id="readerarea")
        if reader_container:
            images = reader_container.find_all('img')
            for image in images:
                img_url = image.get('src')
                if img_url:
                    img_url_fixed = re.sub(r'\s+', '%20', img_url)
                    images_urls.append(img_url_fixed)
    return images_urls

def search_manga(name):
    manga_name = name.replace(' ', '+')
    url = f"{BASE_URL}/page/1/?s={manga_name}"
    soup = get_soup(url)

    mangas_info = []
    
    if soup:
        mangas = soup.find_all('div', class_='bsx')
        for manga in mangas:
            img = manga.find('img')
            manga_url = manga.find('a').get('href')
            if img:
                title = img.get('title')
                img_url = img.get('src')
                
                mangas_info.append((title, img_url, manga_url))
    
    return mangas_info