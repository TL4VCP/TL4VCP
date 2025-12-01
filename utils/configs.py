# Copyright 2022 CircuitNet. All rights reserved.

import argparse
import os
import sys

sys.path.append(os.getcwd())


class Parser(object):
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--task', default='congestion_gpdl')

        self.parser.add_argument('--save_path', default='work_dir/congestion_gpdl/')
    
        self.parser.add_argument('--pretrained', default=None) # for transfer-learning or test

        self.parser.add_argument('--max_iters', default=200) # transfer learning 200
        self.parser.add_argument('--plot_roc', action='store_true')
        self.parser.add_argument('--arg_file', default=None)
        self.parser.add_argument('--cpu', action='store_true')

        self.parser.add_argument('--dataroot', default='../../training_set/congestion')
        self.parser.add_argument('--ann_file_train', default='./files/train_N14.csv')
        self.parser.add_argument('--ann_file_test', default='./files/test_N14.csv')
        self.parser.add_argument('--dataset_type', default='SuperBlueDataset')
        self.get_remainder()
        
    def get_remainder(self):
        if self.parser.parse_args().task == 'congestion_gpdl':
            self.parser.add_argument('--dataroot', default='../../training_set/congestion')
            self.parser.add_argument('--ann_file_train', default='./files/train_N28.csv')
            self.parser.add_argument('--ann_file_test', default='./files/test_N28.csv')
            self.parser.add_argument('--dataset_type', default='CongestionDataset')
            self.parser.add_argument('--batch_size', default=16)
            self.parser.add_argument('--aug_pipeline', default=['Flip'])
            
            self.parser.add_argument('--model_type', default='GPDL')
            self.parser.add_argument('--in_channels', default=3)
            self.parser.add_argument('--out_channels', default=1)
            self.parser.add_argument('--lr', default=2e-4)
            self.parser.add_argument('--weight_decay', default=0)
            self.parser.add_argument('--loss_type', default='MSELoss')
            self.parser.add_argument('--eval-metric', default=['NRMS', 'SSIM', 'EMD'])
        elif self.parser.parse_args().task == 'transfer_learning_adapter':
            # self.parser.add_argument('--dataroot', default='../../training_set/congestion')
            # self.parser.add_argument('--ann_file_train', default='./files/train_N28.csv')
            # self.parser.add_argument('--ann_file_test', default='./files/test_N28.csv')
            # self.parser.add_argument('--dataset_type', default='SuperBlueDataset')
            self.parser.add_argument('--batch_size', default=16)
            self.parser.add_argument('--aug_pipeline', default=['Flip'])

            self.parser.add_argument('--model_type', default='Congestion_Prediction_Net')
            self.parser.add_argument('--in_channels', default=3)
            self.parser.add_argument('--out_channels', default=1)
            self.parser.add_argument('--lr', default=2e-4)
            self.parser.add_argument('--weight_decay', default=0)
            self.parser.add_argument('--loss_type', default='MSELoss')
            self.parser.add_argument('--eval-metric', default=['NRMS', 'SSIM', 'EMD', 'PSNR'])
            # self.parser.add_argument('--pretrained_transfer', default='../../transfer_learning_1.0-ispd/models/pretrained/gpdl_congestion.pth')
        else:
            raise ValueError
