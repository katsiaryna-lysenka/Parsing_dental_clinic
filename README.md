## Dentalia Scraper
This Python script is designed to scrape information from a specific dental clinic website using the requests library and BeautifulSoup for parsing HTML content. The scraped data includes the name, address, geographical coordinates (latitude and longitude), phone numbers, and working hours of each dental clinic.

## Prerequisites
Python 3.x
Install the required libraries using the following command:

pip install requests beautifulsoup4

## Usage
Open the script in your preferred Python environment.
Set the url variable to the target dental clinic website.
Set the output_file variable to the desired output JSON file name.
Adjust the cookies dictionary if necessary, depending on the website's requirements.
Run the script.
The scraped data will be saved in the specified JSON file (result.json by default).

## Script Overview
The script follows these main steps:

Sends a POST request to the specified URL with necessary headers, cookies, and data payload.
Processes the HTML content of the response to extract relevant information.
Extracts data such as name, address, geographical coordinates, phone numbers, and working hours.
Saves the collected data in a JSON file (result.json).
