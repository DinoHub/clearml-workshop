"""
PyTorch-lightning training script with data from ClearML hyperdataset - iterator method (e.g. dataview.get_iterator()).
You can change the dataset MyDataModule._load_dataview and MyDataModule.setup for versions

python pytorch_with_iter_dataset.py
"""
from typing import Optional

import numpy as np
import pytorch_lightning as pl
import torch
from PIL import Image
from pytorch_lightning.utilities.cli import LightningCLI
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import transforms

from allegroai import DataView, FrameGroup, Task


class Backbone(torch.nn.Module):
    def __init__(self, hidden_dim=128):
        super().__init__()
        self.l1 = torch.nn.Linear(28 * 28, hidden_dim)
        self.l2 = torch.nn.Linear(hidden_dim, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.l1(x))
        x = torch.relu(self.l2(x))
        return x


class LitClassifier(pl.LightningModule):
    def __init__(self, backbone: Optional[Backbone] = None):
        super().__init__()
        self.save_hyperparameters(ignore=["backbone"])
        if backbone is None:
            backbone = Backbone()
        self.backbone = backbone

    def forward(self, x):
        # use forward for inference/predictions
        embedding = self.backbone(x)
        return embedding

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("train_loss", loss, on_epoch=True)
        return None

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("valid_loss", loss, on_step=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("test_loss", loss)

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        x, y = batch
        return self(x)

    def configure_optimizers(self):
        # self.hparams available because we called self.save_hyperparameters()
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)


class AllegroDatasetIter(Dataset):

    def __init__(
            self,
            dataview: DataView,
    ):
        """
        :param dataview: The Allegro DataView
        """
        self._dataview = dataview
        self._count = None
        self._transform = transforms.Compose(
            [
                transforms.PILToTensor(),
                transforms.Resize([28, 28]),
                transforms.Grayscale(),
                transforms.ConvertImageDtype(torch.float)
            ]
        )
        self.frames = self._dataview.get_iterator()

    def __next__(self):
        # We will call the iterator next() for getting the next frame
        frame = next(self.frames)
        if isinstance(frame, FrameGroup):
            # if this is a FrameGroup, use the first SingleFrame
            frame = list(frame.values())[0]
        # Download the data locally (cached)
        img_path = frame.get_local_source()
        img = Image.open(img_path).convert("RGB")
        mock_classification = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=np.float32)
        return self._transform(img), mock_classification

    def __getitem__(self, item):
        return self.__next__()

    def __len__(self) -> int:
        if self._count is None:
            # will return the total number of frames in this version
            self._count = self._dataview.get_count()[0]
        return self._count


class MyDataModule(pl.LightningDataModule):
    def __init__(self, batch_size: int = 32):
        super().__init__()
        self.batch_size = batch_size
        self.train_data = self.val_data = None

    @staticmethod
    def _load_dataview(version, dv_name):
        dataview = DataView(dv_name)
        # Can be changed with other datasets and queries
        dataview.add_query(
            dataset_name="COCO - Common Objects in Context",
            version_name=version,
            roi_query="car"
        )
        # prefetch_files will start downloading all the files in background threads
        dataview.prefetch_files()
        return AllegroDatasetIter(dataview=dataview)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_data = self._load_dataview("Train2017 version", "train")
        self.val_data = self._load_dataview("Val2014 version", "val")

    def train_dataloader(self):
        return DataLoader(self.train_data, num_workers=6, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_data, num_workers=6, batch_size=self.batch_size)


def cli_main():
    task = Task.init(project_name="examples", task_name="DataLoader with iterator")
    cli = LightningCLI(
        LitClassifier,
        MyDataModule,
        seed_everything_default=17,
        save_config_overwrite=True,
        run=False,
    )
    cli.trainer.fit(cli.model, datamodule=cli.datamodule)


if __name__ == '__main__':
    cli_main()
