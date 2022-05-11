import imp
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd


def getAllData(url, tempArray=[]):
    dataArr = tempArray

    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    rows = soup.select('tr')
    for row in rows:
        if row.select('a.text-blue') != []:
            dataArr.append({
                'Nama Dosen': row.select('a.text-blue')[0].get_text(),
                'NIDN': row.select('dd:nth-child(3)')[0].get_text().replace('NIDN /NIP/NIDK : ', ''),
                '3 Years Score': row.select('td:nth-child(2) > div:nth-child(1)')[0].get_text(),
                'All Years Score': row.select('td:nth-child(3) > div:nth-child(1)')[0].get_text()
            })
    try:
        baseUrl = 'https://sinta.kemdikbud.go.id/affiliations/detail'
        pathurl = soup.select(
            'ul.uk-pagination.uk-align-right.top-paging > li:nth-child(8) a')[0].get('href')
        urllengkap = f'{baseUrl}{pathurl}'
        return getAllData(urllengkap, dataArr)
    except:
        return dataArr


base_url = 'https://sinta.kemdikbud.go.id'
html_doc = requests.get(
    'https://sinta.kemdikbud.go.id/affiliations/detail?id=2042&view=overview')
soup = BeautifulSoup(html_doc.text, 'html.parser')

targetLinkAuthor = soup.select('a.hvr-grow')[2].get('href')

linkAuthor = f'{base_url}{targetLinkAuthor}'

json_object = json.dumps(getAllData(linkAuthor), indent=4)

# Writing to sample.json
with open("Output Scrapping Sinta Ubhara.json", "a") as outfile:
    outfile.write(json_object)

# json to csv
df = pd.read_json(r'D:\coding\Output Scrapping Sinta Ubhara.json')
df.to_csv(r'D:\coding\Output Scrapping Sinta Ubhara.csv', index=False)
