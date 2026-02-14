import requests
import json
import time
import re

APP_ID = "644761c2"
APP_KEY = "fff1d2d67aba26807b7e53334e7486eb"

headers = {
    "Accept": "application/json"
}

def extract_phone(text):
    if not text:
        return None

    pattern = r'(\+44\s?7\d{3}|\(?07\d{3}\)?|\+44\s?1\d{3}|\(?01\d{3}\)?)\s?\d{3}\s?\d{3}'
    match = re.search(pattern, text)
    return match.group(0) if match else None

user_input = int(input("Enter How Many Pages: "))

all_jobs = []

RECRUITMENT_KEYWORDS = [
    "consultant",
    "recruitment",
    "recruiter",
    "staffing",
    "agency",
    "talent",
    "resourcing",
    "solutions",
    "employment",
    "workforce",
    "personnel",
    "hiring",
    "search ltd",
    "careers ltd",
    "temp",
    "temporary",
]

def is_recruitment(company_name, description):
    text = f"{company_name} {description}".lower()
    for word in RECRUITMENT_KEYWORDS:
        if word in text:
            return True
    return False


for page in range(1, user_input + 1):  # include last page
    print(f"[>] Fetching page {page}")

    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

    params = {
        "app_id": APP_ID.strip(),
        "app_key": APP_KEY.strip(),
        "what": "care",
        "results_per_page": 40
    }

    response = requests.get(url, params=params, headers=headers)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        break

    data = response.json()

    if not data.get("results"):
        print("[!] No more results")
        break

    for job in data["results"]:
        description = job.get("description")
        phone = extract_phone(description)

        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        if salary_min:
            salary_min = f"£{salary_min:,}"
        if salary_max:
            salary_max = f"£{salary_max:,}"

        company_name = job.get("company", {}).get("display_name", "")
        description = job.get("description", "")

        if is_recruitment(company_name, description):
            continue

        all_jobs.append({
        "title": job.get("title"),
        "company": company_name,
        "location": job.get("location", {}).get("display_name"),
        "salary_min": salary_min,
        "salary_max": salary_max,
        "phone_number": phone,
        "redirect_url": job.get("redirect_url")
    })

        time.sleep(0.5)

with open("uk_care_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)

print(f"[x] Saved {len(all_jobs)} jobs")
