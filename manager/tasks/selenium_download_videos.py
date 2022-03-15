import os
import time

import openpyxl

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from audiowolf.settings import SPREADSHEET_FILE, YT2MATE_URL, BASE_DIR


class SeleniumDownloadVideos:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def build():
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        preferences = {"download.default_directory": os.path.join(BASE_DIR, "media", "downloaded")}
        options.add_experimental_option('prefs', preferences)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver: WebDriver = webdriver.Chrome(service=service, options=options)
        return SeleniumDownloadVideos(driver)

    @staticmethod
    def read_spreadsheet():
        wb = openpyxl.load_workbook(SPREADSHEET_FILE)
        ws = wb.active

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                continue
            official_yt_link = row[7]
            name = row[6]
            brand = row[1]
            if official_yt_link:
                yield official_yt_link, name, brand, row[0]
                continue

    def search_for_video(self, link):
        self.driver.get(YT2MATE_URL)
        search_field = self.driver.find_element(by=By.ID, value='txtUrl')
        search_field.send_keys(link)
        submit: WebElement = self.driver.find_element(by=By.ID, value='btnSubmit')
        submit.click()
        time.sleep(5)

    def rename_file(self, ad_id):
        filename = max([f for f in os.listdir(os.path.join(BASE_DIR, "media", "downloaded"))])
        os.rename(os.path.join(BASE_DIR, "media", "downloaded", filename), os.path.join(BASE_DIR, "media", "downloaded", str(ad_id) + '.mp4'))

    def process_and_download_video(self, link, ad_id):
        self.search_for_video(link)
        try:
            video_table: WebElement = self.driver.find_element(by=By.CLASS_NAME, value='tableVideo')
            video_table_rows = video_table.find_elements(by=By.TAG_NAME, value='tr')
            download_button = video_table_rows[1].find_element(by=By.TAG_NAME, value='button')
            button_id = download_button.find_element(by=By.XPATH, value='..').get_attribute('id')
            download_button.click()
            time.sleep(5)
            video_url = self.driver.find_element(by=By.ID, value=button_id).find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            self.driver.get(video_url)
            time.sleep(5)
            self.rename_file(ad_id)
        except NoSuchElementException:
            error = self.driver.find_element(by=By.ID, value='error')
            if error:
                return
            time.sleep(5)
            self.process_and_download_video(link, ad_id)

    def download_video(self):
        links = self.read_spreadsheet()
        for link, name, brand_name, ad_id in links:
            video_filename = self.process_and_download_video(link, ad_id)
            if video_filename:
                pass


if __name__ == '__main__':
    download = SeleniumDownloadVideos.build()
    download.download_video()
