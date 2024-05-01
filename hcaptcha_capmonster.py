import os
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import HcaptchaProxylessRequest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

API_KEY = os.getenv('APIKEY_CAPMONSTER')
WEBSITE_KEY = 'a5f74b19-9e45-40e0-b45d-47ff91b7a6c2'
WEBSITE_URL = 'https://accounts.hcaptcha.com/demo'
# WEBSITE_KEY = 'f7de0da3-3303-44e8-ab48-fa32ff8ccc7b'
# WEBSITE_URL = 'https://2captcha.com/demo/hcaptcha'


async def solve_hcaptcha():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Браузер инициализирован!")

        # Переход на веб-сайт с hCaptcha
        browser.get(WEBSITE_URL)
        print("Переключение браузера на страницу с капчей!")

        # Инициализация клиента CapMonster
        client_options = ClientOptions(api_key=API_KEY)
        cap_monster_client = CapMonsterClient(options=client_options)
        print("Клиент CapMonster инициализирован!")

        # Создание запроса для решения hCaptcha
        hcaptcha_request = HcaptchaProxylessRequest(
            websiteUrl=WEBSITE_URL,
            websiteKey=WEBSITE_KEY,
            fallbackToActualUA=True
        )

        # Решение hCaptcha с использованием CapMonster
        task_result = await cap_monster_client.solve_captcha(hcaptcha_request)
        solution = task_result.get('gRecaptchaResponse')
        print("hCaptcha решена!")

        # Вставка решения в форму
        element = browser.find_element(By.NAME, 'h-captcha-response')
        browser.execute_script('arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";', element)
        browser.execute_script(f'arguments[0].value = "{solution}";', element)
        print("Результат вставлен на страницу!")

        # Нажатие кнопки отправки
        submit_button = browser.find_element(By.ID, 'hcaptcha-demo-submit')
        submit_button.click()
        print("Нажата кнопка 'hcaptcha-demo-submit'!")

        # Пауза на 10 секунд
        await asyncio.sleep(10)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрытие браузера
        browser.quit()

# Запуск асинхронной функции для решения hCaptcha
asyncio.run(solve_hcaptcha())