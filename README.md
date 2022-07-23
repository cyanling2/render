To build docker image, run:
docker build $PATH-TO-DOCKERFILE

Launch docker container exposed to GPU0 and create a volume:
docker run -it -e NVIDIA_VISIBLE_DEVICES=0 -v /home/cyan:/host --runtime=nvidia --name gpu0 $IMAGE-NAME

If you want to detach the container shell, inside the container, press P+Q
run docker attach gpu0 to re-attach the container

Manually test frame based distribution:
attach the shell and then run:
blender -b /host/Car_Sci_FI.blend -o /host/render_results/ -E CYCLES -s $START_FRAME -e $END_FRAME -a -- --cycles-device CUDA
The results will be stored in folder reder_results

Manually test tile based distribution:
attach the shell and then run:
blender -b /host/Car_Sci_FI.blend --python /host/pyblender.py

To execute my renderfarm, in host, run:
python3 distribute.py
Specify num_gpus and resolution at line 26 and 28.
