# Author: Wentao Yuan (wyuan1@cs.cmu.edu) 05/31/2018

import numpy as np
import tensorflow as tf
from tensorpack import dataflow

from io_util import save_pcd
import os
from os.path import join

def resample_pcd(pcd, n):
    """Drop or duplicate points so that pcd has exactly n points"""
    idx = np.random.permutation(pcd.shape[0])
    if idx.shape[0] < n:
        idx = np.concatenate([idx, np.random.randint(pcd.shape[0], size=n-pcd.shape[0])])
    return pcd[idx[:n]]


class PreprocessData(dataflow.ProxyDataFlow):
    def __init__(self, ds, input_size, output_size):
        super(PreprocessData, self).__init__(ds)
        self.input_size = input_size
        self.output_size = output_size

    def get_data(self):
        for id, input, gt in self.ds.get_data():
            input = resample_pcd(input, self.input_size)
            gt = resample_pcd(gt, self.output_size)
            yield id, input, gt


class BatchData(dataflow.ProxyDataFlow):
    def __init__(self, ds, batch_size, input_size, gt_size, remainder=False, use_list=False):
        super(BatchData, self).__init__(ds)
        self.batch_size = batch_size
        self.input_size = input_size
        self.gt_size = gt_size
        self.remainder = remainder
        self.use_list = use_list

    def __len__(self):
        ds_size = len(self.ds)
        div = ds_size // self.batch_size
        rem = ds_size % self.batch_size
        if rem == 0:
            return div
        return div + int(self.remainder)

    def __iter__(self):
        holder = []
        for data in self.ds:
            holder.append(data)
            if len(holder) == self.batch_size:
                yield self._aggregate_batch(holder, self.use_list)
                del holder[:]
        if self.remainder and len(holder) > 0:
            yield self._aggregate_batch(holder, self.use_list)

    def _aggregate_batch(self, data_holder, use_list=False):
        ''' Concatenate input points along the 0-th dimension
            Stack all other data along the 0-th dimension
        '''
        ids = np.stack([x[0] for x in data_holder])
        inputs = [resample_pcd(x[1], self.input_size) if x[1].shape[0] > self.input_size else x[1]
            for x in data_holder]
        inputs = np.expand_dims(np.concatenate([x for x in inputs]), 0).astype(np.float32)
        npts = np.stack([x[1].shape[0] if x[1].shape[0] < self.input_size else self.input_size
            for x in data_holder]).astype(np.int32)
        gts = np.stack([resample_pcd(x[2], self.gt_size) for x in data_holder]).astype(np.float32)
        return ids, inputs, npts, gts


def lmdb_dataflow(lmdb_path, batch_size, input_size, output_size, is_training, test_speed=False):
    df = dataflow.LMDBSerializer.load(lmdb_path, shuffle=False)
    size = df.size()
    if is_training:
        df = dataflow.LocallyShuffleData(df, buffer_size=2000)
        df = dataflow.PrefetchData(df, nr_prefetch=500, nr_proc=1)
    df = BatchData(df, batch_size, input_size, output_size)
    if is_training:
        df = dataflow.PrefetchDataZMQ(df, nr_proc=8)
    df = dataflow.RepeatedData(df, -1)
    if test_speed:
        dataflow.TestDataSpeed(df, size=1000).start()
    df.reset_state()
    return df, size


def get_queued_data(generator, dtypes, shapes, queue_capacity=10):
    assert len(dtypes) == len(shapes), 'dtypes and shapes must have the same length'
    queue = tf.FIFOQueue(queue_capacity, dtypes, shapes)
    placeholders = [tf.placeholder(dtype, shape) for dtype, shape in zip(dtypes, shapes)]
    enqueue_op = queue.enqueue(placeholders)
    close_op = queue.close(cancel_pending_enqueues=True)
    feed_fn = lambda: {placeholder: value for placeholder, value in zip(placeholders, next(generator))}
    queue_runner = tf.contrib.training.FeedingQueueRunner(queue, [enqueue_op], close_op, feed_fns=[feed_fn])
    tf.train.add_queue_runner(queue_runner)
    return queue.dequeue()


def save_batch_data(ids, inputs, gt):
   for _id, _inputs, _gt in zip(ids, inputs, gt):
      model_id = _id.split('_')[1]
      dir_name = join(os.getenv("BASE_ROOT"), model_id)
      if os.path.exists(dir_name):
         n_files = len(os.listdir(dir_name))-1
         save_pcd(join(dir_name, "{}.pcd".format(n_files)), _inputs)
      else:
         os.makedirs(dir_name)
         save_pcd(join(dir_name, "0.pcd"), _inputs)
         save_pcd(join(dir_name, "GT.pcd"), _gt)

def reshape_data(_npts, _inputs):
   inputs = []
   begin = 0
   for ii in _npts:
      end = begin + ii 
      _input = _inputs[0, begin:end, :] 
      inputs.append(_input)
      begin = end 
   assert len(inputs) == len(_npts)
   return inputs


if __name__ == '__main__':
    input_size = 3000
    output_size = 16384
    lmdb_path = "/home/ankush/kv/pcn/data/shapenet_car/valid.lmdb"
    df = dataflow.LMDBSerializer.load(lmdb_path, shuffle=False)
    size = df.size()
    df = dataflow.LocallyShuffleData(df, buffer_size=7000)
    df = dataflow.PrefetchData(df, nr_prefetch=2, nr_proc=1)
    df = BatchData(df, 2, input_size, output_size)
    data_gen = df.get_data()

    count = 0
    while count <= size:
        ids, inputs, npts, gt = next(data_gen)
        inputs = reshape_data(npts, inputs)
        count += len(ids)
        save_batch_data(ids, inputs, gt)   
        print("{:5d}/{:5d}: inputs: ({}) npts: ({}) gt: ({}), n[0]: {}, i[0]: {}".format(count, size, inputs[0].shape, npts.shape, gt.shape, npts[0], ids[0]))
