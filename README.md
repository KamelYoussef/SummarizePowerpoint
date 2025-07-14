import os, json
from glob import glob
from PIL import Image
from datasets import Dataset
import torch
import pytorch_lightning as pl
from transformers import DonutProcessor, VisionEncoderDecoderModel
