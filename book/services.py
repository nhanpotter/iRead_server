import requests, random
from lxml import html

from .models import Book, Genre

DATA_API = 'https://data.gov.sg/api/action/datastore_search?resource_id=835e630b-a03f-4f77-baa6-9c69c91883f2'

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def get_downloadable_resource_page(resource_url):
    """
    Get downloadable URL for the book
    """
    page = requests.get(resource_url)
    tree = html.fromstring(page.content)
    download = tree.xpath('//a[@title="Download now"]/@href')
    download_url = 'https:' + download[0]
    if is_downloadable(download_url):
        print("Success")
        return download_url
    else:
        print("Fail")
        return ""

def refine_book_data(record):
    """
    Refine all data necessary for the book
    """
    resource_url = record['resource_url']
    record['resource_url'] = get_downloadable_resource_page(resource_url)
    record['item_format'] = record.pop('format')
    record['item_copyright'] = record.pop('copyright')
    record['id'] = record.pop('_id')

    # Genre
    genre_list = Genre.objects.all()
    record['genre'] = random.choice(genre_list)

    return record
    


def get_book_data():
    """
    Get raw book data from api
    """
    get_request = requests.get(DATA_API)
    get_data = get_request.json()
    if not get_data['success']:
        print("Fail to get api data")
        return

    records = get_data['result']['records']
    for record in records:
        record = refine_book_data(record)
        Book.objects.create(**record)
        