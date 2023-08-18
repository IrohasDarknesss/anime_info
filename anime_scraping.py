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

def get_yymm_from_file(yymm_file):
    with open(yymm_file, 'r') as file:
        yymms = [line.strip() for line in file]
    return yymms

# Scraping
def anime_info_scraping(word, logger):


    url = 'https://anime.eiga.com/program' + word

    logger.info(url)

    source = requests.get(url)
    source.encoding = source.apparent_encoding

    soup = bs(source.text, "html.parser")

    return soup

def execute(query_path):
    yymm_list = './search_list/yymm.txt'
    exec_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    yymms = get_yymm_from_file(yymm_list)
    
    logger = setting_log(f"./log/{exec_datetime}.log")
    logger.info("-----------------START-------------------")

    name_list = get_query_from_file(query_path)
    for yymm in yymms:
        csv_path = f"./data/animelist_{yymm}.csv"
        
        logger.info(f"Creating CSV file: {csv_path}")
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["title", "info"]
            writer.writerow(header)
            
            for name in name_list:
                logger.info("Search Name:" + name)
                soup = anime_info_scraping(name, logger)
                div = soup.find_all('div', class_='animeSeasonItemBox04 clearfix')
                
                for anime in div:
                    _title = anime.find('div', class_='seasonAnimeTtl')
                    _info = anime.find('div', class_='seasonAnimeDetail')
                    row = [_title, _info]
                    writer.writerow(row)
                    time.sleep(2)

    logger.info("-----------------END-------------------")
if __name__ == '__main__':
    execute(data)