from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Open Google Images
driver.get("https://www.google.com/imghp")

# Find the upload image button and click it

upload_button = driver.find_element(By.CLASS_NAME, "Gdd5U")
driver.implicitly_wait(10)
upload_button.click()

# Upload image (replace "image_path.jpg" with the path to your image file)
#upload_input = driver.find_element(By.CSS_SELECTOR, "input[name='encoded_image']")
#upload_input.send_keys("image_path.jpg")

# Wait for search results to load
#driver.implicitly_wait(10)

# Extract search results
#search_results = driver.find_element(By.CSS_SELECTOR, "a.iKjWAf")
#for result in search_results:
#    print(result.get_attribute("href"))


# Close WebDriver
#driver.quit()