import os
import json

REPO_USER = "bluemangodev"
REPO_NAME = "svg-assets"
REPO_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main"

index = []

for file in os.listdir("."):
    if file.lower().endswith(".zip"):
        name = os.path.splitext(file)[0]
        title = name.replace("-", " ").replace("_", " ")
        zip_url = f"{REPO_URL}/{file}"

        # Nếu có thumbnail về sau thì cập nhật sau
        thumb_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder.png"

        index.append({
            "title": title,
            "zipUrl": zip_url,
            "thumbnailUrl": thumb_url,
            "category": "Other"
        })

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2)
