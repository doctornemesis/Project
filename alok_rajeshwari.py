from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random

def human_delay(min_sec=3, max_sec=8):
    """Random pause to simulate human actions."""
    time.sleep(random.uniform(min_sec, max_sec))

driver = webdriver.Chrome()
driver.get("https://forms.cloud.microsoft/pages/responsepage.aspx?id=WNzgmUucIEiGFwTDhsJUxnD8T4ogIYhFoPdqNRKar-VUNERXQ1JPSFBRVEE4OVFMTUlCVEtVTEdLSy4u&route=shorturl")

wait = WebDriverWait(driver, 30)

# Click Next
next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
print("Found Next button, clicking...")
human_delay(5, 10)  # Wait before clicking Next
next_btn.click()

# Wait for questions to load
human_delay(5, 10)

# --- Select random radio buttons ---
radio_groups = {}
all_radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
for radio in all_radios:
    name = radio.get_attribute("name")
    if name not in radio_groups:
        radio_groups[name] = []
    radio_groups[name].append(radio)

for name, radios in radio_groups.items():
    human_delay(5, 12)  # delay per question
    selected = random.choice(radios)
    driver.execute_script("arguments[0].click();", selected)

# --- Select random checkboxes ---
checkbox_groups = {}
all_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
for checkbox in all_checkboxes:
    name = checkbox.get_attribute("name")
    if name not in checkbox_groups:
        checkbox_groups[name] = []
    checkbox_groups[name].append(checkbox)

for name, checkboxes in checkbox_groups.items():
    human_delay(5, 12)  # delay per checkbox group
    k = random.randint(1, min(3, len(checkboxes)))  # choose 1–3 randomly
    selected_boxes = random.sample(checkboxes, k)
    for checkbox in selected_boxes:
        human_delay(2, 5)
        driver.execute_script("arguments[0].click();", checkbox)

print(f"Selected {len(radio_groups)} radio groups and {len(checkbox_groups)} checkbox groups.")

# Final wait before submitting to extend total time
human_delay(10, 20)

# --- Click Submit using JS ---
submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
human_delay(3, 6)
driver.execute_script("arguments[0].click();", submit_btn)
print("Form submitted! Browser will remain open. Press Enter in terminal to close...")

input()
