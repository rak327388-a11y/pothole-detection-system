from pathlib import Path
import shutil

# Original RDD2022 dataset
SOURCE = Path("indian_data/rdd2022_india")

# New pothole-only dataset
DEST = Path("indian_data/rdd2022_pothole_only")

# RDD2022 class 6 = D40 = pothole
POTHOLE_CLASS = 6

splits = ["train", "valid", "test"]

for split in splits:
    src_images = SOURCE / split / "images"
    src_labels = SOURCE / split / "labels"

    dst_images = DEST / split / "images"
    dst_labels = DEST / split / "labels"

    dst_images.mkdir(parents=True, exist_ok=True)
    dst_labels.mkdir(parents=True, exist_ok=True)

    count = 0

    for label_file in src_labels.glob("*.txt"):
        lines = label_file.read_text().splitlines()

        pothole_lines = []

        for line in lines:
            parts = line.split()

            if len(parts) == 5 and parts[0] == str(POTHOLE_CLASS):
                # Change RDD2022 class 6 (D40) to class 0 (pothole)
                parts[0] = "0"
                pothole_lines.append(" ".join(parts))

        # Only copy images that contain at least one pothole
        if pothole_lines:
            image_found = False

            for extension in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
                image_file = src_images / (label_file.stem + extension)

                if image_file.exists():
                    shutil.copy2(
                        image_file,
                        dst_images / image_file.name
                    )
                    image_found = True
                    break

            if image_found:
                (dst_labels / label_file.name).write_text(
                    "\n".join(pothole_lines) + "\n"
                )
                count += 1

    print(f"{split}: {count} pothole images copied")

# Create data.yaml
yaml_content = """train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1
names: ['pothole']
"""

(DEST / "data.yaml").write_text(yaml_content)

print("\nDONE!")
print(f"Pothole-only dataset created at: {DEST}")