# Author: Wentao Yuan (wyuan1@cs.cmu.edu) 05/31/2018

import argparse
import os
from io_util import read_pcd
from tensorpack import DataFlow, dataflow


class pcd_df(DataFlow):
    def __init__(self, model_list):
        self.model_list = model_list
        self.base_dir  = os.getenv("BUS_CAR_BASE_DIR")

    def size(self):
        return len(self.model_list)

    def get_data(self):
        for model_id in model_list:
            complete = read_pcd(os.path.join(self.base_dir, model_id, 'GT.pcd'))
            for i in range(len(os.listdir(os.path.join(self.base_dir, model_id)))-1):
                partial = read_pcd(os.path.join(self.base_dir, model_id, '%d.pcd' % i))
                yield model_id.replace('/', '_'), partial, complete


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list_path')
    parser.add_argument('--output_path')
    args = parser.parse_args()

    with open(args.list_path) as file:
        model_list = file.read().splitlines()
    df = pcd_df(model_list)
    if os.path.exists(args.output_path):
        os.system('rm %s' % args.output_path)
    dataflow.LMDBSerializer.save(df, args.output_path)

