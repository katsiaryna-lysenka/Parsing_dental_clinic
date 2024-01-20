import requests
import time
import json
from bs4 import BeautifulSoup
import re

url = "https://dentalia.com/clinica/"
       # "https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/",
       # "https://www.santaelena.com.co/tiendas-pasteleria/tienda-bogota/",
       # "https://www.santaelena.com.co/tiendas-pasteleria/tienda-monteria/",
       # "https://www.santaelena.com.co/tiendas-pasteleria/tiendas-pastelerias-pereira/",
       # "https://www.santaelena.com.co/tiendas-pasteleria/nuestra-pasteleria-en-barranquilla-santa-elena/"

output_file = "result.json"
cookies = {'_ga': 'GA1.1.798642735.1705659686', '_lscache_vary': '7f9211ff83e640e486010157d7d75cd1', '_gcl_au': '1.1.961798081.1705659693', '_hjSessionUser_3724640': 'eyJpZCI6IjE1Y2NkYTA3LTNkNGItNWQ0MC05MWViLTI5NDYxMGU0MzgyMyIsImNyZWF0ZWQiOjE3MDU2NTk2OTM5NjQsImV4aXN0aW5nIjp0cnVlfQ==', 'PHPSESSID': 'e6qam4gppv1k32hg2mjmvspddk', '_hjIncludedInSessionSample_3724640': '0', '_hjSession_3724640': 'eyJpZCI6IjI2ZDQxNjBiLTk1OWItNDViZS05MjZkLTM2MGNjM2U4NzBlZiIsImMiOjE3MDU3NDQ3NTI0NTIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=', '_ga_94GCJ4Q0CE': 'GS1.1.1705744750.5.1.1705745728.0.0.0', '_ga_EN8BN980LH': 'GS1.1.1705744750.5.1.1705745729.59.0.0', '_ga_FMK4KRGVF2': 'GS1.1.1705744750.5.1.1705745729.0.0.0'}

nocache_value = int(time.time())
url_with_params = f"{url}?nocache={nocache_value}"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    'action': 'jet_engine_ajax',
    'handler': 'get_listing',
    'page_settings[post_id]': 5883,
    'page_settings[queried_id]': '344706|WP_Post',
    'page_settings[element_id]': 'c1b6043',
    'page_settings[page]': 1,
    'listing_type': 'elementor',
    'isEditMode': False,
}

result_list = []


def func_for_response(url_with_params):
    response = requests.post(url_with_params, headers=headers, cookies=cookies, data=data)
    response.raise_for_status()
    return response

try:

    for url_item in url:
        response = func_for_response(url_with_params)

    if response.ok:
        json_data = json.loads(response.text)

        html_content = json_data['data']['html']

        soup = BeautifulSoup(html_content, 'html.parser')

        elements_with_class = soup.select('.jet-listing-grid__item')

        def extract_schedule(schedule_string):
            matches = re.findall(r'Horario: (.*?)(?=\r\n|$)', schedule_string)
            return matches

        for element in elements_with_class:
            result_item = {}

            name_element = element.select_one('h3.elementor-heading-title.elementor-size-default')

            address_element = element.select_one('.elementor-element.elementor-element-b843495.elementor-widget.elementor-widget-jet-listing-dynamic-field')

            latlon_element = element.select_one('.elementor-element.elementor-element-a6c6867 a[href]')

            phones_element = element.select_one('.elementor-element.elementor-element-cb84d19.elementor-widget.elementor-widget-jet-listing-dynamic-field')

            working_ours_element = element.select_one('.elementor-element.elementor-element-9e2c33b.elementor-widget.elementor-widget-jet-listing-dynamic-field')

            if name_element:
                result_item['name'] = name_element.text.strip()

            if address_element:
                result_item['address'] = address_element.text.strip()

            if latlon_element and 'href' in latlon_element.attrs:
                href_value = latlon_element['href']
                matches = re.search(r'@([-?\d.]+),([-?\d.]+),(\d+)z', href_value)
                if matches:
                    latitude = float(matches.group(1))
                    longitude = float(matches.group(2))
                    result_item['latlon'] = [latitude, longitude]

            if phones_element:
                phone_strings = phones_element.text.strip().split('\n')
                result_item['phones'] = [re.sub(r'\D', '', phone) for phone in phone_strings]

            if working_ours_element:
                schedules = extract_schedule(working_ours_element.text.strip())
                result_item['working_hours'] = schedules

            result_list.append(result_item)

    with open('result.json', 'w', encoding='utf-8') as json_file:
        json.dump(result_list, json_file, ensure_ascii=False, indent=2)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")



