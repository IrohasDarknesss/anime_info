with open('search_list/season_query.txt', 'w') as file:
    for year in range(2015, 2024):
        seasons = ['winter', 'spring', 'summer', 'autumn']
        for season in seasons:
            url = f'/season/{year}-{season}/'
            file.write(url + '\n')