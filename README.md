import os
import json

def create_metadata_jsonl(dataset_dir: str, output_file: str = "metadata.jsonl"):
    """
    Reads all .png and .json files in dataset_dir, and writes metadata.jsonl
    where each line is:
    {"file_name": "userX.png", "ground_truth": "{\"gt_parse\": ... }"}
    """
    lines = []
    for fname in os.listdir(dataset_dir):
        if fname.lower().endswith(".json"):
            stem = fname[:-5]  # remove .json
            img_name = stem + ".png"
            json_path = os.path.join(dataset_dir, fname)
            img_path = os.path.join(dataset_dir, img_name)

            if not os.path.isfile(img_path):
                print(f"⚠️ Warning: no matching image for {json_path}, skipping.")
                continue

            # Load JSON content
            with open(json_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # Wrap content under "gt_parse"
            wrapped = {"gt_parse": content}

            # Dump ground_truth as a JSON string
            gt_str = json.dumps(wrapped, ensure_ascii=False)

            # Prepare metadata line
            entry = {
                "file_name": img_name,
                "ground_truth": gt_str
            }
            lines.append(entry)

    # Write to metadata.jsonl
    out_path = os.path.join(dataset_dir, output_file)
    with open(out_path, 'w', encoding='utf-8') as f:
        for entry in lines:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Wrote {len(lines)} entries to {out_path}")

# Usage:
# create_metadata_jsonl("dataset/")
