import random
import time
import csv
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FORM_URL = "https://forms.cloud.microsoft/pages/responsepage.aspx?id=WNzgmUucIEiGFwTDhsJUxnD8T4ogIYhFoPdqNRKar-VUNERXQ1JPSFBRVEE4OVFMTUlCVEtVTEdLSy4u&route=shorturl"
LOG_FILE = "submission_log.csv"

def fill_and_submit():
    driver = webdriver.Chrome()
    driver.get(FORM_URL)
    wait = WebDriverWait(driver, 20)

    try:
        # Click "Next"
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
        next_btn.click()
        time.sleep(3)

        # Random radio selection
        radio_groups = {}
        for radio in driver.find_elements(By.XPATH, "//input[@type='radio']"):
            radio_groups.setdefault(radio.get_attribute("name"), []).append(radio)
        for radios in radio_groups.values():
            driver.execute_script("arguments[0].click();", random.choice(radios))
            time.sleep(random.uniform(0.5, 1.5))

        # Random checkbox selection
        checkbox_groups = {}
        for checkbox in driver.find_elements(By.XPATH, "//input[@type='checkbox']"):
            checkbox_groups.setdefault(checkbox.get_attribute("name"), []).append(checkbox)
        for checkboxes in checkbox_groups.values():
            selected = random.sample(checkboxes, k=random.randint(1, min(3, len(checkboxes))))
            for cb in selected:
                driver.execute_script("arguments[0].click();", cb)
                time.sleep(random.uniform(0.5, 1.5))

        print(f"Selected {len(radio_groups)} radio groups and {len(checkbox_groups)} checkbox groups.")

        # Simulate human filling delay
        fill_time = random.uniform(180, 300)
        print(f"Simulating form completion for {fill_time:.1f} seconds...")
        time.sleep(fill_time)

        # Submit
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_btn)
        print("Form submitted!")

        # Log submission
        with open(LOG_FILE, "a", newline="") as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        # Keep browser open briefly
        time.sleep(random.uniform(10, 15))
        driver.quit()

    except Exception as e:
        print("Error:", e)
        driver.quit()

# Schedule new submissions for the day
def schedule_daily_submissions():
    for job in schedule.jobs:
        schedule.cancel_job(job)

    submissions_today = random.randint(15, 20)
    print(f"Scheduling {submissions_today} submissions for today.")

    for _ in range(submissions_today):
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(fill_and_submit)

# Refresh schedule at midnight
def refresh_schedule():
    print("Refreshing schedule for a new day...")
    schedule_daily_submissions()

schedule_daily_submissions()
schedule.every().day.at("00:00").do(refresh_schedule)

print("Scheduler started. Waiting for submission times...")
while True:
    schedule.run_pending()
    time.sleep(30)
