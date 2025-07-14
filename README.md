class FormsDataset(torch.utils.data.Dataset):
    def __init__(self, ds):
        self.ds = ds
    def __len__(self): return len(self.ds)
    def __getitem__(self, i):
        item = self.ds[i]
        return {
            "pixel_values": item["pixel_values"],
            "labels": item["labels"]
        }

train_ds = FormsDataset(ds["train"])
val_ds = FormsDataset(ds["test"])
