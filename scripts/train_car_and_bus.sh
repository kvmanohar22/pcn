cd /home/ankush/kv/pcn

# Set the following variables
MODEL_TYPE=pcn_emd
LOG_DIR=log_car_bus/${MODEL_TYPE}2
BATCH_SIZE=10
NUM_INPUT_POINTS=3000
NUM_GT_POINTS=16384
STEPS_PER_PRINT=100
STEPS_PER_EVAL=5000
STEPS_PER_SAVE=10000

export CUDA_VISIBLE_DEVICES=0
python train.py \
   --lmdb_train data/car_bus/train.mdb \
   --lmdb_valid data/car_bus/valid.mdb \
   --model_type ${MODEL_TYPE} \
   --log_dir ${LOG_DIR} \
   --batch_size ${BATCH_SIZE} \
   --num_input_points ${NUM_INPUT_POINTS} \
   --num_gt_points ${NUM_GT_POINTS} \
   --steps_per_print ${STEPS_PER_PRINT} \
   --steps_per_eval ${STEPS_PER_EVAL} \
   --steps_per_save ${STEPS_PER_SAVE} \
   --lr_decay
 
