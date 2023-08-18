from bs4 import BeautifulSoup as bs
import csv
import requests
import time
import logging, datetime

# Query File Path
data = './search_list/season_query.txt'

#Setting log
def setting_log(logpath):
    
    formatter = '%(levelname)s : %(asctime)s : %(message)s'

    # Chage log level to DEBUG
    logging.basicConfig(level=logging.DEBUG, format=formatter, handlers=[logging.FileHandler(logpath, 'w', 'utf-8')])

    logger = logging.getLogger(__name__)

    return logger

# Get Query Info from Text File
def get_query_from_file(filename):
    with open(filename, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

# Scraping
def anime_info_scraping(word, logger):


    url = 'https://anime.eiga.com/program' + word

    logger.info(url)

    source = requests.get(url)
    source.encoding = source.apparent_encoding

    soup = bs(source.text, "html.parser")

    return soup

def execute(log, query_path):

    exec_datetiime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    log_path = f"./log/{exec_datetiime}.log"
    csv_path = f"./data/animelist_{exec_datetiime}.csv"

    name_list = get_query_from_file(query_path)
    for name in name_list:
        with open(csv_path, "w", newline="", encoding="utf-8"):
            div = soup.find_all('div', 'animeSeasonContainer')