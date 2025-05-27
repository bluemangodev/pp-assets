import os
import json
import zipfile
import shutil
from PIL import Image

# ==== CONFIG ====
REPO_USER = "bluemangodev"
REPO_NAME = "pp-assets"
REPO_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main"

ZIP_DIR = "."  # Folder containing .zip files
THUMB_DIR = "thumbnails"
TEMP_DIR = "temp_extract"
THUMB_SIZE = (300, 300)

# Ensure folders exist
os.makedirs(THUMB_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

output = []

for filename in os.listdir(ZIP_DIR):
    if not filename.lower().endswith(".zip"):
        continue

    filepath = os.path.join(ZIP_DIR, filename)
    name = os.path.splitext(filename)[0]
    title = name.replace("-", " ").replace("_", " ")

    zip_url = f"{REPO_URL}/{filename}"
    thumb_filename = f"{name}.png"
    thumb_url = f"{REPO_URL}/thumbnails/{thumb_filename}"

    # Reset temp extract
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR)
    except Exception as e:
        print(f"[{name}] ❌ Failed to extract ZIP: {e}")
        continue

    found_thumb = None
    for root, _, files in os.walk(TEMP_DIR):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                found_thumb = os.path.join(root, file)
                break
        if found_thumb:
            break

    if found_thumb:
        dest_path = os.path.join(THUMB_DIR, thumb_filename)
        try:
            img = Image.open(found_thumb).convert("RGBA")

            # Bỏ qua nếu ảnh trắng hoàn toàn
            if img.getbbox() is None:
                print(f"[{name}] ⚪ Skipped - Image is blank.")
                continue

            # Resize thumbnail về đúng kích thước
            img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
            img.save(dest_path, "PNG")

            print(f"[{name}] ✅ Thumbnail saved: {thumb_filename}")
        except Exception as e:
            print(f"[{name}] ❌ Error processing image: {e}")
            continue
    else:
        print(f"[{name}] ⚠️ No image found in ZIP.")

    output.append({
        "title": title,
        "zipUrl": zip_url,
        "thumbnailUrl": thumb_url,
        "category": "Other"
    })

# Save index.json
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("\n🎉 Done generating index.json and thumbnails.")
