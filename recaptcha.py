import sys
import os
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from SetUpDriver import SetUpDriver
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
load_dotenv()
api_key = os.getenv("APIKEY_2CAPTCHA")
logger.info(f"api_key is {api_key}")

solver = TwoCaptcha(api_key)
URL = 'https://2captcha.com/demo/recaptcha-v3'
setup_driver = SetUpDriver()
driver = setup_driver.get_driver()
driver.get(URL)
try:
    result = solver.recaptcha(
        sitekey='6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu',
        url=URL,
        version='v3',
        action='demo_action',
        score=0.9
    )

except Exception as e:
    sys.exit(e)

else:
    logger.info('solved: ' + str(result))
time.sleep(7)
submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
submit_btn.click()
time.sleep(100)


