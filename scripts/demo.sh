INPUT=demo_data/frame_5_car_0.pcd

python demo.py \
   --checkpoint log/pcn_emd/model-300000 \
   --model_type pcn_emd \
   --input_path ${INPUT}

