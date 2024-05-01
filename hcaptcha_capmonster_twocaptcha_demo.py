from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import HcaptchaProxylessRequest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

API_KEY = os.getenv('APIKEY_CAPMONSTER')
WEBSITE_KEY = 'f7de0da3-3303-44e8-ab48-fa32ff8ccc7b'
WEBSITE_URL = 'https://2captcha.com/demo/hcaptcha?difficulty=moderate'


async def solvehCaptcha():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Браузер инициализирован!")

    browser.get(WEBSITE_URL)
    print("Переключение браузера на страницу с капчей!")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.h-captcha')))
    client_options = ClientOptions(api_key=API_KEY)
    cap_monster_client = CapMonsterClient(options=client_options)
    print("Клиент CapMonster инициализирован!")

    hcaptcha_request = HcaptchaProxylessRequest(
        websiteUrl=WEBSITE_URL,
        websiteKey=WEBSITE_KEY,
        fallbackToActualUA=True
    )

    task_result = await cap_monster_client.solve_captcha(hcaptcha_request)
    solution = task_result.get('gRecaptchaResponse')
    print("hCaptcha решена!")

    element = browser.find_element(By.NAME, 'h-captcha-response')
    browser.execute_script('arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";', element)
    browser.execute_script(f'arguments[0].value = "{solution}";', element)
    print("Результат вставлен на страницу!")

    submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()
    print("Нажата кнопка 'submit'!")

    await asyncio.sleep(10)


asyncio.run(solvehCaptcha())
