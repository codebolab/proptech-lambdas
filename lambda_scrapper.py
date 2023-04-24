import json
import boto3
import requests
import hashlib
import logging
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError
from datetime import datetime

region_name = 'us-east-1'
BUCKET = "codebolabs-lake"


class Scrapper:
    hostname = "https://clasificados.lostiempos.com"

    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

    def get_hash_id(self, *args):
        hasher = hashlib.blake2s()
        for arg in args:
            hasher.update(str(arg).encode('utf-8'))
        return hasher.hexdigest()

    def fetch(self):
        logging.info(f"  fetching")
        response = requests.get(self.url)
        response.raise_for_status()
        self.content = response.text

        now = datetime.now()
        today = now.date().isoformat()
        hash_id = self.get_hash_id(self.url, today)

        raw = {
            "url": self.url,
            "hash_id": hash_id,
            "data": self.content,
            "created": now.isoformat(),
            "date": today
        }
        raw.update(self.kwargs)

        key = f'raw/scrapped/lostiempos.com/{today}/{hash_id}.json'
        s3 = boto3.client('s3', region_name=region_name)
        try:
            s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(raw))
            logging.info(f'  s3://{BUCKET}/{key}')
            return f"s3://{BUCKET}/{key}"
        except ClientError as e:
            logging.info(f'   Error uploading data to {BUCKET}/{key}: {e}')
            return None

    def next_page(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        next_page_element = soup.find('li', class_='pager-next')

        if next_page_element:
            next_page_link = next_page_element.find('a', href=True)
            if next_page_link:
                return f"{self.hostname}{next_page_link['href']}"

        return None


class Snapshot:
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

    def __iter__(self):
        current_url = self.url
        while current_url:
            page = Scrapper(current_url, **self.kwargs)
            yield page
            current_url = page.next_page()


def lambda_handler(event, context):
    logging.info("> starting scrapping")
    url = event.get('url')

    scrapped = []
    walker = Snapshot(url)
    for page in walker:
        page.save()
        logging.info("  scrapped: %s" % page.url)
        scrapped.append(page.url)

    logging.info("< finished scrapping")
    return {
        'statusCode': 200,
        'body': json.dumps(scrapped)
    }
