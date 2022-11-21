from bs4 import BeautifulSoup
from selenium import webdriver
import time, re
from selenium.webdriver.chrome.service import Service
import pandas


def saving_html(
    count_smart=100,
    url=r"https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating&type=49659",
):
    service = Service(executable_path=r"chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(url=url)
        time.sleep(3)
        cash_links = 0
        all_links = []
        # with open("html_files/parser_selenium.html", "w", encoding="utf-8") as file:
        #     file.write(driver.page_source)
        while cash_links < count_smart:
            [
                all_links.append(str(link))
                for link in parsing_os_smartphone(driver.page_source)
            ]
            cash_links += len(parsing_os_smartphone(driver.page_source))
            url_next = "https://www.ozon.ru" + parsing_next_list(driver.page_source)
            driver.service.stop()
            driver = webdriver.Chrome(service=service)
            driver.get(url_next)
            time.sleep(3)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return all_links


def parsing_os_smartphone(html_file):
    list_links = []
    soup = BeautifulSoup(html_file, "html.parser")
    for link in soup.find_all("a", href=True):
        if str(link["href"]).startswith("/product/smartfon"):
            list_links.append(str(link["href"]))
    return set(list_links)


def parsing_next_list(html_file):
    links = []
    soup = BeautifulSoup(html_file, "html.parser")
    for link in soup.find_all("a", {"class": re.compile(r"_4-a")}, href=True):
        links.append(link["href"])
    return str(max(links, key=len))


def pars_os_os(list_links):
    os = []
    point_link = 1
    list_links = list_links[0:30]
    service = Service(executable_path=r"chromedriver.exe")
    for links in list_links:
        try:
            driver = webdriver.Chrome(service=service)
            cash = []
            driver.get("https://www.ozon.ru" + links)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            for link in soup.find_all("dd", {"class": re.compile(r".{0,5}ly.{0,5}")}):
                cash.append(
                    str(re.search(r".*(((a|A)ndroid)|((i|I)(O|o)(S|s))).*", link.text))
                )
            os.append(max(cash, key=len)[max(cash, key=len).index("match='") + 7 : -2])
            cash.clear()
            driver.service.stop()
            point_link += 1
        except Exception as ex:
            print("Missing link")
    return os


def sorted_p(list_os):
    pand = pandas.Series(list_os)
    print(pand.value_counts())


def main():
    start_time = time.time()
    sorted_p(pars_os_os(saving_html()))
    finish_time = time.time()
    print(time.ctime(finish_time - start_time))


if __name__ == "__main__":
    main()
