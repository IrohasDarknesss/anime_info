with open('search_list/season_query.txt', 'w') as file:
    for year in range(2021, 2024):
        #'winter', 'spring'
        seasons = ['1', '2']
        for season in seasons:
            url = f'/year/{year}-{season}.php'
            file.write(url + '\n')


with open('search_list/yymm.txt', 'w') as file:
    for year in range(2021, 2024):
        #'Apr', 'Jul'
        seasons = ['Jul', 'Oct']
        for season in seasons:
            text = f'{year}_{season}'
            file.write(text + '\n')