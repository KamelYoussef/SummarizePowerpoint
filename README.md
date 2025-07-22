from datasets import load_dataset

raw = load_dataset(
    "imagefolder",
    data_dir="dataset",
    split="train",
    keep_in_memory=True
)

def preprocess(sample):
    import json
    text = json.loads(sample["ground_truth"])
    token_str = "<s>" + json2token(text) + "</s>"
    sample["text"] = token_str
    sample["image"] = sample["image"].convert("RGB")
    return sample

proc = raw.map(preprocess)

from transformers import DonutProcessor

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
new_tokens = list_of_special_tokens_from_json()  # e.g., field names wrapped in tags
processor.tokenizer.add_special_tokens({"additional_special_tokens": new_tokens})
processor.feature_extractor.size = [720, 960]

def transform(sample):
    pv = processor(sample["image"], return_tensors="pt").pixel_values.squeeze()
    enc = processor.tokenizer(
        sample["text"],
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    labels = enc.input_ids.clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    return {"pixel_values": pv, "labels": labels}

dataset = proc.map(transform, remove_columns=["image", "ground_truth", "text"])
