from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from socket_manager import sio
import asyncio

service = Service(f"C:/Users/iaff_admin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
options = Options()
options.headless = False
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://sdxlturbo.ai/")

element = driver.find_element(By.NAME, "prompt")

async def generate(prompt, sid):
    await asyncio.sleep(1.5) 
    await sio.emit('get_response_info', "Generating", room=sid)        

    element.clear()    
    element.send_keys(prompt)
    await asyncio.sleep(4) 
    try:
        image_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//img[@alt="Generated"]'))
        )        
        image = driver.find_element(By.CSS_SELECTOR, 'img[alt="Generated"]')
        src_value = image.get_attribute('src')
        return {"function": "generate_image", 
                "source": src_value or ""}
    except Exception:
        print("Image not found in the given time.")