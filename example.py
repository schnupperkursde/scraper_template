# coding=utf-8
from selenium import webdriver
import logging
import os
from xlsxwriter.workbook import Workbook
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)


def setup_selenium_driver():
    logging.info('starting init selenium')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    selenium_driver = webdriver.Chrome(chrome_options=chrome_options)
    logging.info('finished init selenium')
    return selenium_driver


def parse(selenium_driver):
    logging.info('starting parsing')
    # Implement your parsing code here
    URL = "https://sportspass.de/sportangebot/"
    results = []
    selenium_driver.get(URL)
    count = len(selenium_driver.find_elements_by_css_selector(".course_date_link.link"))
    for idx in range(count):
        logging.info('processing course {} of {}'.format(idx+1, count))
        selenium_driver.get(URL)
        link = selenium_driver.find_elements_by_css_selector(".course_date_link.link")[idx]
        link.click()
        # for the first element after the click we wait until loading finished
        description = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".course_description"))
        )
        rows = selenium_driver.find_elements_by_css_selector(".table-row.items")
        for row in rows:
            results.append([
                row.find_element_by_css_selector('.text.course').text, # course_title
                row.find_element_by_css_selector('.text.course').text,  # category
                row.find_element_by_css_selector('.text.day').text, # day
                row.find_element_by_css_selector('.text.time').text.split('-')[0], #start_time
                row.find_element_by_css_selector('.text.time').text.split('-')[1],  # end_time
                row.find_element_by_css_selector('.text.sportcenter').text, #location
                description.text,
                row.find_element_by_css_selector('.text.level').text,  #level
                row.find_element_by_css_selector('.text.trainer').text, #trainer
                ' ', #other
            ])
    logging.info('finished parsing results')
    return results


def save_results(data):
    logging.info('starting saving results')
    header = [['course_title', 'category', 'day', 'start_time', 'end_time',
              'location', 'description', 'level', 'trainer', 'other']]
    data = header + data
    filename = os.path.basename(__file__).split('.')[0] + '_' + str(datetime.datetime.now()) + '.xlsx'
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row,line in enumerate(data):
        for col,entry in enumerate(line):
            worksheet.write(row, col, entry)
    workbook.close()
    logging.info('finished saving results to file {}'.format(filename))


if __name__ == "__main__":
    start = time.time()
    driver = setup_selenium_driver()
    scrape_results = parse(driver)
    save_results(scrape_results)
    end = time.time()
    logging.info('execution took {} secs'.format(end-start))