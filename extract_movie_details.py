import time
import random
import csv
from bs4 import BeautifulSoup
import requests
from utils import headers

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = requests.get(movie_link, headers=headers)
    movie_soup = BeautifulSoup(response.content, 'html.parser')

    if movie_soup is not None:
        title, date, rating, plot_text = None, None, None, None

        # Encontrando a seção específica
        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})
        if page_section is not None:
            divs = page_section.find_all('div', recursive=False)
            if len(divs) > 1:
                target_div = divs[1]

                # Título
                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()

                # Data
                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()

                # Classificação
                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                rating = rating_tag.get_text() if rating_tag else None

                # Sinopse
                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                plot_text = plot_tag.get_text().strip() if plot_tag else None

                with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                    movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if all([title, date, rating, plot_text]):
                        print(title, date, rating, plot_text)
                        movie_writer.writerow([title, date, rating, plot_text])
