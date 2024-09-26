from utilities.utilities import get_current_date_time

PDF_MAIN_DICT = {
        "t1_pdf": {
            "output_file": 'output/t1/pdf/final_combined_csv_' + str(get_current_date_time()) + '.csv',
            "input_files": 'output/t1/pdf/combined_csv*.csv',
            "output_file_loc": 'output/t1/pdf/',
            "url_file_path": 'resource/t1_pdf_urls.txt',
            "domain_name": 'https://www.t1.com'
        },
        "f1_pdf": {
            "output_file": 'output/f1/pdf/final_PDF_combined_csv_' + str(get_current_date_time()) + '.csv',
            "input_files": 'output/f1/pdf/combined_csv*.csv',
            "url_file_path": 'resource/f1_pdf_urls.txt',
            "output_file_loc": 'output/f1/pdf/',
            "domain_name": 'https://www.f1.com',
        }
    }
