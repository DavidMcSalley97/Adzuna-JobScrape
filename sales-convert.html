import json

INPUT_FILE = input("Enter File name to convert: ")
OUTPUT_FILE = input("Enter converted file name (html format): ")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    jobs = json.load(f)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>UK Care Jobs</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
.card { background: white; padding: 15px; margin-bottom: 15px; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.card h2 { margin: 0; color: #2a2a2a; }
.card p { margin: 4px 0; }
.card a { color: #1a73e8; text-decoration: none; }
</style>
</head>
<body>
<h1>UK Care Jobs</h1>
"""

for job in jobs:
    html += f"""
<div class="card">
<h2>{job.get('title')}</h2>
<p><strong>Company:</strong> {job.get('company')}</p>
<p><strong>Location:</strong> {job.get('location')}</p>"""
    if job.get('salary_min') or job.get('salary_max'):
        html += f"<p><strong>Salary:</strong> {job.get('salary_min') or '-'} - {job.get('salary_max') or '-'}</p>"
    if job.get('phone_number'):
        html += f"<p><strong>Phone:</strong> {job.get('phone_number')}</p>"
    html += f"<p><a href='{job.get('redirect_url')}' target='_blank'>View Job</a></p></div>"

html += "</body></html>"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML report created: {OUTPUT_FILE}")

