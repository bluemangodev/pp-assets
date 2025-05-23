import os
import json
import zipfile
import shutil

# ==== CONFIG ==== #
REPO_USER = "bluemangodev"
REPO_NAME = "svg-assets"
REPO_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main"

ZIP_DIR = "."  # thư mục hiện tại
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
    "thumbnailUrl": f"{REPO_URL}/thumbnails/{name}.png"
    thumb_url = f"{REPO_URL}/thumbnails/{name}.png"

    found_thumb = False

    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            candidates = [
                m for m in z.namelist()
                if m.lower().endswith((".png", ".jpg", ".jpeg"))
                and "__MACOSX" not in m
            ]
            candidates.sort()  # đảm bảo thứ tự ổn định

            for member in candidates:
                z.extract(member, TEMP_DIR)
                extracted_path = os.path.join(TEMP_DIR, member)
                if not os.path.isfile(extracted_path):
                    continue

                # Chuyển đổi sang PNG nếu cần
                ext = os.path.splitext(member)[1].lower()
                dest_path = os.path.join(THUMB_DIR, f"{name}.png")

                shutil.copy(extracted_path, dest_path)
                found_thumb = True
                break

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {filename}: {e}")

    if not found_thumb:
        thumb_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder.png"

    output.append({
        "title": title,
        "zipUrl": zip_url,
        "thumbnailUrl": thumb_url,
        "category": "Other"
    })

# Xóa tạm
shutil.rmtree(TEMP_DIR, ignore_errors=True)

# Ghi index.json
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"✅ Đã tạo index.json với {len(output)} mục.")
