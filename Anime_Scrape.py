from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import psycopg2

url = "https://myanimelist.net/recommendations.php?s=recentrecs&t=anime"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

# to ensure that the page is loaded
time.sleep(5)

html = driver.page_source

# this renders the JS code and stores all of the information in static HTML code.
soup = BeautifulSoup(html, "html.parser")


def insert_Data():
    anime_Comparisons = soup.find_all('div', {'class': 'borderClass'})
    count = 0

    conn = psycopg2.connect(
        host="hostname",
        database="database",
        user="user",
        password="password"
    )

    cur = conn.cursor()

    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print(db_version)

    # Enter data into database
    for anime_Comparison in anime_Comparisons:
        description = anime_Comparison.find('div', {'class': 'recommendations-user-recs-text'})
        table = anime_Comparison.find('table')
        titles = table.find_all('strong')

        firstAnime = titles[0].text
        secondAnime = titles[1].text
        animeDescription = description.text

        try:
            cur.execute("INSERT INTO anime (first_anime, second_anime, anime_descr) VALUES(%s, %s, %s)",
                        (firstAnime, secondAnime, animeDescription))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        count += 1

    print("Total Recommendations =", count)


insert_Data()
