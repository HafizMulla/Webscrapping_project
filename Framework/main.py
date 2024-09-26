import sys
sys.path.append("../..")

from TCSWebScrapping.Framework.scripts.file.four_season_pdf import FourSeasonPdf
from TCSWebScrapping.Framework.scripts.file.tcs_pdf import TcsPdf
from TCSWebScrapping.Framework.scripts.website.four_season_web import FourSeasonWebsite
from TCSWebScrapping.Framework.scripts.website.tcs_com import TCSCOMWebsite
from TCSWebScrapping.Framework.scripts.website.tcs_co_uk import TCSCOUKWebsite
from TCSWebScrapping.Framework.scripts.website.white_labeled import WhiteLabelWebsite
from TCSWebScrapping.Framework.utilities.utilities import capture_time, total_time_spent, agr_parser, get_current_date_time

import transcript

if __name__ == '__main__':

    transcript.start('reports/logfile_{}.log'.format(get_current_date_time()))

    four_season_pdf = FourSeasonPdf()
    tcs_pdf = TcsPdf()
    four_season_website = FourSeasonWebsite()
    tcs_com_website = TCSCOMWebsite()
    tcs_co_uk_website = TCSCOUKWebsite()
    white_labeled_site = WhiteLabelWebsite()
    args_option = agr_parser()
    start_time = capture_time()

    if args_option in ['white-label', 'all']:
        # Running for White label sites
        print("Running for White labelled websites")
        white_labeled_site.run_white_labeled_website()

    if args_option in ['tcs-com', 'all']:
        # Running for Sitemap of TCS .com domain sitemap
        print("Running for TCS .com domain website sitemap")
        tcs_com_website.run_tcs_com_website()

    # As per Ann's comment, tcsworldtravel.co.uk is now removed from the search list as all the pages from .co.uk are
    # redirect to tcsworldtravel.com url - 2nd June 2023
    # if args_option in ['tcs-uk', 'all']:
    #     # Running for Sitemap of TCS .co.uk domain sitemap
    #     print("Running for TCS .co.uk domain website sitemap")
    #     tcs_co_uk_website.run_tcs_co_uk_website()

    if args_option in ['four-season', 'all']:
        # Running for Sitemap of TCS .co.uk domain sitemap
        print("Running for Four Season website")
        four_season_website.run_four_season_website()

    if args_option in ['tcs-pdf', 'pdf', 'all']:
        print("Running TCS pdf web-scrapping")
        tcs_pdf.run_tcs_pdf_function()

    if args_option in ['four-season-pdf', 'pdf', 'all']:
        # This will only be run once the script for four-season-website is run.
        print("Running four-pdf web-scrapping")
        four_season_pdf.run_four_season_pdf_function()

    end_time = capture_time()

    total_time_spent(start_time, end_time)

    transcript.stop()
