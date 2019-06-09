TYPE=car

DATA_BASE=${DATA_SHAPENET}
MODEL_LIST=`cat lists/${TYPE}.txt`

for model in ${MODEL_LIST}; do
   MODEL_OBJ_IN=${DATA_SHAPENET}/$model/model.obj
   MODEL_OBJ_OUT=${DATA_SHAPENET}/../pcn/my_data/${TYPE}/pcd/$model/GT.pcd
   ./sample/build/mesh_sampling ${MODEL_OBJ_IN} ${MODEL_OBJ_OUT} -no_vis_result 
done

