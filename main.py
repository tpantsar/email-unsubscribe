import email
import imaplib
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

queries = ['unsubscribe', 'klikkaa tästä', 'tästä', 'peru', 'opt-out', 'remove', 'stop']


def connect_to_mail(host: str):
    mail = imaplib.IMAP4_SSL(host=host)
    mail.login(username, password)
    mail.select('inbox')
    return mail


def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [
        link['href']
        for link in soup.find_all('a', href=True)
        if any(query in link.get_text(strip=True).lower() for query in queries)
    ]
    return links


def click_link(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print('Successfully visited', link)
        else:
            print('Failed to visit', link, 'error code', response.status_code)
    except Exception as e:
        print('Error with', link, str(e))


def search_for_email(search_query: str):
    mail = connect_to_mail('imap.gmail.com')
    _, search_data = mail.search(None, search_query)
    data = search_data[0].split()

    links = []

    for num in data:
        _, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode(
                        'utf-8', errors='ignore'
                    )
                    links.extend(extract_links_from_html(html_content))
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

            if content_type == 'text/html':
                links.extend(extract_links_from_html(content))

    mail.logout()
    return links


def save_links(links):
    with open('links.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(links))
    print(f'{len(links)} links saved to links.txt')


links = search_for_email('ALL')

# for link in links:
#     click_link(link)

save_links(links)
