import subprocess
import random
import time
import datetime

# How many times to run per day
RUNS_PER_DAY = random.randint(15, 20)

print(f"Planned runs for today: {RUNS_PER_DAY}")

for i in range(RUNS_PER_DAY):
    print(f"\nRun {i+1}/{RUNS_PER_DAY} - {datetime.datetime.now().strftime('%H:%M:%S')}")
    subprocess.run(["python", "auto_form_cloud.py"])
    
    # Random wait time between runs: 20 to 60 minutes
    wait_time = random.randint(20 * 60, 60 * 60)
    print(f"Waiting {wait_time // 60} minutes before next run...\n")
    time.sleep(wait_time)
