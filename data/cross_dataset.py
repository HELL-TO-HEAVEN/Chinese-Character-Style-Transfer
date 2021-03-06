import logging
import random
import numpy as np
from .base_dataset import BaseDataset
logger = logging.getLogger(__name__)

class CrossDataset(BaseDataset):
    def name(self):
        return 'simple-data-loader'

    def __init__(self):
        pass

    def initialize(self, opt):
        logger.info('Initialize simple-data-loader...')
        self.path = opt.dataroot + '/' + opt.dataset
        self.data = np.load(self.path)
        self.content_size = self.data.shape[0]
        self.style_size = self.data.shape[1]
        self.sample_size = opt.sample_size
        logger.info("Content = %d"%self.content_size)
        logger.info("Style = %d"%self.style_size)
        logger.info("Sample = %d"%self.sample_size)
        logger.info('Initialize finish.')

    def __len__(self):
        return self.content_size * self.style_size

    def __getitem__(self, idx):
        idx1 = idx // self.style_size
        idx2 = idx %  self.style_size
        idxs_1 = []
        idxs_2 = []
        while True:
            for i in range(self.sample_size):
                while True:
                    x = random.randint(0,self.style_size-1)
                    if x != idx2:
                        break
                idxs_1.append(x)
                while True:
                    x = random.randint(0,self.content_size-1)
                    if x != idx1:
                        break
                idxs_2.append(x)
            flag = False
            for w in idxs_1:
                if self.data[idx1,w,:,:].sum() == 0:
                    flag = True
            for w in idxs_2:
                if self.data[w,idx2,:,:].sum() == 0:
                    flag = True
            if not flag:
                break
            else:
                logger.info("Filterd...");

        return (
                self.data[idx1,idxs_1,:,:],
                self.data[idxs_2,idx2,:,:],
                self.data[idx1,idx2,:,:])
