
import re
import csv
import pdfplumber

from TCSWebScrapping.Framework.resource.search_keywords import SEARCH_KEYWORDS
from TCSWebScrapping.Framework.utilities.utilities import download_pdf_files_and_save_on_local, \
    merge_individual_csv_into_one_combined_csv, remove_old_individual_csv_files


class File_Management_Utilities:

    def download_and_search_keywords(self, valid_urls_file, output_file_location):

        combine_file_count = 0

        # Iterating through each urls
        for i, url in enumerate(valid_urls_file):
            combine_file_count = combine_file_count + 1
            print("\nUrl no:{} - Running for url: {}".format(combine_file_count, url))

            # Reading the pdf file
            downloaded_file = download_pdf_files_and_save_on_local(url)

            # Searching the keywords in the pdf file and storing in individual csv files
            if len(downloaded_file) > 0:
                csv_files_with_keywords = self.search_keywords_in_the_pdf_file(downloaded_file, url)

                # merging all the individual test csv files into 1 combined csv file
                merge_individual_csv_into_one_combined_csv(csv_files_with_keywords, combine_file_count, output_file_location)

                # remove all the individual files
                remove_old_individual_csv_files(csv_files_with_keywords)

    def search_keywords_in_the_pdf_file(self, pdf_file, correct_url):
        """
        This function will search the keywords in the pdf file and will store it in
        an individual csv files. It will return the same csv file.

        """
        csv_file_names = []

        try:
            with pdfplumber.open(pdf_file) as pdf:
                pages = pdf.pages

                for i, pg in enumerate(pages):
                    counter = i+1
                    csv_file_name = self.search_keywords_on_each_page(pg, counter, correct_url)
                    csv_file_names.append(csv_file_name)

                return csv_file_names

        except Exception as e:
            print("Exception raised while searching the keyword in the file:{}".format(e))

    def search_keywords_on_each_page(self, pg, counter, pdf_url,):
        """ This function will search keywords on individual page of the file"""

        output_list = []

        try:

            for search_item,flag in SEARCH_KEYWORDS.items():
                if flag:
                    word_dict = {}
                    text_fetch = pg.extract_text()
                    print("Searching the text '{}' on page no:{}".format(search_item, counter))
                    pattern = r'\b{}\b'.format(search_item)
                    # pattern = r'\w*-\s' # Finding words with hyphen at the end
                    occurrence_list = re.findall(pattern, text_fetch, flags=re.IGNORECASE)
                    sentence = ""

                    no_of_occurrence = len(occurrence_list)
                    if no_of_occurrence > 0:
                        print("\tFound {} instances of the text '{}' on page no:{}".format(no_of_occurrence, search_item, counter))
                        word_dict['url'] = pdf_url
                        word_dict['page_no'] = counter
                        word_dict['word'] = search_item
                        word_dict['no_of_occurrence'] = no_of_occurrence

                        for i in range(0, len(occurrence_list)):
                            partition_text = text_fetch.partition(occurrence_list[i])
                            initial_text = partition_text[0].split('\n')

                            start_text = partition_text[0].split('\n')[len(initial_text)-1]
                            middle_text = partition_text[1]
                            end_text = partition_text[2].split('\n')[0]

                            complete_sentence = start_text + middle_text + end_text
                            sentence = sentence + " New Sentence: " + complete_sentence
                            word_dict['sentence'] = sentence

                        output_list.append(word_dict)
                else:
                    print(f"Excluding the text '{search_item}' from searching as flag:{flag}")

        except Exception as e:
            print("Exception occurred:{}".format(e))

        # Storing the word's occurrence detail in a csv file
        csv_file = 'output/test'+str(counter)+'.csv'
        # csv_file = file_name + str(counter) + '.csv'

        try:
            with open(csv_file, 'w', newline='') as f:
                w = csv.DictWriter(f, ['url', 'page_no', 'word', 'no_of_occurrence', 'sentence'])
                w.writeheader()
                w.writerows(output_list)

        except Exception as e:
            print("Exception occurred:{}".format(e))

        return csv_file
