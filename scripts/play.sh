cd /home/ankush/kv/pcn

# Set the following variables
MODEL_TYPE=pcn_cd
LOG_DIR=log/play/${MODEL_TYPE}
BATCH_SIZE=2
NUM_INPUT_POINTS=3000
NUM_GT_POINTS=16384
STEPS_PER_PRINT=1

rm -rf log/play/*
export CUDA_VISIBLE_DEVICES=''
python train.py \
   --lmdb_train data/shapenet_car/train.lmdb \
   --lmdb_valid data/shapenet_car/valid.lmdb \
   --model_type ${MODEL_TYPE} \
   --log_dir ${LOG_DIR} \
   --batch_size ${BATCH_SIZE} \
   --num_input_points ${NUM_INPUT_POINTS} \
   --num_gt_points ${NUM_GT_POINTS} \
   --steps_per_print ${STEPS_PER_PRINT}  
