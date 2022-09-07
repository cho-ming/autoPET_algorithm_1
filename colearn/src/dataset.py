import os
import torch
import numpy as np
import nibabel as nib
from torch.utils.data import Dataset
import pathlib
import skimage.transform as skTrans
import matplotlib.pyplot as plt

def read_data(path_to_nifti, return_numpy=True):
    """Read a NIfTI image. Return a numpy array (default) or `nibabel.nifti1.Nifti1Image` object"""
    if return_numpy:
        return nib.load(str(path_to_nifti)).get_fdata()
    return nib.load(str(path_to_nifti))

def read_data_header(path_to_nifti):
    """Read a header file of Nifti image"""
    return nib.load(str(path_to_nifti))

def cal_margin(val):
    dap = int(val//16)
    na = (val%16)
    margin = int(32-na)
    if margin %2 ==0:
        margin_f, margin_l = int(margin//2),int(margin//2)
    else:
        margin_f = int(margin//2)
        margin_l = int(margin - margin_f)




    return margin_f,margin_l





class HecktorDataset(Dataset):
    def __init__(self, sample_path, transforms=None):
        self.sample_path = sample_path
        self.transforms = transforms


    def __len__(self):
        return len(self.sample_path)

    def __getitem__(self, index):
        sample = dict()

        header = read_data_header(self.sample_path[index][-1])
        sample['header'] = header.affine

        sample['id'] = str(self.sample_path[index][0]).split('/')[-2]

        PET = read_data(self.sample_path[index][0])
        CT = read_data(self.sample_path[index][1])

        sample['shape'] = PET.shape

        # img = [resize_pet, resize_ct]
        img = [PET, CT]
        img = np.stack(img, axis=-1)
        sample['input'] = img

        mask = read_data(self.sample_path[index][-1])
        mask = np.expand_dims(mask, axis=3)
        assert img.shape[:-1] == mask.shape[:-1]
        sample['target'] = mask



        if self.transforms:
            sample = self.transforms(sample)


        return sample


