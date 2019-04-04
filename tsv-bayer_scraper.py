# coding=utf-8
from selenium import webdriver
import logging
import os
from xlsxwriter.workbook import Workbook
import datetime
import time

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
    URLs = list()                                                           # Hardcoded list of urls we need to scrape, imported from 'urls.xlsx'
    URLs = ['https://www.tsv-bayer-dormagen.de/abteilungen/fechten/trainingszeiten',
            'https://www.tsv-bayer-dormagen.de/abteilungen/fu%C3%9Fball/trainingszeiten',
            'https://www.tsv-bayer-dormagen.de/abteilungen/schwimmen/trainingszeiten',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/aerobic-und-fitness',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/boxen',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/ju-jutsu',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/gymnastik-und-sportspiele',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/pr%C3%A4ventionssport',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/seniorensport',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/kraftsport',
            'https://www.tsv-bayer-dormagen.de/abteilungen/breitensport/rehabilitationssport',
            'https://www.tsv-bayer-dormagen.de/abteilungen/kinder-und-jugendsport/eltern-kinder-sport',
            'https://www.tsv-bayer-dormagen.de/abteilungen/kinder-und-jugendsport/kindersport-4-bis-12-jahre',
            'https://www.tsv-bayer-dormagen.de/abteilungen/kinder-und-jugendsport/kiss-%E2%80%93-kindersportakademie',
            'https://www.tsv-bayer-dormagen.de/abteilungen/weitere-abteilungen/basketball',
            'https://www.tsv-bayer-dormagen.de/abteilungen/weitere-abteilungen/judo',
            'https://www.tsv-bayer-dormagen.de/abteilungen/weitere-abteilungen/turnen',
            'https://www.tsv-bayer-dormagen.de/abteilungen/weitere-abteilungen/volleyball',
            'https://www.tsv-bayer-dormagen.de/handball/abteilung/trainingszeiten']
    result = []
    page_idx = 0
    pages_count = len(URLs)
    for url in URLs:                                                        # main loop, where we go through each page from URLs, one by one
        page_idx += 1
        logging.info('page {} of {}: '.format(page_idx, pages_count) + url)
        selenium_driver.get(url)
        try:
            selenium_driver.find_element_by_tag_name('title')
            logging.info('page loaded successfully')
        except:
            logging.error('page loading failed')
            continue
        course_title_part1 = ''                                             # initializing local variables
        course_title_part2 = ''
        day = ''
        start_time = ''
        end_time = ''
        trainer = ''
        location = ''
        parsed_rows_count = 0
        logging.info('starting parsing that page')
        rows = selenium_driver.find_element_by_css_selector('table.dmTable').find_elements_by_xpath("./*")
        for row in rows:                                                    # nested loop through all rows in table
            if row.tag_name == 'caption':
                try:
                    course_title_part1 = row.text
                except:
                    pass
            elif row.tag_name == 'thead':
                try:
                    course_title_part2 = row.find_element_by_tag_name('a').text
                except:
                    pass
            elif row.tag_name == 'tbody':
                try:
                    shedules = row.text.split('\n')
                    if len(shedules) > 1:
                        for idx in range(len(shedules) // 3):
                            parsing_error = False
                            day = shedules[idx * 3]
                            splitted_text = shedules[idx * 3 + 1].split(' - ')
                            if len(splitted_text) > 1:
                                start_time = splitted_text[0].replace(' ', '')
                                splitted_text = splitted_text[1].split('Uhr')
                                if len(splitted_text) > 1:
                                    end_time = splitted_text[0].replace(' ', '')
                                    trainer = splitted_text[1].strip()
                                else:
                                    parsing_error = True                    # can't extract end_time
                            else:
                                parsing_error = True                        # can't extract start_time
                            location = shedules[idx * 3 + 2]
                            entry = ['' + course_title_part1 + ' ' + course_title_part2,
                                     '',                                    # category
                                     day,
                                     start_time,
                                     end_time,
                                     location,
                                     '',                                    # description
                                     '',                                    # level
                                     trainer,
                                     '']                                    # other
                            if not parsing_error:
                                result.append(entry)
                                parsed_rows_count += 1
                            else:
                                logging.error('failed to parsing row: ' + str(entry))
                            day = ''                                        # clearing local variables before parsing next row
                            start_time = ''
                            end_time = ''
                            trainer = ''
                            location = ''
                except:
                    pass
        logging.info(
            'finished parsing that page. {} rows added to results ({} rows total)'.format(str(parsed_rows_count),
                                                                                          str(len(result))))
        time.sleep(2)                                                       # waiting 2 seconds to avoid blocking due to too frequent requests
    logging.info('finished parsing results. {} rows parsed.'.format(len(result)))
    selenium_driver.close()                                                 # closing driver to prevent resources leaks
    selenium_driver.quit()
    logging.info('driver closed')
    return result


def save_results(data):
    logging.info('starting saving results')
    header = [['course_title', 'category', 'day', 'start_time', 'end_time',
               'location', 'description', 'level', 'trainer', 'other']]
    data = header + data
    filename = os.path.basename(__file__).split('.')[0] + '_' + str(datetime.datetime.now()).replace(":", "_") + '.xlsx'
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row, line in enumerate(data):
        for col, entry in enumerate(line):
            worksheet.write(row, col, entry)
    workbook.close()
    logging.info('finished saving results to file {}'.format(filename))


if __name__ == "__main__":
    start = time.time()
    driver = setup_selenium_driver()
    scrape_results = parse(driver)
    save_results(scrape_results)
    end = time.time()
    logging.info('execution took {} secs'.format(str(int(end - start))))
