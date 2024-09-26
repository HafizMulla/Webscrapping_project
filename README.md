# Webscrapping_project
## TCSWebScrapping 

This repo store the Web Scrapping scripts used to search for the keywords on the TCS website and downloadable contents such as brouchures in pdf format.

Page Object Model is followed in this framework

**Scripts** folder contains the script file 

**Files** folder store all the outcome files 

### **Setup**
- Install the dependencies from `requirements.txt`
```sh
pip install -r requirements.txt
```
- Grab all the variables from `.env` and add it to your OS environment path.
- Download the chrome driver with version `98.0.X`
- To run the script:
```sh

Run script for the following using any one command:
	python main.py --mode all : To run script for all the below options in one go
	python main.py --mode tcs-pdf : To run script for tcs pdf files
	python main.py --mode four-season-pdf : To run script for four pdf files
	python main.py --mode white-label : To run script for searching keywords in White labeled website
	python main.py --mode tcs-com : To run script for searching keywords in TCS COM website
	python main.py --mode tcs-uk : To run script for searching keywords in TCS Co Uk website
	python main.py --mode four-season : To run script for searching keywords in Four Season website

```
To exclude any keyword from the search list, set it to False.
For example: Change this "'Our Private Trav-': True" to "'Our Private Trav-': False"
