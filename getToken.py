from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import re
from Stripe_connection import stripe_auth


# Appium server
server = 'http://127.0.0.1:4723/wd/hub'

# Set up Appium capabilities for your device or emulator
desired_caps = {
    "platformName": "Android",
    "platformVersion": "12",
    "deviceName": "cloud",
    "appPackage": "org.telegram.messenger",
    "appActivity": "org.telegram.messenger.DefaultIcon",
    "noReset": True
}

local_test = {
    "platformName": "Android",
    "platformVersion": "13",
    "deviceName": "android33",
    "appPackage": "org.telegram.messenger",
    "appActivity": "org.telegram.messenger.DefaultIcon",
    "noReset": True
}

qr_code_hash = "lruzgenpayp55icmf6dypdcw"
stripe_email = "pottercarlos068@gmail.com"
stripe_password = "P!_kMPz?zV-KN2^"


def generate_bot_name():
    # Set the length of the random character part of the name
    name_length = 8
    
    # Generate a random string of characters
    random_chars = ''.join(random.choices(string.ascii_letters, k=name_length))
    
    # Generate a random number
    number = random.randint(0, 999)
    
    # Combine the random characters and number to form the bot name
    bot_name = random_chars + str(number)
    
    return bot_name


def get_message(driver, command):
    cmd = driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.EditText')))
    cmd.send_keys(command)
    
    send = driver.until(EC.visibility_of_element_located((By.XPATH, '//android.view.View[@content-desc="Send"]')))
    send.click()
    
    msg = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    
    return msg[-1].text


def click_button(driver, name):
    groups = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    ct_group = len(groups)
    buttons = driver.until(EC.visibility_of_all_elements_located((By.XPATH, f'//android.view.ViewGroup[{ct_group}]/android.widget.Button')))
    ct_button = len(buttons)
    
    for i in range(ct_button):
        button = driver.until(EC.visibility_of_element_located((By.XPATH, f'//android.view.ViewGroup[{ct_group}]/android.widget.Button[{i+1}]')))
        if name == button.text:
            button.click()
            return True
    return False
    

def find_stripe(driver):
    groups = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    ct_group = len(groups)
    
    find = False
    while True:
        i = 1
        while True:
            i += 1
            button = driver.until(EC.visibility_of_element_located((By.XPATH, f'//android.view.ViewGroup[{ct_group}]/android.widget.Button[{i}]')))
            if 'stripe' in button.text.lower():
                button.click()
                find = True
                break
            elif chr(187)[::-1] == button.text:
                button.click()
                break
        if find: break
    
def extractToken(message):
    match = re.search(r"HTTP API:\n(.+)", message)
    if match:
        http_api_section = match.group(1)
        return http_api_section
    else:
        print('no token')
 
 
def extractAuthUrl(link):
    url = re.search(r"https?://([^\s]+)", link).group(0)
    return url[:-1]
        
def create_bot(bot_name):
    android_driver = webdriver.Remote(server, desired_caps)
    driver = WebDriverWait(android_driver, 20)
    
    # create BotFather Room
    search = driver.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.ImageButton[@content-desc="Search"]/android.widget.ImageView')))
    search.click()
    
    name = driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.EditText')))
    name.send_keys('@BotFather')
    
    group = driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    group.click()
    
    # start = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.TextView')))
    # start[-1].click()
    
    msg = get_message(driver, '/newbot')
    if ('Alright, a new bot. How are we going to call it? Please choose a name for your bot.' in msg):
        
        get_message(driver, bot_name)
        key = get_message(driver, f'{bot_name}_bot')
        bot_token = extractToken(key)
        print(bot_token)
        
        get_message(driver, '/mybots')
        
        click_button(driver, f'@{bot_name}')
        click_button(driver, 'Payments')
        find_stripe(driver)
        
        click_button(driver, 'Connect Stripe Live')
        click_button(driver, 'Authorize')
        
        auth_url = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.TextView')))
        url = extractAuthUrl(auth_url[1].text)
        
        stripe_auth(url)
        
        # Payment Provider
        group = driver.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.view.ViewGroup')))
        pattern = r"Stripe Live:\s(\d+):LIVE:(\w+)"
        matches = re.search(pattern, group[-1].text)
        payment_provider = matches.group(0)[13:]
        
        return bot_token, payment_provider
    elif "Sorry, too many attempts" in msg:
        return False
    
    android_driver.quit()

if __name__ == '__main__':
    desired_caps = local_test
    create_bot('jflklke')