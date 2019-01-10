# coding=utf-8
from selenium import webdriver
import logging
import os
from xlsxwriter.workbook import Workbook
import datetime
logging.basicConfig(level = logging.INFO)


def setup_selenium_driver():
    logging.info('starting init selenium')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    selenium_driver = webdriver.Chrome(chrome_options=chrome_options)
    logging.info('finished init selenium')
    return selenium_driver


def parse(selenium_driver):
    logging.info('staring parsing')
    # Implement your parsing code here
    result = [['Vinyasa Yoga', 'So', '10:00', '12:00', 'Einführung in Vinyasa Yoga'],
              ['Karate', 'So', '13:00', '15:00', 'Einführung in Karate']]
    logging.info('finished parsing results')
    return result


def save_results(data):
    logging.info('starting saving results')
    """
        data is expected to be an array of arrays. Each entry should consist of Title, Day, Start, Time, End, Time, Description.
        E.g. [['Vinyasa Yoga', 'So', '10:00', '12:00', 'Einführung in Vinyasa Yoga'], ['Karate', 'So', '13:00', '15:00', 'Einführung in Karate']]
    """
    header = ['Title', 'Day', 'Start', 'Time', 'End', 'Time', 'Description']
    data = header + data
    filename = os.path.basename(__file__).split('.')[0] + '_' + str(datetime.datetime.now()) + '.xlsx'
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row,line in enumerate(data):
        for col,entry in enumerate(line):
            worksheet.write(row, col, entry)
    logging.info('finished saving results')


driver = setup_selenium_driver()
scrape_results = parse(driver)
save_results(scrape_results)