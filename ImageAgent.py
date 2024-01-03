from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fastapi import Response
import httpx
import uuid
import os

options = Options()
options.headless = False
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36")

driver = webdriver.Chrome(options=options)

driver.get("https://sdxlturbo.ai/")

element = driver.find_element(By.NAME, "prompt")

IMAGE_DIR = f'C:/Users/iaff_admin/Documents/GitHub/ZPI_VAF/iaff_front/build/generated/'

os.makedirs(IMAGE_DIR, exist_ok=True)

async def download_image(image_url):    
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)

        if response.status_code != 200:
            return Response(content="Failed to fetch the image", status_code=response.status_code)

        file_id = str(uuid.uuid4())
        file_path = os.path.join(IMAGE_DIR, f"{file_id}.png")

        with open(file_path, "wb") as file:
            file.write(response.content)
        
        return f"{file_id}.png"

async def generate(prompt):
    element.clear()    
    element.send_keys(prompt)
    time.sleep(4)
    try:
        image_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//img[@alt="Generated"]'))
        )        
        image = driver.find_element(By.CSS_SELECTOR, 'img[alt="Generated"]')
        src_value = image.get_attribute('src')
        content = await download_image(src_value)
        return {"function": "generate_image", 
                "source": content or ""}
    except Exception:
        print("Image not found in the given time.")