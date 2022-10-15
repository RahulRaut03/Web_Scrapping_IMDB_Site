import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


def get_movie_rank(doc):
    movie_rank = []
    Title_tag = doc.findAll('h3', {'class': 'lister-item-header'})
    for tag in Title_tag:
        rank_movie = tag.find('span', {'class': 'lister-item-index unbold text-primary'}).text
        movie_rank.append(rank_movie)
    return movie_rank

def get_movie_name(doc):
    movie_name = []
    Title_tag = doc.findAll('h3', {'class': 'lister-item-header'})
    for tag in Title_tag:
        name = tag.find('a').text
        movie_name.append(name)
    return movie_name

def get_movie_year(doc):
    movie_year = []
    Title_tag = doc.findAll('h3', {'class': 'lister-item-header'})
    for tag in Title_tag:
        year = tag.find('span', {'class': 'lister-item-year text-muted unbold'}).text
        movie_year.append(year[1:5])
    return movie_year

def get_movie_rating(doc):
    movie_rating = []
    div_tag = doc.findAll('div', {'class': 'ipl-rating-widget'})
    for tag in div_tag:
        tag1 = tag.find('span', {'class': 'ipl-rating-star__rating'})
        rating = tag1.text
        movie_rating.append(rating)
    return movie_rating

def get_imdb_link(doc):
    Title_tag = doc.findAll('h3', {'class': 'lister-item-header'})
    base_url = 'https://imdb.com'
    imdb_link = []
    for tag in Title_tag:
        link_tag = tag.find('a')
        link = base_url + link_tag['href']
        imdb_link.append(link)
    return imdb_link

def Top_Movies():
    Url = 'https://www.imdb.com/list/ls009997493/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
    response = requests.get(Url)

    if response.status_code != 200:
        raise Exception('Failed to URL "{}"'.format(Url))
    #print("URL loaded successfully")
    doc = BeautifulSoup(response.text, 'html.parser')


    movie_dict = {'Rank': get_movie_rank(doc),
                  'Movie Name': get_movie_name(doc),
                  'Year of Release': get_movie_year(doc),
                  'Rating': get_movie_rating(doc),
                  'Imdb Link': get_imdb_link(doc)}

    movie_data = pd.DataFrame(movie_dict)
    return movie_data


def get_movie_data(url, name):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Failed to URL "{}"'.format(url))
    # print("URL loaded successfully")
    doc = BeautifulSoup(response.text, 'html.parser')

    movie_data_dict = {'Movie Name': [],
                       'Release year': [],
                        'IMDB Rating' : [],
                       'Movie Desc': [],
                        'Directors': []}

    #name_tag = doc.find('h1', {'class': 'sc-b73cd867-0 eKrKux'})

    movie_data_dict['Movie Name'].append(name)

    year_tag = doc.find('a', {'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh'})
    movie_data_dict['Release year'].append(year_tag.text)

    rate_tag = doc.find('span', {'class': 'sc-7ab21ed2-1 jGRxWM'})
    movie_data_dict['IMDB Rating'].append(rate_tag.text)

    desc = doc.find('span', {'class': 'sc-16ede01-2 gXUyNh'})
    movie_data_dict['Movie Desc'].append(desc.text)

    director = doc.find('a', {
        'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
    movie_data_dict['Directors'].append(director.text)

    return pd.DataFrame(movie_data_dict)



def scrape_movie_data(url,path,name):
    if os.path.exists(path):
        print("The file {} already exists....Skipping....".format(path))
        return
    movie_df = get_movie_data(url,name)
    movie_df.to_csv(path, index=None)

def Top_movies_csv():
    print("Scrapping list of top 100 hindi movies...")
    movie_data_df = Top_Movies()
    #create a folder
    fname = 'Top Movies List'
    os.makedirs('Movie Data', exist_ok=True)
    #movie_data_df.to_csv('Movie Data/{}.csv'.format(fname), index=None)

    for index, row in movie_data_df.iterrows():
        print('Scrapping Movie data for movie "{}"'.format(row['Movie Name']))
        scrape_movie_data(row['Imdb Link'], 'Movie Data/{}.csv'.format(row['Movie Name']), row['Movie Name'])



Top_movies_csv() #function calling
