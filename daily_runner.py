import subprocess, random, time, datetime

RUNS_PER_DAY = random.randint(15, 20)
SCRIPT = "auto_form_cloud.py"

def run_once():
    print(f"[{datetime.datetime.now()}] Starting form submission...")
    try:
        subprocess.run(["python", SCRIPT], check=True)
        print(f"[{datetime.datetime.now()}] Run complete.\n")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.datetime.now()}] Run failed: {e}. Retrying in 5 min...")
        time.sleep(300)
        run_once()

# Spread runs evenly across the day
interval = (24 * 3600) / RUNS_PER_DAY

for i in range(RUNS_PER_DAY):
    run_once()
    # Wait a random time near the interval (±30%)
    wait_time = interval * random.uniform(0.7, 1.3)
    print(f"Next run in {wait_time / 60:.1f} minutes.")
    time.sleep(wait_time)
