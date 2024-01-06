from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from socket_manager import sio
import asyncio
import random

#service1 = Service(f"C:/Users/iaff_admin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
#service2 = Service(f"C:/Users/iaff_admin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

options = Options()
options.headless = False
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36")

#driver1 = webdriver.Chrome(service=service1, options=options)
#driver2 = webdriver.Chrome(service=service2, options=options)
driver1 = webdriver.Chrome(options=options)
driver2 = webdriver.Chrome(options=options)

driver1.get("https://sdxlturbo.ai/")
driver2.get("https://lexica.art/")

element1 = driver1.find_element(By.NAME, "prompt")
element2 = driver2.find_element(By.ID, "main-search")
button2 = driver2.find_element(By.ID, "main-search")

async def emit_message(sid, message):
    await sio.emit('get_response_info', message, room=sid)

async def generate(prompt, sid):
    try:
        existing_image = driver1.find_element(By.XPATH, '//img[@alt="Generated"]')
        existing_src = existing_image.get_attribute('src') if existing_image else ""
    except Exception as e:
        existing_src = ""    

    element1.clear()    
    element1.send_keys(prompt)        
    try:
        await sio.emit('get_response_info', "Generating", room=sid)    

        def found_new_image(driver):
            image = driver.find_element(By.XPATH, '//img[@alt="Generated"]')            
            if (image.get_attribute('src') != existing_src):
                return image
            return False
        
        image = WebDriverWait(driver1, 10).until(found_new_image)        
        src_value = image.get_attribute('src')
        return {"function": "generate_image", 
                "source": src_value or ""}
    except Exception:        
        await sio.emit('get_response_info', "Could not generate, try again!", room=sid)

async def find_similar(link, sid):    
    await sio.emit('get_response_info', "Finding", room=sid)

    element2.clear()    
    element2.send_keys(link)
    element2.send_keys(Keys.ENTER)    
    try:
        def found_new_images(driver):
            images = driver.find_elements(By.TAG_NAME, "img")
            return images                                    
        images = WebDriverWait(driver2, 10).until(found_new_images)
        return {"function": "find_similar_images",
                "image_links": random.sample(list(map(lambda img: img.get_attribute('src'), images)), 5)}
    except Exception:        
        await sio.emit('get_response_info', "Could not find, try again!", room=sid)