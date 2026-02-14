import requests
import json
import time

APP_ID = "644761c2"
APP_KEY = "4e4149cfe2beee79d8557f57c5744cc9"

headers = {
    "Accept": "application/json"
}

user_input = int(input("Enter How Many Pages: "))

all_jobs = []

for page in range(1, user_input):  # test first 5 pages
    print(f"[>] Fetching page {page}")

    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

    params = {
        "app_id": APP_ID.strip(),
        "app_key": APP_KEY.strip(),
        "what": "care",
        "results_per_page": 20
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
        all_jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "redirect_url": job.get("redirect_url")
        })

    time.sleep(0.5)

with open("uk_care_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)

print(f"[x] Saved {len(all_jobs)} jobs")
