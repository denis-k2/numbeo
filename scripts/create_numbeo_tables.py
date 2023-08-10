from os import getenv

import pandas as pd
import psycopg2
from psycopg2 import Error


def aux_table(link):
    table = pd.read_html(link)[1]
    temp_tbl = pd.DataFrame([table.columns], columns=table.columns)
    table = pd.concat([temp_tbl, table]).reset_index(drop=True)
    for index, row in table.iterrows():
        if row['Edit'] == 'Edit':
            category = row['Restaurants']
            table.drop(index, inplace=True)
        else:    
            table.at[index, 'categories'] = category
    
    return table


def create_numbeo_category(table):
    with open("./sql/create_numbeo_category.sql") as sql_script:
        cursor.execute(sql_script.read())
        for item in table['categories'].unique():    
            cursor.execute("INSERT INTO numbeo_category (category) VALUES (%s)", (item,))
        cursor.execute("INSERT INTO numbeo_category (category) VALUES ('Summary');")
        connection.commit()


def create_numbeo_param(table):
    with open("sql/create_numbeo_param.sql") as sql_script:
        cursor.execute(sql_script.read())
        for index, row in table.iterrows():    
            cursor.execute(
                "INSERT INTO numbeo_param (category_id, param) \
                 VALUES ((SELECT category_id FROM numbeo_category WHERE category = %s), %s)",
                (row.categories, row.Restaurants)
            )
        cursor.execute(open("sql/insert_numbeo_param_summary.sql", "r").read())
        connection.commit()


def create_numbeo_stat():
    with open("sql/create_numbeo_stat.sql") as sql_script:
        cursor.execute(sql_script.read())
        connection.commit()


if __name__ == '__main__':
    link = pd.read_pickle("./data/numbeo_links.pkl").loc[1, 'link']
    
    try:
        # connection = psycopg2.connect(getenv('SQLALCHEMY_RELOHELPER_URL'))
        connection = psycopg2.connect('postgresql://postgres:5123@localhost:5432/relohelper')
        cursor = connection.cursor()
        
        table = aux_table(link)
        create_numbeo_category(table)
        create_numbeo_param(table)
        create_numbeo_stat()
    except (Exception, Error) as error:
        print("[INFO] Error:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("[INFO] PostgresQL connection closed")
