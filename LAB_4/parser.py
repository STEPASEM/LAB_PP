import requests
import asyncio
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.data_film = []
        self.url_film = "https://msk.kinoafisha.info/"

    async def parse_film(self):
        response = requests.get(self.url_film, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.text, 'html.parser')

        movies = soup.find_all('div', class_='movieItem_info')

        for movie in movies:
            title_elem = movie.find('a', class_='movieItem_title')
            if title_elem:
                self.data_film.append(title_elem.text.strip())

        return self.data_film