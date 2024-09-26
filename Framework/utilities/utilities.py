import argparse
import os
import glob
import requests
from bs4 import BeautifulSoup #pip install bs4
import pandas as pd
import time
import datetime
from TCSWebScrapping.Framework.utilities.Slackbot import SlackBot


def merge_multiple_csv_into_one_csv(csv_file_list, file_name):
    """ Function to merge the multiple csv files into 1 final csv file"""

    try:
        combined_csv = pd.DataFrame()
        print("\nMerging multiple csv files into one csv file")
        combined_csv = pd.concat([pd.read_csv(f, encoding='cp437') for f in csv_file_list])
        combined_csv.to_csv(file_name, index=False)
        print('-'*20)
        print('Merging completed.\nPlease refer the final file with all the findings '
              'in the file:{}.'.format(file_name))

    except Exception as e:
        print('Error raised while merging csv file:{}'.format(e))


def merge_multiple_combined_csv_into_one_final_csv(input_files, output_file):
    """ This function will merge the multiple combined csv files into 1 final csv file"""

    files = glob.glob(input_files)

    try:
        print('\nNow merging all the combined csv files into Final_combined_csv file')
        with open(output_file, 'a', encoding='cp437') as singleFile:
            for csvFile in files:
                print('Merging file:{}'.format(csvFile))
                for line in open(csvFile, 'r', encoding='cp437'):
                    singleFile.write(line)

        print('-'*20)
        print('Merging completed.\nPlease refer the final file with all the findings '
              'in the file:{}.'.format(output_file))

        remove_old_individual_csv_files(files)

    except Exception as e:
        print('Error raised while merging csv file:{}'.format(e))


def remove_old_individual_csv_files(csv_file_list):
    """ This function is to remove the individual test csv files for each urls"""

    print('Deleting all the individual files')
    for csv_file in csv_file_list:
        os.remove(csv_file)
    print('-'*30)

def get_valid_urls_from_raw_urls(url_file, domain_name):
    """
    This method will read the urls.txt file which contains all the urls and
    will return only valid urls

    """
    valid_url_list = []

    with open(url_file) as url_links:
        try:
            for url_link in url_links:
                url_link = url_link.replace('ï»¿', '').replace('\n', '').replace('\ufeff', '')
                url_link = url_link.replace(' ','')
                complete_url_link = domain_name + url_link
                print("complete_url_link", complete_url_link)
                valid_url_list.append(complete_url_link)

            return valid_url_list

        except Exception as e:
            print('Exception raised while fetching valid urls from raw url:{}'.format(e))


def download_pdf_files_and_save_on_local(file_url):
    """
    This function will download the pdf files from the urls and store it into
    a dummy pdf file for further processing
    """

    try:
        req = requests.get(file_url, stream=True)
        file_name = ""
        if req.status_code == 200:
            file_name = 'output/dummy_pdf_file.pdf'
            with open(file_name, 'wb') as f:
                f.write(req.content)

            print('Successfully downloaded the pdf files')
        elif req.status_code == 404:
            print(f'No pdf file exist as we got error:{req.status_code}')

        else:
            # This line will handle for any failures in BeautifulSoup4 functions:
            print('Error in code for url:{} with status code:{}'.format(file_url, req.status_code))

        return file_name

    except Exception as e:
        print('Exception raised while downloading the file content:{}'.format(e))


def search_and_download_brochure_links_from_four_season_website(url_link):
    """ This function is searching and returning all the pdf files links """
    try:
        page = requests.get(url_link).text
        soup = BeautifulSoup(page, 'lxml')

        if soup.find('div', {"class": "Destination-CTAs"}):
            page_content = soup.find('div', {"class": "Destination-CTAs"})
            download_div = page_content.find('a')
            print('Found pdf file:', download_div['href'])
            return download_div['href']
        else:
            print("No downloadable file exist on this page:{}".format(url_link))

    except Exception as e:
        print('Exception raised while searching the pdf links:{} in the brochure:{}'.format(url_link, e))


def merge_individual_csv_into_one_combined_csv(csv_file_list, count, file_location):
    """ This function to merge all the multiple csv files into 1 combined csv file"""

    combined_csv = pd.DataFrame()

    print('\nMerging individual test csv files into one combined csv file')
    combined_csv = pd.concat([pd.read_csv(f, encoding='cp437') for f in csv_file_list])
    combined_csv.to_csv(file_location+'/combined_csv'+str(count)+'.csv', index=False)

    print("Merging completed.\nPlease refer file 'combined_csv"+str(count)+".csv'")


def capture_time():
    print('-'*20)
    print('Time :{}'.format(round(time.perf_counter(),2)))
    print('-'*20)
    return time.perf_counter()


def total_time_spent(start_time, end_time):
    print('-'*30)
    duration = round(end_time - start_time, 2)
    print('Total time spent :{} seconds'.format(duration))
    print('-'*30)


def get_current_date_time():
    current_date_time = str(datetime.datetime.now())
    formatted_date_time = current_date_time.replace(" ", "_").replace(":", "_").replace(",", "_").split('.')[0]
    return formatted_date_time


def agr_parser():
    """" This function is use for command line argument and for running specific options from the choices """

    parser = argparse.ArgumentParser(description="List to run script for running the scripts for TCS Com, "
                                                 "TCS Co Uk, White label domains or Four Season website or pdf files.")

    parser.add_argument(
        '--mode', dest='format', type=str,
        choices=['all', 'pdf', 'tcs-pdf', 'four-season-pdf', 'white-label', 'tcs-com', 'tcs-uk', 'four-season'],
        help="Run script for the following using any one command:\n\n"
             "tcs-pdf : For running script for tcs pdf files\\n"
             "four-pdf : For running script for four pdf files\n"
             "white-label : For running script for searching keywords in "
             "White labeled website\n"
             "tcs-com : For running script for searching keywords in TCS COM website\n"
             "tcs-uk : For running script for searching keywords in TCS Co Uk website\n"
             "four : For running script for searching keywords in Four Season website"
        )

    # Read arguments from command line
    args = parser.parse_args()
    fmt = args.format

    return fmt


def send_file_over_slack(filename):
    slackbot = SlackBot()
    slackbot.post_message_on_slack("Sending file now")
    slackbot.post_file_on_slack(filename)
    slackbot.post_message_on_slack("File sent")
