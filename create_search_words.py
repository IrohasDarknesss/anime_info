with open('search_list/season_query.txt', 'w') as file:
    for year in range(2010, 2023):
        #'winter', 'spring'
        seasons = ['0', '1', '2', '3']
        for season in seasons:
            url = f'/year/{year}-{season}.php'
            file.write(url + '\n')


with open('search_list/yymm.txt', 'w') as file:
    for year in range(2010, 2024):
        #'Apr', 'Jul'
        seasons = ['Apr', 'Jul', 'Oct', 'Jan']
        for season in seasons:
            text = f'{year}_{season}'
            file.write(text + '\n')