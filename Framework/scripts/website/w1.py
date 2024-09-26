from TCSWebScrapping.Framework.basepages.webscraping_website import Webscraping_website
from TCSWebScrapping.Framework.utilities.websiteutility.website_management_utility import Website_Management_Utilities
from TCSWebScrapping.Framework.utilities.utilities import get_current_date_time
from TCSWebScrapping.Framework.resource.while_label_urls import WHITE_LABEL_URLS
from TCSWebScrapping.Framework.utilities.utilities import merge_multiple_combined_csv_into_one_final_csv,\
    merge_multiple_csv_into_one_csv, remove_old_individual_csv_files


class WhiteLabelWebsite(Webscraping_website):

    def __int__(self):
        super().__init__()

    def run_white_labeled_website(self):

        files = {
            'output_file': 'output/whitelabel/final_whitelabel_combined_'
                           + str(get_current_date_time()) + '.csv',
            'input_file': 'output/whitelabel/whitelabel_*_combined.csv',
            'filename': "output/whitelabel/whitelabel_"
        }

        self.extract_text_from_white_labeled_sites(files)

    def extract_text_from_white_labeled_sites(self, files):
        """ This method will extract the text from the white labeled sites """

        counter = 0
        website_management_utilities = Website_Management_Utilities()

        # get the cleaned text from each urls
        for item in range(0, len(WHITE_LABEL_URLS)):
            csv_files, csv_flag = website_management_utilities.extract_text_from_web_page(WHITE_LABEL_URLS[item], counter, files['filename'])

            if csv_flag:
                # merged the multiple csv files into 1 combined csv file
                if len(csv_files) > 1:
                    merge_multiple_csv_into_one_csv(csv_files, files['output_file'])

                # remove all the individual csv files
                remove_old_individual_csv_files(csv_files)

        # merged the individual csv files into 1 final combined csv file
        merge_multiple_combined_csv_into_one_final_csv(files['input_file'], files['output_file'])


