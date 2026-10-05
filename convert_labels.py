from pathlib import Path

labels_dir = Path("combined_pothole_dataset/valid/labels")

converted = 0
already_detection = 0

for file in labels_dir.glob("*.txt"):
    new_lines = []

    for line in file.read_text().splitlines():
        parts = line.split()

        if not parts:
            continue

        # Already YOLO detection format
        if len(parts) == 5:
            new_lines.append(line)
            already_detection += 1
            continue

        # Segmentation format:
        # class x1 y1 x2 y2 x3 y3 ...
        cls = parts[0]
        coords = list(map(float, parts[1:]))

        if len(coords) < 4 or len(coords) % 2 != 0:
            print("Skipped invalid:", file.name)
            continue

        xs = coords[0::2]
        ys = coords[1::2]

        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)

        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        width = xmax - xmin
        height = ymax - ymin

        new_lines.append(
            f"{cls} {x_center:.6f} {y_center:.6f} "
            f"{width:.6f} {height:.6f}"
        )

    file.write_text("\n".join(new_lines) + "\n")
    converted += 1

print("DONE")
print("Files processed:", converted)
print("Detection rows kept:", already_detection)
