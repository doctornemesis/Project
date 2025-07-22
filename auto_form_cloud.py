from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)

driver.get("https://forms.cloud.microsoft/pages/responsepage.aspx?id=WNzgmUucIEiGFwTDhsJUxnD8T4ogIYhFoPdqNRKar-VUNERXQ1JPSFBRVEE4OVFMTUlCVEtVTEdLSy4u&route=shorturl")
wait = WebDriverWait(driver, 20)

# Step 1: Click Next
next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
print("Found Next button, clicking...")
next_btn.click()

# Simulate thinking time before answering
time.sleep(random.randint(5, 15))

# Step 2: Randomly fill radio buttons
radio_groups = {}
all_radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
for radio in all_radios:
    name = radio.get_attribute("name")
    if name not in radio_groups:
        if random.choice([True, False]):  # 50% chance to pick a radio group
            driver.execute_script("arguments[0].click();", radio)
            radio_groups[name] = True
            time.sleep(random.uniform(0.5, 2))  # delay between clicks

# Step 3: Randomly fill checkboxes
checkbox_groups = {}
all_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
for checkbox in all_checkboxes:
    name = checkbox.get_attribute("name")
    if name not in checkbox_groups:
        group_checkboxes = driver.find_elements(By.XPATH, f"//input[@type='checkbox' and @name='{name}']")
        selected = random.sample(group_checkboxes, random.randint(1, min(2, len(group_checkboxes))))  # 1-2 random selections
        for cb in selected:
            driver.execute_script("arguments[0].click();", cb)
            time.sleep(random.uniform(0.5, 1.5))
        checkbox_groups[name] = True

print(f"Selected {len(radio_groups)} radio groups and {len(checkbox_groups)} checkbox groups.")

# Simulate more time (to get 3–5 min total)
remaining_time = random.randint(180, 300) - (len(radio_groups) + len(checkbox_groups)) * 2
if remaining_time > 0:
    print(f"Simulating user review for {remaining_time} seconds...")
    time.sleep(remaining_time)

# Step 4: Submit form
submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
time.sleep(1)
driver.execute_script("arguments[0].click();", submit_btn)
print("Form submitted! Browser will remain open.")
