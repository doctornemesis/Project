import random
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --- Config ---
URL = "https://forms.cloud.microsoft/pages/responsepage.aspx?id=WNzgmUucIEiGFwTDhsJUxnD8T4ogIYhFoPdqNRKar-VUNERXQ1JPSFBRVEE4OVFMTUlCVEtVTEdLSy4u&route=shorturl"
MIN_DELAY = 3 * 60  # minimum 3 minutes
MAX_DELAY = 5 * 60  # maximum 5 minutes

# --- Browser setup ---
chrome_options = Options()
if os.getenv("GITHUB_ACTIONS") == "true":  # headless in GitHub Actions
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
wait = WebDriverWait(driver, 20)

# --- Click Next ---
next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
print("Found Next button, clicking...")
next_btn.click()
time.sleep(random.uniform(2, 4))

# --- Randomly fill radio groups ---
radio_groups = {}
all_radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
for radio in all_radios:
    name = radio.get_attribute("name")
    if name not in radio_groups and random.random() < 0.9:  # 90% chance to select
        driver.execute_script("arguments[0].click();", radio)
        radio_groups[name] = True
        time.sleep(random.uniform(1, 3))

print(f"Selected {len(radio_groups)} radio groups.")

# --- Randomly fill checkboxes ---
checkbox_groups = {}
all_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
for checkbox in all_checkboxes:
    name = checkbox.get_attribute("name")
    if name not in checkbox_groups:
        checkbox_groups[name] = []
    # 30% chance each checkbox is clicked
    if random.random() < 0.3:
        driver.execute_script("arguments[0].click();", checkbox)
        checkbox_groups[name].append(checkbox)

filled_check_groups = sum(1 for v in checkbox_groups.values() if v)
print(f"Selected {filled_check_groups} checkbox groups.")

# --- Human-like delay ---
delay = random.randint(MIN_DELAY, MAX_DELAY)
print(f"Pretending to think... waiting {delay} seconds.")
time.sleep(delay)

# --- Submit form ---
submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
time.sleep(1)
driver.execute_script("arguments[0].click();", submit_btn)
print("Form submitted!")

# Keep browser open locally
if os.getenv("GITHUB_ACTIONS") != "true":
    print("Browser will remain open. Close it manually when done.")
else:
    driver.quit()
