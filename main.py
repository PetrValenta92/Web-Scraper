"""
This small app allows to user to download articles from websites and save the link, header and fulltext.
"""

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv
import sys


def main():
    # This part need to be changed for every different website
    starting_url = "https://www.smartprague.eu/aktuality"
    link_selector = "a.tile"
    header_selector = ".jumbotron h1" # names of the class and the tag
    fulltext_selector = ".col-lg-10 p"
    output_path = "TestFile.csv"

    if output_path:
        print("Data will be saved to", output_path)
    else:
        print("Data will be printed but not saved!")

    lst_for_analyze, data_lst = [], []

    links = find_links(starting_url, link_selector)
    links = links[:5]  # You can choose how many articles you want to download
    for url in links:
        output_from_site = {}
        html = download_html(url)
        if fulltext_selector:
            fulltext = find_by_selector(html, fulltext_selector)
        else:
            fulltext = None  # No fulltext_selector means No data
        header = find_by_selector(html, header_selector)
        data_lst.append(dict(url=url, header=header, fulltext=fulltext))
        lst_for_analyze.append((header, fulltext))

    print(data_lst)
    print("Data will be saved to", output_path)
    save_to_file(data_lst, output_path)

    print("DONE!")
    return 0


def download_html(starting_url):
    r = requests.get(starting_url)
    if r.status_code != 200:
        raise RuntimeError(f"The link {starting_url} returned status {r.status_code}")
    html = r.text
    return html


def find_links(starting_url, link_selector):
    html = download_html(starting_url)
    soup = BeautifulSoup(html, "html.parser")
    link_selector_lst = [urljoin(starting_url, a_elem["href"]) for a_elem in soup.select(link_selector)]
    return link_selector_lst


def find_by_selector(html, fulltext_selector) -> str:
    soup = BeautifulSoup(html, "html.parser")
    found_text = [elem.text for elem in soup.select(fulltext_selector)]
    return " ".join(found_text)


def save_to_file(data_lst, output_path):
    fieldnames = ["url", "header", "fulltext"]

    with open(output_path, "wt", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames, delimiter=";")
        writer.writeheader()
        for row_dict in data_lst:
            writer.writerow(row_dict)

    return writer


if __name__ == '__main__':
    sys.exit(main())
