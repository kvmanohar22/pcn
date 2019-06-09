NUM_SCANS_PER_MODEL=8

TYPE=bus
blender -b -P render/render_depth.py ${DATA_SHAPENET} lists/$TYPE.txt ${DATA_SHAPENET}/data/$TYPE ${NUM_SCANS_PER_MODEL}
