from TCSWebScrapping.Framework.basepages.webscraping_website import Webscraping_website
from TCSWebScrapping.Framework.utilities.websiteutility.website_management_utility import Website_Management_Utilities
from TCSWebScrapping.Framework.resource.four_season_urls import FOUR_SEASON_ULRS
from TCSWebScrapping.Framework.utilities.utilities import merge_multiple_csv_into_one_csv,\
    remove_old_individual_csv_files, get_current_date_time


class FourSeasonWebsite(Webscraping_website):

    def run_four_season_website(self):

        files = {
            'output_file': 'output/fourseason/website/final_fourseason_combined_' + \
                                str(get_current_date_time()) + '.csv',
            'filename': "output/fourseason/website/fourseason_"
        }

        self.extract_text_from_four_season_sites(files)

    def extract_text_from_four_season_sites(self, files):
        """ This method will extract the text from the white labeled sites """

        counter = 0
        website_management_utilities = Website_Management_Utilities()

        # get the cleaned text from each urls
        for i, item in enumerate(FOUR_SEASON_ULRS):
            files['filename'] = files['filename']+str(i+1)

            # Extract text from the web base pages
            csv_files = website_management_utilities.extract_text_from_web_page(
                item,
                counter,
                files['filename'],
                mode='four-season'
            )

            # merged the multiple csv files into 1 combined csv file
            merge_multiple_csv_into_one_csv(csv_files, files['output_file'])

            # remove all the individual csv files
            remove_old_individual_csv_files(csv_files)
