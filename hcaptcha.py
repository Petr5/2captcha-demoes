import os
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
import time


def solvehCaptcha():
    api_key = os.getenv('APIKEY_2CAPTCHA')
    solver = TwoCaptcha(api_key)

    try:
        result = solver.hcaptcha(
            sitekey='f7de0da3-3303-44e8-ab48-fa32ff8ccc7b',
            url='https://2captcha.com/demo/hcaptcha',
        )

    except Exception as e:
        print(e)
        return False

    else:
        return result


browser = webdriver.Chrome()
browser.get('https://2captcha.com/demo/hcaptcha')

WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'div.h-captcha')))
# wait for iframe
WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'iframe')))

result = solvehCaptcha()

if result:
    code = result['code']
    logger.info(f"code is {code}")

    captcha = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[data-hcaptcha-response]")))

    browser.execute_script(f"arguments[0].setAttribute('data-hcaptcha-response', '{code}');", captcha)

    browser.execute_script(
        "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + code + "'")

    browser.find_element(
        By.CSS_SELECTOR, "button[type='submit'").click()
    logger.info(f"waiting is started")
    time.sleep(1000)
    browser.quit()