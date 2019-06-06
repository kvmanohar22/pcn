NUM_SCANS_PER_MODEL=10

blender -b -P render/render_depth.py ${DATA_SHAPENET} lists/car.txt ${DATA_SHAPENET}/pcn/car ${NUM_SCANS_PER_MODEL}
