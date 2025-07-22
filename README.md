def collate_fn(batch):
    return {
        "input_ids": torch.stack([b["input_ids"] for b in batch]),
        "pixel_values": torch.stack([b["pixel_values"] for b in batch]),
        "labels": torch.stack([b["labels"] for b in batch]),
    }
