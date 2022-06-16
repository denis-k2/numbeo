import pandas as pd
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import Error
from os import getenv
import time
from datetime import datetime, date


skip_list = [
    'Domestic Non-Alcoholic Beer (0.5 liter draught)',
    'Domestic Non-Alcoholic Beer (0.5 liter bottle)',
    'Imported Non-Alcoholic Beer (0.33 liter bottle)',
    'Bottle of Non-Alcoholic Wine (Mid-Range)',
    'Buffalo Round (1kg) (or Equivalent Back Leg Red Meat)'
]


def create_df_summary_empty():
    summary_dict = {
        'Restaurants': ['Summary',
                        'Family of four estimated monthly costs (without rent)',
                        'A single person estimated monthly costs (without rent)'],
        'Edit': ['Edit', None, None]
    }
    return pd.DataFrame(summary_dict)


def get_response(link):
    return requests.get(link).text


def get_soup(response):
    return BeautifulSoup(response, 'lxml')


def create_df_summary_complete(soup, df_summary_empty):
    try:
        div = soup.find('div', class_='seeding-call table_color summary limit_size_ad_right padding_lower other_highlight_color')
        items = div.find_all('li')
        costs_list = items[0].span.text.split(' ')
        if costs_list[0][-1] == '$':
            family_costs = costs_list[0]
            person_costs = items[1].span.text.split(' ')[0]
        elif costs_list[1][-2] == '$':
            family_costs = costs_list[1].strip('()')
            person_costs = items[1].span.text.split(' ')[1].strip('()')
        else:
            family_costs = None
            person_costs = None
    except:
        family_costs = None
        person_costs = None
    
    df_summary_complete = df_summary_empty.copy()
    df_summary_complete['Edit'][1] = family_costs
    df_summary_complete['Edit'][2] = person_costs
    
    return df_summary_complete


def last_update_pars(soup):
    try:
        div = soup.find('div', class_='align_like_price_table')
        last_date = div.find('br').next.lstrip('Last update: ').rstrip('\n')
        last_update = datetime.strptime(last_date, '%B %Y').date()
    except:
        last_update = None
    return last_update


def create_main_table(responce):
    return pd.read_html(responce)[1]


def tidy_main_table(table):
    table[['Edit', 'Range']] = table[['Edit', 'Range']].replace(',', '', regex=True)
    table.Edit = table.Edit.replace({"?": None})
    table.Edit = table.Edit.str.strip('\xa0$')
    table.Range = table.Range.str.split('-')
    table = table.where(pd.notnull(table), None)
    table = table.loc[table.Edit != 'Edit']
    
    for _, row in table.iterrows():
        try:
            row.Range = str(list(map(float, row.Range)))
        except:
            pass
        
    return table


def main_table_into_db(table, index, current_date, data_engr):
    # create connection
    # create cursor
    param_id = iter([5, 26]) # это Primary Keys (param_id) из numbeo_params для 'Imported Beer (0.33 liter bottle)'
    for _, row in table.iterrows():
        if row['Restaurants'] != 'Imported Beer (0.33 liter bottle)' and row['Restaurants'] not in skip_list:
            cursor.execute(
                "INSERT INTO numbeo_stats (city_id, param_id, cost, range, updated_date, sys_updated_date, sys_updated_by) \
                VALUES (%s, \
                (SELECT param_id FROM numbeo_params WHERE params = %s), \
                %s, %s, %s, %s, %s)",
                (index, row['Restaurants'], row['Edit'], row['Range'], last_update, current_date, data_engr)
            )
        elif row.Restaurants in skip_list:
            pass
        else:
            cursor.execute(
                "INSERT INTO numbeo_stats (city_id, param_id, cost, range, updated_date, sys_updated_date, sys_updated_by) \
                VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (index, next(param_id), row['Edit'], row['Range'], last_update, current_date, data_engr)
            )
        connection.commit()


if __name__ == "__main__":
    current_date = date.today()
    data_engr = getenv('DE_ENGR')
    df = pd.read_pickle("./data/numbeo_links.pkl")
    #df = df.iloc[390:396]
    df_summary_empty = create_df_summary_empty()

    start_time = time.time()
    try:
        connection = psycopg2.connect(getenv('POSTGRES_CONN'))
        cursor = connection.cursor()
    
        for index, row in df.iterrows():
            link = row['link']
            response = get_response(link)
            soup = get_soup(response)
            df_summary_complete = create_df_summary_complete(soup, df_summary_empty)
            df_main_table = create_main_table(response)
            df_main_table = pd.concat([df_main_table, df_summary_complete], ignore_index=True)
            df_main_table = tidy_main_table(df_main_table)
            last_update = last_update_pars(soup)
            main_table_into_db(df_main_table, index, current_date, data_engr)
    except (Exception, Error) as error:
        print("[INFO Error]:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            finish_time = time.time()
            print("[INFO] Postgres connection closed.")
            print("Code execution time: ", finish_time - start_time)
