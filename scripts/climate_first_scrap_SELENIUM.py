from os import getenv
from time import time
from datetime import date
import re
import logging

import pandas as pd
# import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import Error
from selenium import webdriver


def construct_url(country, state, city):
    if country == 'United States':
        country = ''.join([state.replace(' ', '-'), '-usa'])
    else:
        country = country.replace(' ', '-')
    city = city.replace(' ', '-')
    url = f"https://www.weather-atlas.com/en/{country}/{city}-climate?c,mm,mb,km"
    # Units of measurement are forced in the request
    # In the future I will not do reconciliation on them
    return url


def scrap_city_dict(url):
    city_dict = {}
    try:
        # r = requests.get(url, allow_redirects=False).text
        driver.get(url=url)
        driver.find_element('xpath', '/html/body/div[1]/div[3]/div[2]/div[1]/a[1]').click()
        r = driver.page_source
        soup = BeautifulSoup(r, 'lxml')
        ul_tags = soup.find_all('ul', class_='list-unstyled mb-0')
        if not ul_tags:
            print(f'wrong url: {url}')
        else:
            for ul in ul_tags:
                li_tags = ul.find_all('li')
                for li in li_tags:
                    city_dict[li.a.text] = li.span.text
            for key, value in city_dict.items():
                city_dict[key] = re.split(r'(\-?\d*\.?\d+|\d+)', value)
    except Exception as ex:
        print(f"[INFO] {url} Error: ", ex)

    return city_dict


def get_params_dict(city_dict):
    params_dict = {}
    for key, value in city_dict.items():
        item = key.split(' in ')
        param = item[0]
        if param not in params_dict.keys():
            params_dict[param] = [param.removeprefix('Average ').removesuffix('erature').replace(' ', '_').lower()]
            params_dict[param].append(value[2].strip().lstrip('В').replace('h', 'hours').replace('km/hours', 'km/h'))
    return params_dict


def get_months_dict(city_dict):
    count = 0
    months_dict = {}
    for key, value in city_dict.items():
        item = key.split(' in ')
        month = item[1]
        if month not in months_dict.keys():
            count += 1
            months_dict[month] = count
    return months_dict


def create_climate_into_db(params_dict):
    climate_params = ''  # Part to insert into SQL table creation
    comments = ''  # SQL query to add comments to a table
    for key, value in params_dict.items():
        climate_params += f'{value[0]} numeric(5,1),'
        comments += f"COMMENT ON COLUMN avg_climate.{value[0]} IS '{key}, {value[1]}';"
    with open("./sql/create_avg_climate.sql") as sql_script:
        sql_script = sql_script.read().format(climate_params=climate_params)
    cursor.execute(sql_script)
    cursor.execute(comments)
    connection.commit()


def get_columns_list(params_dict):
    # To create an empty template DataFrame
    columns_list = []
    for key, value in params_dict.items():
        columns_list.append(value[0])
    return columns_list


def params_template_df(months_dict, columns_list):
    df_params_templ = pd.DataFrame(index=months_dict.values(), columns=columns_list, dtype=None)
    df_params_templ.loc[:, :] = None
    df_params_templ.insert(0, 'city_id', None)
    df_params_templ.insert(1, 'month', df_params_templ.index)
    return df_params_templ


def fill_params_template_df(city_dict, months_dict, params_dict, df_params_fill):
    for key, value in city_dict.items():
        item = key.split(' in ')
        month = months_dict[item[1]]
        column = params_dict[item[0]][0]
        num = float(value[1])
        df_params_fill.loc[month, column] = num
    return df_params_fill
    #  = df_params_full


if __name__ == '__main__':
    # ========================== change *.log ========================== #
    logging.basicConfig(filename="./data/logs_usa.log", filemode="w", level=logging.INFO)
    current_date = date.today()
    # data_engr = getenv('DATA_ENGR')
    data_engr = 'de_k2'

    # ========================== change *.pkl ========================== #
    df_numbeo = pd.read_pickle("./data/numbeo_links_usa.pkl")
    # Sorting to make it easier to find the error in the url
    df_numbeo.sort_values('country', inplace=True)
    # driver = webdriver.Firefox(executable_path='./data/firefox/geckodriver')
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)

    try:
        connection = psycopg2.connect(dbname="relohelper", user="postgres", password="5123", host="localhost")
        cursor = connection.cursor()

        # Create 'avg_climate' table in DB
        url_instance = 'https://www.weather-atlas.com/en/canada/vancouver-climate?c,mm,mb,km'
        city_dict_instance = scrap_city_dict(url_instance)
        params_dict = get_params_dict(city_dict_instance)
        months_dict = get_months_dict(city_dict_instance)
        create_climate_into_db(params_dict)

        # Scraping into 'avg_climate'
        columns_list = get_columns_list(params_dict)
        df_params_empty = params_template_df(months_dict, columns_list)

        start_time = time()
        for index, row in df_numbeo.iterrows():
            url = construct_url(row['country'], row['state_name'], row['city'])
            city_dict = scrap_city_dict(url)
            if not city_dict:
                logging.info('city_id:%s:wrong_url:%s', index, url)
            else:
                df_params_fill = df_params_empty.copy()
                df_params_fill['city_id'] = index
                df_params_full = fill_params_template_df(city_dict, months_dict, params_dict, df_params_fill)
                # df_params_full[['sys_updated_date', 'sys_updated_by']] = [date.today(), getenv('DATA_ENGR')]
                df_params_full[['sys_updated_date', 'sys_updated_by']] = [date.today(), 'de_k2']
                for row in df_params_full.itertuples(index=False):
                    cursor.execute("INSERT INTO avg_climate VALUES %s", (tuple(row),))
                connection.commit()
    except (Exception, Error) as error:
        print("[INFO Error]:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            finish_time = time()
            print("[INFO] Postgres connection closed.")
            print("Code execution time: ", finish_time - start_time)
            logging.info('Finished scraping: %s', finish_time - start_time)

# postgresql://localhost:5123@postgres/numb
# conn = psycopg2.connect(dbname="numb", user="postgres", password="5123", host="localhost")
