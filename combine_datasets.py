from pathlib import Path
import shutil

DEST = Path("combined_pothole_dataset")

DATASETS = {
    "original": Path("dataset"),
    "bharat": Path("indian_data/bharatpothole/BharatPotHole/BharatPotHole"),
    "rdd2022": Path("indian_data/rdd2022_pothole_only"),
}

SPLITS = ["train", "valid", "test"]

total = 0

for dataset_name, source in DATASETS.items():
    print(f"\nProcessing: {dataset_name}")

    for split in SPLITS:
        src_images = source / split / "images"
        src_labels = source / split / "labels"

        dst_images = DEST / split / "images"
        dst_labels = DEST / split / "labels"

        if not src_images.exists() or not src_labels.exists():
            print(f"  {split}: folders not found - skipped")
            continue

        count = 0

        for label_file in src_labels.glob("*.txt"):
            image_file = None

            for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
                candidate = src_images / (label_file.stem + ext)
                if candidate.exists():
                    image_file = candidate
                    break

            if image_file is None:
                continue

            # Unique filename to prevent collisions
            new_name = f"{dataset_name}_{image_file.name}"
            new_label = f"{dataset_name}_{label_file.name}"

            shutil.copy2(image_file, dst_images / new_name)
            shutil.copy2(label_file, dst_labels / new_label)

            count += 1
            total += 1

        print(f"  {split}: {count} images copied")

print("\n==============================")
print(f"TOTAL IMAGES COPIED: {total}")
print("==============================")

yaml = """train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1
names: ['pothole']
"""

(DEST / "data.yaml").write_text(yaml)

print("data.yaml created successfully.")