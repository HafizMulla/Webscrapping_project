
from TCSWebScrapping.Framework.basepages.webscrapping_files import Webscraping_file
from TCSWebScrapping.Framework.resource.pdf_main_dict import PDF_MAIN_DICT
from TCSWebScrapping.Framework.utilities.utilities import get_valid_urls_from_raw_urls
from TCSWebScrapping.Framework.utilities.fileutility.file_management_utilities import File_Management_Utilities
from TCSWebScrapping.Framework.utilities.utilities import merge_multiple_combined_csv_into_one_final_csv


class FourSeasonPdf(Webscraping_file):

    def run_four_season_pdf_function(self):

        self.extract_text_from_four_season_pdf_files()

        print('Done web-scrapping pdf files')

    def extract_text_from_four_season_pdf_files(self):

        file_management = File_Management_Utilities()

        valid_urls_file = get_valid_urls_from_raw_urls(
            PDF_MAIN_DICT["four_pdf"]["url_file_path"],
            PDF_MAIN_DICT["four_pdf"]["domain_name"]
        )

        file_management.download_and_search_keywords(
            valid_urls_file,
            PDF_MAIN_DICT["four_pdf"]["output_file_loc"]
        )

        # merging all the combined csv files into 1 final combined csv file
        merge_multiple_combined_csv_into_one_final_csv(
            PDF_MAIN_DICT["four_pdf"]["input_files"],
            PDF_MAIN_DICT["four_pdf"]["output_file"]
        )
