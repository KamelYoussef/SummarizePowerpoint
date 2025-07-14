model = DonutFineTuner()
trainer = pl.Trainer(accelerator="gpu", devices=1, max_epochs=5)
trainer.fit(model, 
            train_dataloaders=torch.utils.data.DataLoader(train_ds, batch_size=4, shuffle=True),
            val_dataloaders=torch.utils.data.DataLoader(val_ds, batch_size=2))
