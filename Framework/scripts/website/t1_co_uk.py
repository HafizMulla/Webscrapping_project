from TCSWebScrapping.Framework.basepages.webscraping_website import Webscraping_website
from TCSWebScrapping.Framework.utilities.websiteutility.website_management_utility import Website_Management_Utilities
from TCSWebScrapping.Framework.resource.tcs_site_map_urls import TCS_SITE_MAP_URL
from TCSWebScrapping.Framework.utilities.utilities import get_current_date_time


class TCSCOUKWebsite(Webscraping_website):

    def __int__(self):
        super().__init__()

    def run_tcs_co_uk_website(self):

        website_management = Website_Management_Utilities()

        files = {
            'filename': "output/tcs/website/uk_sitemap_" + str(get_current_date_time()) + "_combined.csv"
        }

        website_management.extract_text_from_tcs_sitemap(TCS_SITE_MAP_URL[1], files)
