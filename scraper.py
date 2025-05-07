# -*- coding: utf-8 -*-
import requests
import asyncio
from bs4 import BeautifulSoup
import json
import datetime
import random
from headers import headers_list
from reg import email_re, phone_re, address_re

def get_random_headers():
    return random.choice(headers_list)



async def fetch_page(url):

    if not url:
        print("No URL provided")
        return None
    if not url.startswith(('http://', 'https://')):
        print("Invalid URL format")
        return None
    

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        response.encoding = response.apparent_encoding

        response.raise_for_status()
        print(f"Fetched {url} successfully, status code: {response.status_code}, page encoding: {response.encoding}" + '\n' + f'page length: {len(response.text)}, page type: {type(response.text)}' +'\n')
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
async def parse_page(html, url):
    if html is None:
        return None

    soup = await asyncio.to_thread(BeautifulSoup, html, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'

    async def extract_emails():
        emails = set()
        for match in soup.find_all(string=email_re):
            emails.update(email_re.findall(match))
        return emails

    async def extract_phones():
        phones = set()
        for match in soup.find_all(string=phone_re):
            phones.update(phone_re.findall(match))
        return phones

    async def extract_addresses():
        addresses = set()
        for match in soup.find_all(string=address_re):
            addresses.update(address_re.findall(match))
        if not addresses:
            print("No addresses found")
        else:
            return addresses

    async def extract_links():
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.add(href)
            else:
                links.add(requests.compat.urljoin(url, href))
        return links

    emails, phones, addresses, links = await asyncio.gather(
        extract_emails(),
        extract_phones(),
        extract_addresses(),
        extract_links()
    )

    all_data = {
        'title': title,
        'emails': list(emails),
        'phones': list(phones),
        'addresses': list(addresses),
        'links': list(links)
    }
    return all_data

async def create_output_json_file(data, filename=f'output.json'):
    if data is None:
        print("No data to write")
        return

    output_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "title": data['title'],
        "emails": data['emails'],
        "phones": data['phones'],
        "addresses": data['addresses'],
        "links": data['links']
    }

    json_data = json.dumps(output_data, indent=4, ensure_ascii=False)

    if not filename.endswith('.json'):
        filename += '.json'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_data)

    print(f"Data written to {filename}")



async def create_output_file(data, filename='output.txt', encoding='utf-8'):
    if data is None:
        print("No data to write")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')

        f.write(f"Title: {data['title']}\n")

        f.write("Emails:\n")

        for email in data['emails']:
            f.write(f"{email}\n")
        f.write("Phones:\n")
        for phone in data['phones']:
            f.write(f"{phone}\n")
        f.write("Addresses:\n")
        for address in data['addresses']:
            f.write(f"{address}\n")
        f.write("Links:\n")
        for link in data['links']:
            f.write(f"{link}\n")

        print(f"Data written to {filename}")

async def main():
    try:
        url = 'https://en.wikipedia.org/wiki/Canada'
        html = await fetch_page(url)
        data = await parse_page(html, url)

        await create_output_file(data, 'output.txt')
        print("Data extraction complete.")
        print(data)

    except Exception as e:
        print(f"An error occurred: {e} \t in main()")
        return None  
      
    #await create_output_json_file(data, 'output.json')
  

if __name__ == '__main__':
    asyncio.run(main())