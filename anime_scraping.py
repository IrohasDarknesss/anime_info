from bs4 import BeautifulSoup as bs
import csv
import requests
import time
import logging, datetime
import re, os
import glob, getpass
from tqdm import tqdm

# Query File Path
data = './search_list/season_query.txt'

#save_path
save_csv_dir = glob.glob('./data/*csv')

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

# delete same name csv
def delete_same_file(dirs):
    for dir in dirs:
        if os.path.exists(dir):
            print('Duplicate files found.')
            os.remove(dir)
            print('Delete to prevent duplication.')
            print('Deletion completed.')
        else:
            pass

# Scraping
def anime_info_scraping(word, logger):


    url = 'http://ruijianime.com/main' + word

    logger.info(url)

    source = requests.get(url)
    source.encoding = source.apparent_encoding

    soup = bs(source.text, "html.parser")

    return soup

def additional_pages_scraping(base_word, logger, writer):
    base_url = 'http://ruijianime.com/main'
    page_number = 1
    while page_number <= 3:  # 60になるまでループを続ける
        url = f"{base_url}{base_word}?start={page_number * 20}"
        logger.info(url)
        source = requests.get(url)
        if source.status_code == 404:
            logger.info(f"No more additional pages for {base_word} starting from page {page_number}.")
            break
        source.encoding = source.apparent_encoding
        soup = bs(source.text, "html.parser")
        
        div = soup.find_all('div', class_=re.compile('year_'))
        for anime in div:
            _title = anime.find('h2')
            if _title:
                for span in _title.find_all('span'):
                    span.decompose()
                _title = _title.text
            _info = anime.find('p', class_='exp').text
            row = [_title, _info]
            writer.writerow(row)
            time.sleep(2)
        
        page_number += 1

        if page_number >= 60:  # page_numberが60以上になったらループを終了する
            logger.info(f"Page limit reached ({page_number}), stopping additional scraping.")
            break
    
def execute(query_path, del_dir):
    yymm_list = './search_list/yymm.txt'
    exec_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    yymms = get_yymm_from_file(yymm_list)

    print('To prevent duplication, check whether an existing file exists.')
    delete_same_file(del_dir)
    print('Duplicate checks completed.')

    print('Start loading the programme.')

    for _ in tqdm(range(100), desc="Loading", ncols=100, ascii=True):
        time.sleep(0.1) 
    print('Loading complete.')
    time.sleep(3)

    choice = input("The programme is ready to start. Do you want to run the programme? (yes/no): ").strip().lower()
    if choice in ['yes', 'y', 'YES', 'Yes']:
        print('Enter the final excecution phase')
        time.sleep(3)
        print('Execution rights are required to run this programme.')
        time.sleep(3)
        password = getpass.getpass("Please enter the execution password.: ")
        if password == "620978":
            print("Authentication completed. Start of programme execution.")
            logger = setting_log(f"./log/{exec_datetime}.log")
            logger.info("-----------------START-------------------")

            name_list = get_query_from_file(query_path)
            for yymm, name in zip(yymms, name_list):
                csv_path = f"./data/animelist_{yymm}.csv"
                
                logger.info(f"Creating CSV file: {csv_path}")
                
                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    header = ["title", "info"]
                    writer.writerow(header)
                    
                    logger.info("Search Name:" + name)
                    soup = anime_info_scraping(name, logger)
                    div = soup.find_all('div', class_=re.compile('year_'))
                        
                    for anime in div:
                        _title = anime.find('h2')
                        if _title:
                            for span in _title.find_all('span'):
                                span.decompose()
                            _title = _title.text
                        _info = anime.find('p', class_='exp').text
                        row = [_title, _info]
                        writer.writerow(row)
                        time.sleep(2)
                    logger.info(f'Writing to {csv_path} completed.')

                    # Check if there are additional pages and scrape them
                    additional_pages_scraping(name, logger, writer)
                    
            logger.info("-----------------END-------------------")

            print("The programme has been executed.")
        else:
            print("The execution password is incorrect. Access has been denied.")
    elif choice in ['no', 'n', 'NO', 'No']:
        print("Execution cancelled.")
    else:
        print("Input character error: answer with 'yes', 'y', 'YES', 'Yes' or ''no', 'n', 'NO', 'No'.")
    
if __name__ == '__main__':
    execute(data, save_csv_dir)