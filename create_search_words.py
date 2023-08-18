with open('search_list/season_query.txt', 'w') as file:
    for year in range(2015, 2024):
        seasons = ['winter', 'spring', 'summer', 'autumn']
        for season in seasons:
            url = f'/season/{year}-{season}/'
            file.write(url + '\n')


with open('search_list/yymm.txt', 'w') as file:
    for year in range(2015, 2024):
        seasons = ['Jan', 'Apr', 'Jul', 'Oct']
        for season in seasons:
            text = f'{year}_{season}'
            file.write(text + '\n')