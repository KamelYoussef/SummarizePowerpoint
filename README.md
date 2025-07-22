def collate_fn(batch):
    print("Batch item types:", [type(item) for item in batch])
    print("Keys:", [item.keys() for item in batch])
    print("pixel_values shapes:", [b["pixel_values"].shape if "pixel_values" in b else None for b in batch])
    print("labels types:", [type(b.get("labels")) for b in batch])
    print("labels shapes:", [b["labels"].shape for b in batch])
    # then stack once verified
    return {
        "pixel_values": torch.stack([b["pixel_values"] for b in batch]),
        "labels": torch.stack([b["labels"] for b in batch])
    }
