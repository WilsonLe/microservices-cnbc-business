import json
import re
from os import getenv

import psycopg2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

"""Scrape business article link from cnbc 
    """


def main(event, context) -> list[str]:
    load_dotenv()
    soup = BeautifulSoup(requests.get(
        'https://www.cnbc.com/business/').text, 'html.parser')

    # extract article links
    articleLinks = [link.get('href') for link in soup.find_all('a') if bool(
        re.search(r'^https://www.cnbc.com/\d{4}/\d{2}/\d{2}', link.get('href')))]

    # de-dup article links
    articleLinks = [uniqueLink for uniqueLink in set(articleLinks)]

    # connect to db
    conn = psycopg2.connect(
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"))

    # create cursor to execute sql commands
    cur = conn.cursor()

    sql = """
	INSERT INTO articles
        (url)
	VALUES
        (%s)
    ON CONFLICT (url) DO NOTHING
    RETURNING id
	"""

    newIds: list[int] = []

    # insert link to db
    for link in articleLinks:
        cur.execute(sql, (link, ))
        data = cur.fetchone()
        if data != None and len(data) > 0:
            newIds.append(data[0])

    conn.commit()

    cur.close()

    return newIds


if __name__ == "__main__":
    main(None, None)
