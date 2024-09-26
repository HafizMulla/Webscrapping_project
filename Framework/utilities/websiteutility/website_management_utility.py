import re
from bs4 import BeautifulSoup #pip install bs4
import requests
import csv
import traceback
from TCSWebScrapping.Framework.resource.search_keywords import SEARCH_KEYWORDS
from TCSWebScrapping.Framework.utilities.utilities import search_and_download_brochure_links_from_four_season_website, \
    merge_multiple_csv_into_one_csv, remove_old_individual_csv_files


class Website_Management_Utilities:

    def extract_text_from_tcs_sitemap(self, main_url, files):
        """ This method will extract the text from the TCS .com domain site """

        counter = 0
        csv_files = []

        try:
            print('main_url:', main_url)
            resp = requests.get(main_url)

            if resp.status_code == 200:

                # extract all the links from the sitemap xml
                valid_links = self.extract_text_from_xml(resp)

                # get the cleaned text from each urls
                csv_files = self.get_cleaned_text_from_the_urls(counter, valid_links, files['filename'])

                # merged the multiple csv files into 1 combined csv file
                merge_multiple_csv_into_one_csv(csv_files, files['filename'])

                # remove all the individual csv files
                remove_old_individual_csv_files(csv_files)

            else:
                # This line will handle for any failures in BeautifulSoup4 functions:
                print('Error in code for url:{} with status code:{}. '
                      'No file is generated'.format(main_url, resp.status_code))


        except Exception as e:
            print('Exception raised while running main url:{}'.format(e))

    def extract_text_from_web_page(self, main_url, counter, filename, mode=None):
        """This method will extract all the text from the web base pages"""

        download_brochure_links = []
        csv_files = []
        csv_flag = "false"

        try:
            print('main_url:', main_url)
            resp = requests.get(main_url)

            if resp.status_code == 200:

                try:
                    # get all the urls
                    all_urls = self.get_all_urls_from_web_page(resp, main_url, counter)
                    print('Got all the urls from the website')

                    # this code inside if condition will only run for the 'Four Season' part
                    if mode == 'four-season':

                        for i, item in enumerate(all_urls):
                            # Searching and downloading brochure links
                            try:
                                print("Collecting all the pdf files from the website")
                                brochure_link = search_and_download_brochure_links_from_four_season_website(item)

                                if brochure_link:
                                    download_brochure_links.append(brochure_link)

                                # writing in an external pdf url text file
                                with open("resource/four_season_pdf_urls.txt", "w") as file:
                                    file.write('\n'.join(download_brochure_links))
                                    file.close()

                            except Exception as e:
                                print('Exception raised while downloading the pdf '
                                                   'links {} got error:{}'.format(item, e))

                        print("All the pdf of the Four seasons links are downloaded")

                    # Adding main url for web scrapping on 1st position
                    all_urls.insert(0, main_url)

                    # get the cleaned text from each urls and store into 1 combined csv file
                    csv_files = self.get_cleaned_text_from_the_urls(counter, all_urls, filename)
                    csv_flag = "True"
                    return csv_files, csv_flag

                except Exception as e:
                    print('Exception raised while iterating through all web base pages:{}'.format(e))

            elif resp.status_code == 404:
                print(f"The URL does not exist.It giving the error code:{resp.status_code}")
                csv_flag = "False"
                return csv_files,csv_flag

        # Handling for any URLs that don't have the correct protocol
        except Exception as e:
            print('Exception raised while hitting the main url:{} got error:e'.format(main_url, e))

    def get_all_urls_from_web_page(self, resp, main_url, counter):
        """This function return all the urls from the web page"""

        # Create the beautifulsoup object:
        soup = BeautifulSoup(resp.text, 'html.parser')

        print('Searching for Urls:{} in the web page {}'.format(main_url, counter+1))

        try:
            urls = []
            complete_url_list = []
            lines_seen = set()

            # Adding all the raw urls into the raw url file
            raw_url_file = open('output/raw_url_file' + str(counter) + '.txt', 'w')

            # traverse paragraphs from soup
            for link in soup.find_all("a"):
                data = link.get('href')

                # Avoiding adding the duplicate urls in file
                label_name = main_url.split('/')
                n1 = "/"+label_name[3]+"/"
                if data is not None and data.startswith(n1):
                    data.split()
                    urls.append(data)
                    lines_seen.add(data)
                    raw_url_file.write(data)
                    raw_url_file.write("\n")

            raw_url_file.close()

            # Updating the incomplete url with 'https://www.tcsworldtravel.com/' and storing in the file
            refined_url_file = open('output/complete_url_file' + str(counter) + '.txt', 'w')
            # traverse paragraphs from soup
            for url in lines_seen:
                if url.startswith(('http', 'https')):
                    complete_url_list.append(url)
                    refined_url_file.write(url)
                    refined_url_file.write("\n")
                else:
                    complete_url = main_url.split(n1)[0] + url
                    complete_url_list.append(complete_url)
                    refined_url_file.write(complete_url)
                    refined_url_file.write("\n")

            refined_url_file.close()

            return complete_url_list

        except Exception as e:
            print('Exception raised:{}'.format(e))

    def get_cleaned_text_from_the_urls(self, counter, all_urls, filename):
        """Iterating through all the urls"""

        csv_file_names = []

        for url in all_urls:

            counter = counter + 1

            print('\nUrl no:{} - Iterating for the url:{}'.format(counter, url))
            resp = requests.get(url)

            # We will only extract the text from successful requests:
            if resp.status_code == 200:

                # extract the text from the url web page
                website_extracted_text = self.extract_text_from_the_web_page(resp.content, counter)

                # search the key-words in the extracted text from the web page
                keyword_list = self.search_key_words_on_the_extracted_text(website_extracted_text, url, counter)

                # Storing the word's occurrence detail in a csv file
                csv_file_name = self.save_keyword_findings_to_csv_file(keyword_list, counter, filename)

                csv_file_names.append(csv_file_name)

            else:
                # This line will handle for any failures in BeautifulSoup4 functions:
                print('Error in code for url:{} with status code:{}'.format(url, resp.status_code))

        return csv_file_names

    def extract_text_from_the_web_page(self, response_content, counter):
        """ This method will search the key-words in the extracted text from the web page"""
        try:

            # Create the beautifulsoup object:
            soup = BeautifulSoup(response_content, 'html.parser')

            # Finding the text:
            text = soup.find_all(text=True)

            # Remove unwanted tag elements:
            cleaned_text = ''
            blacklist = [
                '[document]',
                'noscript',
                'header',
                'html',
                'meta',
                'head',
                'input',
                'script',
                'style', ]

            print('Searching for the text in the web page for url {}'.format(counter))
            # Then we will loop over every item in the extract text and make sure that the beautifulsoup4 tag
            # is NOT in the blacklist
            for item in text:
                if item.parent.name not in blacklist:
                    cleaned_text += '{} '.format(item)
            extracted_text = cleaned_text.strip()
            # print("a", a)
            # a.replace('\n', ' ')
            return extracted_text

        except Exception as e:
            print('Exception occurred while reading the text from website:{}'.format(e))

    def search_key_words_on_the_extracted_text(self, cleaned_text, url, counter):
        """ This method will search the key-words in the extracted text from the web page
        and store them in the dictionary. Will return the same dictionary"""

        try:
            output_list = []
            # cleaned_text = a.replace('\n', '').replace('\t', ' ')

            for search_item in SEARCH_KEYWORDS:
                word_dict = {}
                print("Searching the text '{}' on url no:{}".format(search_item, counter))
                pattern = r'\b{}\b'.format(search_item)
                occurrence_list = re.findall(pattern, cleaned_text, re.IGNORECASE)
                no_of_occurrence = len(occurrence_list)
                sentence = ""
                if no_of_occurrence > 0:
                    print("\tFound {} instances of the text '{}' on url no:{}".format(no_of_occurrence, search_item,
                                                                                      counter))
                    word_dict['url'] = url
                    word_dict['word'] = search_item
                    word_dict['no_of_occurrence'] = no_of_occurrence

                    for i in range(0, len(occurrence_list)):
                        partition_text = cleaned_text.partition(occurrence_list[i])
                        initial_text = partition_text[0].split('\n')

                        start_text = partition_text[0].split('\n')[len(initial_text) - 1]
                        middle_text = partition_text[1]
                        end_text = partition_text[2].split('\n')[0]

                        complete_sentence = start_text + middle_text + end_text
                        sentence = sentence + " New Sentence: " + complete_sentence
                        word_dict['sentence'] = sentence

                    output_list.append(word_dict)
                else:
                    print("\tNo. of instance found {} of the text '{}' on url no:{}".format(no_of_occurrence, search_item,
                                                                                      counter))

            return output_list

        except Exception as e:
            print('Exception occurred while searching the keywords in the extracted '
                  'web text for the url-{}:{}'.format(url, e))

    def save_keyword_findings_to_csv_file(self, output_list, counter, file_name):
        """Storing the word's occurrence detail in a csv file"""

        csv_file = []
        try:
            # csv_file = 'file\\test'+str(counter)+'.csv'
            csv_file = file_name + str(counter) + '.csv'
            with open(csv_file, 'w', newline='', encoding="utf-8") as f:
                w = csv.DictWriter(f, ['url', 'word', 'no_of_occurrence', 'sentence'])
                w.writeheader()

                w.writerows(output_list)

            return csv_file

        except Exception as e:
            print('Exception occurred while storing the word occurrence:{}'.format(e))


    def extract_text_from_xml(self, resp):

        try:
            sitemap_links = []

            # get the cleaned text from each urls
            soup = BeautifulSoup(resp.text, features='xml')

            # Finding all the tag 'loc':
            b_unique = soup.find_all('loc')

            for link in b_unique:
                sitemap_links.append(link.text)

            return sitemap_links

        except Exception as e:
            print('Exception occurred while extracting text from the XML:{}'.format(e))
