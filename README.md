class DonutFineTuner(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "naver-clova-ix/donut-base"
        )
        self.lr = 5e-5

    def forward(self, pixel_values, labels):
        return self.model(pixel_values=pixel_values, labels=labels)

    def training_step(self, batch, batch_idx):
        loss = self(**batch).loss
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self(**batch).loss
        self.log("val_loss", loss)

    def configure_optimizers(self):
        return torch.optim.AdamW(self.model.parameters(), lr=self.lr)
