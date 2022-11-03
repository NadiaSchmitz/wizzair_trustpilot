from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time

# URL
url = 'https://de.trustpilot.com/review/www.wizzair.com'
print("URL: ", url)

print("Anfang: ", time.ctime())

# Response
url_response = requests.get(url)
browser = webdriver.Chrome()
print("SELENIUM: Ich habe Chrome geöffnet.")
browser.get(url)
browser.maximize_window()
print("SELENIUM: Ich habe das Fenster maximiert.")

try:
    cookies_button = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    if cookies_button:
        cookies_button.click()
        print("SELENIUM: Ich habe cookies erlaubt.")
    else:
        print("Es gibt keine cookies_button.")
    time.sleep(3)
except:
    print("Cookies. Daten können nicht geparst werden.")

browser.execute_script("window.scrollTo(0, 500);")
print("SELENIUM: Ich habe die Seite um 500px gescrollt.")
time.sleep(3)

try:
    filter_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[3]/button/span/p')
    if filter_button:
        filter_button.click()
        print("SELENIUM: Ich habe Filter geklickt.")
    else:
        print("Es gibt keine filter_button.")
    time.sleep(3)
except:
    print("Filter. Daten können nicht geparst werden.")

try:
    lang_input = browser.find_element(By.XPATH, '//*[@id="language-option-all"]')
    if lang_input:
        lang_input.click()
        print("SELENIUM: Ich habe alle Sprachen ausgewählt.")
    else:
        print("Es gibt keinen lang_input.")
    time.sleep(3)
except:
    print("Language Auswahl. Daten können nicht geparst werden.")

try:
    filter_confirm_button = browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[3]/div/button[2]')
    if filter_confirm_button:
        filter_confirm_button.click()
        print("SELENIUM: Ich habe meine Auswahl bestätigt.")
    else:
        print("Es gibt keine filter_confirm_button.")
    time.sleep(3)
except:
    print("Filter Bestätigung. Daten können nicht geparst werden.")

# URL aktuell ermitteln
url_actual = browser.current_url
print("BS4: Ich habe URL aktualisiert.")
print("URL: ", url_actual)

# Response
url_response_actual = requests.get(url_actual)

# Soup erstellen
url_soup = BeautifulSoup(url_response_actual.text, "lxml")

# Anzahl der Seiten ermitteln
page_number = int(url_soup.find('a', attrs={'name': 'pagination-button-last'}).find('span').text)
print("BS4: Ich habe die Anzahl der Seiten festgestellt.", page_number)

reviews_data = []
page = 1

try:
    url = url_actual
    while page <= page_number:
        url_response_actual = requests.get(url)
        time.sleep(3)
        url_soup = BeautifulSoup(url_response_actual.text, "lxml")
        reviews = url_soup.findAll('div', class_='styles_cardWrapper__LcCPA')
        print("Die Seite ", page, " aus ", page_number, " wird bearbeitet.")
        print("URL: ", url)
        for review in reviews:
            country = review.find('div', 'typography_body-m__xgxZ_').find('span').text
            rating = int(review.find('div', class_='styles_reviewHeader__iU9Px').attrs['data-service-review-rating'])
            date_review = review.find('p', class_='typography_body-m__xgxZ_').text
            review_title = review.find('h2').text
            reviews_data.append([country, rating, date_review, review_title])
        page = page + 1
        url = url_actual + '&page=' + str(page)
except:
    print("Parsing war nicht erfolgreich")

header_csv = ['country', 'rating', 'date_review', 'review_title']

df = pd.DataFrame(reviews_data, columns=header_csv)
df.to_csv('/Users/nadii/Desktop/Daten/trustpilot_wizzair/wizzair.csv', sep=';')

print("Parsing war erfolgreich. Die Daten wurden gespeichert und sind verfügbar: ")
print("C:/Users/nadii/Desktop/Daten/trustpilot_wizzair/wizzair.csv")

print("Ende: ", time.ctime())
