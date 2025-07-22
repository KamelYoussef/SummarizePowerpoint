import torch

def collate_fn(batch):
    pixel_vals = torch.stack([b["pixel_values"] for b in batch])
    labels = torch.stack([b["labels"] for b in batch])  # already padded to -100 in preprocess()
    return {"pixel_values": pixel_vals, "labels": labels}
