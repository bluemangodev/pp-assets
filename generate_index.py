import os
import json
import zipfile
import shutil
from PIL import Image

# ==== CONFIG ====
REPO_USER = "bluemangodev"
REPO_NAME = "pp-assets"
REPO_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main"

ZIP_DIR = "."  # Thư mục chứa các file .zip
THUMB_DIR = "thumbnails"
TEMP_DIR = "temp_extract"

# Tạo thư mục nếu chưa có
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

    # Xóa thư mục tạm trước mỗi lần extract
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Extract ZIP tạm thời
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    # Tìm file ảnh đầu tiên trong ZIP
    found_thumb = None
    for root, _, files in os.walk(TEMP_DIR):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                found_thumb = os.path.join(root, file)
                break
        if found_thumb:
            break

    # Nếu tìm thấy ảnh, chuyển sang .png nếu cần
    if found_thumb:
        dest_path = os.path.join(THUMB_DIR, thumb_filename)

        ext = os.path.splitext(found_thumb)[1].lower()
        if ext == ".png":
            shutil.copy(found_thumb, dest_path)
        else:
            # Chuyển JPG sang PNG
            try:
                img = Image.open(found_thumb).convert("RGBA")
                img.save(dest_path, "PNG")
            except Exception as e:
                print(f"[{name}] ❌ Failed to convert image: {e}")
                continue

        print(f"[{name}] ✅ Thumbnail saved: {thumb_filename}")
    else:
        print(f"[{name}] ⚠️ No thumbnail found in ZIP")

    # Ghi vào output JSON
    output.append({
        "title": title,
        "zipUrl": zip_url,
        "thumbnailUrl": thumb_url,
        "category": "Other"
    })

# Ghi ra index.json
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("\n🎉 Done generating index.json and thumbnails.")
