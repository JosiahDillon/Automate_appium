from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from time import sleep
import random
import string
import pyotp
####################################################

qr_code_hash = "lruzgenpayp55icmf6dypdcw"
stripe_email = "pottercarlos068@gmail.com"
stripe_password = "P!_kMPz?zV-KN2^"

##############################################################
def waitInfinite(callback, debug = False):
    sleep(0.3)
    yet = True
    while yet:
        try:
            callback()
            yet = False
        except NoSuchElementException:
            pass
        except JavascriptException: 
            pass
        except StaleElementReferenceException:
            pass
############################################################

def real_click_button(driver, button_name):
    sleep(2)
    print("click_button function calling...", button_name, " selected")
    buttons = driver.find_elements(By.XPATH, "//button")
    select_button = None
    for button in buttons:
        if button_name == button.text:
            select_button = button
    print('select_button,    ', select_button)
    if select_button is not None:
        select_button.click()

########################################################

def click_button(driver, button_name):
    waitInfinite(lambda: real_click_button(driver, button_name))

    
########################################################

def stripe_auth(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    web_driver = webdriver.Chrome(options=chrome_options)

    waitInfinite(lambda: web_driver.get(url))
    web_driver.find_element(By.ID, "email").send_keys(stripe_email)
    click_button(web_driver, "Continue")
    web_driver.find_element(By.ID, "password").send_keys(stripe_password)
    click_button(web_driver, "Log in")
    totp = pyotp.TOTP(qr_code_hash)
    otp = totp.now()
    web_driver.find_element(By.CSS_SELECTOR, 'input[type="tel"]').send_keys(otp)
    click_button(web_driver, "Connect")