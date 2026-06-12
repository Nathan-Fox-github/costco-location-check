from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth # type: ignore
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_job_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        Stealth().apply_stealth_sync(page)
        page.goto(f"{os.getenv('URL')}", timeout=60000)
        page.wait_for_selector(f"{os.getenv('CONTAINER')}", timeout=10000)
        count = page.locator(f"{os.getenv('CONTAINER')} {os.getenv('LIST_ITEM')}").count()
        browser.close()

    return count

def send_notif(message: str) -> None:
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    if not webhook_url:
        print("Webhook URL not found in environment variables.")
        return

    requests.post(webhook_url, json={"content": message})

if __name__ == "__main__":
    job_count = get_job_count()
    with open("previous_job_count.txt", "r") as f:
        previous_job_count = int(f.read().strip())
    
    if job_count == previous_job_count:
        send_notif("No new job postings.")
    else:
        send_notif(f"<@{os.getenv('DISCORD_USER_ID')}> New job postings found at {os.getenv('URL')}!")
        with open("previous_job_count.txt", "w") as f:
            f.write(str(job_count))