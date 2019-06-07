cd /home/ankush/kv/pcn

# Set the following variables
MODEL_TYPE=pcn_emd
LOG_DIR=log/${MODEL_TYPE}
BATCH_SIZE=4
NUM_INPUT_POINTS=3000
NUM_GT_POINTS=16384
STEPS_PER_PRINT=1

export CUDA_VISIBLE_DEVICES=0
python train.py \
   --lmdb_train data/shapenet_car/train.lmdb \
   --lmdb_valid data/shapenet_car/valid.lmdb \
   --model_type ${MODEL_TYPE} \
   --log_dir ${LOG_DIR} \
   --batch_size ${BATCH_SIZE} \
   --num_input_points ${NUM_INPUT_POINTS} \
   --num_gt_points ${NUM_GT_POINTS} \
   --steps_per_print ${STEPS_PER_PRINT}  
