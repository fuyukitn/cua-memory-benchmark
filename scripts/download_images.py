import os
import json
import requests
import time
from pathlib import Path
from duckduckgo_search import DDGS

# Define paths
script_dir = Path(__file__).parent
json_path = script_dir.parent / "data" / "products.json"
output_dir = script_dir.parent / "static" / "img"
output_dir.mkdir(parents=True, exist_ok=True)

# Load product list
with open(json_path, "r") as f:
    products = json.load(f)

# Image search instance
ddgs = DDGS()

# Search and download one image per product
for product in products:
    name = product["name"]
    try:
        results = ddgs.images(name, safesearch="Moderate")
        if results and len(results) > 0:
            image_url = results[0]["image"]

            # Create safe filename
            filename = name.lower().replace(" ", "_").replace("/", "_") + ".jpg"
            save_path = output_dir / filename

            # Download image
            r = requests.get(image_url, timeout=10)
            r.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(r.content)

            # Update image path in JSON (for static serving)
            product["image"] = f"/static/img/{filename}"

            print(f"Downloaded: {name}")
        else:
            print(f"No image found for {name}")
    except Exception as e:
        print(f"Failed for {name}: {e}")
    time.sleep(1)

# Save updated products.json
with open(json_path, "w") as f:
    json.dump(products, f, indent=2)

print("🎉 All images downloaded and products.json updated.")