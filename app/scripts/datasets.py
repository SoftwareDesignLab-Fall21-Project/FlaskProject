import urllib3
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()

""" 
This is a utility for scraping the list of available datasets on physionet.org." 
If you want to generate a new dataset json, run this file directly.
This file should never be used for handling requests, it is very slow and intensive.
"""


def sizeof_fmt(num, suffix="B"):
    """Generates human readable size string for a given number of bytes.
    Taken from: https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_dataset_file(content_href):
    """Helper function that gets the zip file link and size for a given dataset."""
    file_url = ''.join(["https://physionet.org/static/published-projects", content_href[8:]])
    file_response = http.request('GET', file_url)
    soup = BeautifulSoup(file_response.data, 'html.parser')
    pre = soup.find("pre")
    for element in pre.find_all('a'):
        href = element['href']
        if href[-3:] == "zip":
            data = element.nextSibling
            sp = data.split(" ")
            byte_size = int(sp[-1])
            byte_size_human = sizeof_fmt(byte_size)
            return file_url + href, byte_size, byte_size_human
    return None


def dump_dataset_json():
    """ Scrapes the list of available datasets from physionet.org and creates a static dataset json file."""
    print("Generating a new dataset json file...")
    about_response = http.request('GET', 'https://physionet.org/about/database/')
    soup = BeautifulSoup(about_response.data, 'html.parser')
    item = soup.find('div', class_="main-content")
    item2 = item.find("h2", id="open").find_next_sibling()

    datasets = {"datasets": []}
    for child in item2.find_all("li"):
        a_href = child.contents[0]
        href = a_href['href']
        title = a_href.contents[0]
        description = child.contents[1].strip(':\n ')
        dataset_file = get_dataset_file(href)
        if dataset_file is not None:
            datasets["datasets"].append(
                {"file_url": dataset_file[0], "file_size": dataset_file[1], "file_size_human": dataset_file[2],
                 "title": title, "description": description})
        # print(child)
    json_obj = json.dumps(datasets)
    with open("../static/datasets/dump.json", 'w', encoding='utf-8') as f:
        f.write(json_obj)
    print("Done!")


if __name__ == "__main__":
    dump_dataset_json()

