from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import mariadb
import sys

import time
from datetime import datetime

import chromedriver_autoinstaller


chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--headless=new") # for Chrome >= 109


# Set the path for your ChromeDriver here
browser = webdriver.Chrome(options=chrome_options)
tickers = ['9988', '3690', '700', '1810', '9618']
translation = str.maketrans("", "", ",%")


try:
    conn = mariadb.connect(
        user="admin",
        password="K03cmErgBSz07mMfhDs6",
        host="db-warrants.c58gq2a6gh56.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        database="ccass"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


def save_data(created_date, ticker, shareholding, percent):
    print('Saving data to DB')
    print(f"{created_date}, {ticker}, {shareholding}, {percent}")
    cur.execute("INSERT IGNORE INTO ccass_summary (created_date, ticker, shareholding, percentage) VALUES (?,?,?,?)", (created_date, ticker, shareholding, percent))
    conn.commit()


def scrape_data(ticker):
    url = 'https://www3.hkexnews.hk/sdw/search/searchsdw.aspx'
    browser.get(url)
    input_element = browser.find_element(By.NAME, 'txtStockCode')
    input_element.send_keys(ticker)
    input_element.send_keys(Keys.RETURN)
    time.sleep(1)

    button = browser.find_element(By.ID, 'btnSearch')
    button.click()

    date = browser.find_element(By.NAME, 'txtShareholdingDate').get_attribute('value')
    formatted_date = datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
    ccass_search_total = browser.find_element(By.CLASS_NAME, 'ccass-search-total')
    shareholding = ccass_search_total.find_element(By.CLASS_NAME, 'shareholding').text
    formatted_shareholding = int(shareholding.translate(translation))
    percent = ccass_search_total.find_element(By.CLASS_NAME, 'percent-of-participants').text
    formatted_percent = float(percent.translate(translation))
    return formatted_date, ticker, formatted_shareholding, formatted_percent


def main():
    for ticker in tickers:
        formatted_date, ticker, formatted_shareholding, formatted_percent = scrape_data(ticker)
        save_data(formatted_date, ticker, formatted_shareholding, formatted_percent)
        print(f'Date: {formatted_date}, Ticker: {ticker} ,Shareholding: {formatted_shareholding}, Percent: {formatted_percent}')
        # pause the script to wait for page to load
        time.sleep(1)
    cur.close()
    browser.quit()

if __name__ == '__main__':
    main()


