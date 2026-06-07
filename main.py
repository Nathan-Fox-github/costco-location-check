from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def get_job_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        Stealth().apply_stealth_sync(page)
        page.goto("https://careers.costco.com/jobs?page=1&locations=CYPRESS,Texas,United%20States&limit=100&keywords=Pharmacy%20Technician")
        page.wait_for_selector(".mat-accordion", timeout=10000)
        count = page.locator(".mat-accordion .mat-expansion-panel").count()
        browser.close()

    return count

if __name__ == "__main__":
    job_count = get_job_count()
    with open("previous_job_count.txt", "r") as f:
        previous_job_count = int(f.read().strip())
    
    if job_count == previous_job_count:
        print("No new job postings.")
    else:
        print("New job postings found!")
        with open("previous_job_count.txt", "w") as f:
            f.write(str(job_count))