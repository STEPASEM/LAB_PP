import requests
import asyncio
from bs4 import BeautifulSoup
from httpx import delete


class Parser:
    def __init__(self):
        self.data_film = {}
        self.url_film = "https://msk.kinoafisha.info/movies/"

    async def parse_film(self):
        response = requests.get(self.url_film, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.text, 'html.parser')

        movies = soup.find_all('div', class_='movieItem_info')

        for movie in movies:
            title_elem = movie.find('a', class_='movieItem_title')
            dop_inf = movie.find('span', class_='movieItem_subtitle')
            detail = movie.find('div', class_='movieItem_details')
            genres = detail.find('span', class_='movieItem_genres')
            time_location = detail.find('span', class_='movieItem_year')
            if dop_inf is None:
                dop_inf = ""
            else:
                dop_inf = dop_inf.text.strip()
            if title_elem:
                self.data_film[title_elem.text.strip()] = [title_elem.get('href'), dop_inf, genres.text.strip(), time_location.text.strip()]

        return self.data_film