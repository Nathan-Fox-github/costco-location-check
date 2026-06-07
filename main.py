from playwright.sync_api import sync_playwright

def get_job_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
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