"""
This file will scrap the website that we will get from topHospital file.

Since I wasn't not aware of task like 
    to suggest medicine: would have scraped data form top medical books
    to suggest doctor: should have scraped data from websites like practo
So I scraped all data in 'p'.

to keep the scraping process faster I kept MAX_DEPTH to 0 that is main page only  i.e., visiting  what level of sublinks in page
    like main_page have link carrers
                carrers have link apply_job
                    and so on............

"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from topHospital import hospital_list

MAX_DEPTH = 0  # Maximum depth of recursive scraping


def scrape_website(url, depth=0, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()
    if depth > MAX_DEPTH or url in visited_urls:
        return {}
    visited_urls.add(url)

    try:
        # session = requests.Session()
        # session.headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        #     "Accept-Encoding": "*",
        #     "Connection": "keep-alive"
        # }
        # response = session.get(url)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tags_to_scrape = ['p']  # more tags "div" & "span"
            scraped_data = {
                "url": url,
                "content": {}
            }

            for tag_name in tags_to_scrape:
                tag_elements = soup.find_all(tag_name)
                tag_texts = [element.get_text(strip=True)
                             for element in tag_elements]
                if tag_texts:
                    scraped_data["content"][tag_name] = tag_texts
            link_elements = soup.find_all('a', href=True)
            links_to_visit = [urljoin(url, element['href'])
                              for element in link_elements]

            for link in links_to_visit:
                link_data = scrape_website(link, depth + 1, visited_urls)
                if link_data:
                    # Merge the scraped data from the current link into the main dictionary
                    for tag_name, tag_texts in link_data["content"].items():
                        scraped_data["content"].setdefault(
                            tag_name, []).extend(tag_texts)

            return scraped_data

        else:
            pass
            # print(f"Error {response.status_code} occurred.")

    except requests.exceptions.InvalidSchema:
        pass
        # print(f"Invalid URL: {url}")


website_urls = hospital_list()
hospitalData = []

for i, website_url in enumerate(website_urls):
    try:
        # Scrape the website
        print(f'scrapping {i}. {website_url}')
        data = scrape_website(website_url)
        hospitalData.append(data)
    except:
        print('error occured at {i} {website_url}')
        with open(f"backup_scraped_data.json", "w") as file:
            json.dump(hospitalData, file, indent=4)
            print('Saved Backup Json File!!!!!!')

# Save the formatted data to a JSON file
with open("scraped_data.json", "w") as file:
    json.dump(hospitalData, file, indent=4)
    print('Saved Json File!!!!!!')
