def json_to_token(json_obj):
    txt = ""
    for k, v in json_obj.items():
        txt += f"<s_{k}>{v}</s_{k}>"
    return f"<s>{txt}</s>"

# Build Hugging Face Dataset
records = []
for img_path in glob("data/*.png"):
    j = img_path.replace(".png", ".json")
    with open(j) as f:
        js = json.load(f)
    records.append({
        "image_path": img_path,
        "labels": json_to_token(js)
    })

ds = Dataset.from_list(records)
