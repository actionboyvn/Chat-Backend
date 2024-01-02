from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

options = Options()
options.headless = False
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36")

driver = webdriver.Chrome(options=options)

driver.get("https://sdxlturbo.ai/")

element = driver.find_element(By.NAME, "prompt")

async def generate(prompt):
    element.clear()
    time.sleep(random.uniform(1, 3))
    element.send_keys(prompt)
    time.sleep(5)
    try:
        image_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//img[@alt="Generated"]'))
        )        
        image = driver.find_element(By.CSS_SELECTOR, 'img[alt="Generated"]')
        src_value = image.get_attribute('src')
        print(src_value)
        return {"function": "generate_image", 
                "source": src_value}
    except Exception:
        print("Image not found in the given time.")