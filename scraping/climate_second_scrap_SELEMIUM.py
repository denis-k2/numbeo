import json

from selenium import webdriver as wd

from climate_first_scrap_SELENIUM import *


def scrap_city_dict2(url):
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


# Open the file with the corrected links
with open("./data/correct_urls_usa.json") as file:
    correct_links = json.load(file)

if __name__ == '__main__':
    DATA_ENGR = getenv('DATA_ENGR')
    URL = getenv('SQLALCHEMY_RELOHELPER_URL')
    # ========================== change *.log ========================== #
    logging.basicConfig(filename="./data/logs_correct_urls_usa.log", filemode="w", level=logging.INFO)
    current_date = date.today()
    driver = wd.Firefox()
    driver.implicitly_wait(10)

    try:
        connection = psycopg2.connect(URL)
        cursor = connection.cursor()

        url_instance = 'https://www.weather-atlas.com/en/canada/vancouver-climate?c,mm,mb,km'
        city_dict_instance = scrap_city_dict2(url_instance)
        params_dict = get_params_dict(city_dict_instance)
        months_dict = get_months_dict(city_dict_instance)
        columns_list = get_columns_list(params_dict)
        df_params_empty = params_template_df(months_dict, columns_list)

        start_time = time()
        for index, url in correct_links.items():
            print(url)
            city_dict = scrap_city_dict2(url)
            if not city_dict:
                logging.info('city_id:%s:wrong_url:%s', index, url)
            else:
                df_params_fill = df_params_empty.copy()
                df_params_fill['city_id'] = index
                df_params_full = fill_params_template_df(city_dict, months_dict, params_dict, df_params_fill)
                df_params_full[['sys_updated_date', 'sys_updated_by']] = [date.today(), DATA_ENGR]
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
