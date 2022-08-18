# myRenderfarm
To build docker image, run:
```
docker build $PATH-TO-DOCKERFILE
```
Launch docker container exposed to GPU0 and create a volume:
```
docker run -it -e NVIDIA_VISIBLE_DEVICES=0 -v /home/cyan:/host --runtime=nvidia --name gpu0 $IMAGE-NAME
```
If you want to detach the container shell, inside the container, press P+Q
run
```
docker attach gpu0 
```
to re-attach the container

Manually test frame based distribution:
attach the shell and then run:
```
blender -b /host/Car_Sci_FI.blend -o /host/render_results/ -E CYCLES -s $START_FRAME -e $END_FRAME -a -- --cycles-device CUDA
```
The results will be stored in folder reder_results

Manually test tile based distribution:
attach the shell and then run:
```
blender -b /host/Car_Sci_FI.blend --python /host/pyblender.py
```
To execute my renderfarm, in host, run:
```
python3 distribute.py
```
Specify num_gpus and resolution at line 26 and 28.

_____________________________________________________________________________________
no_docker method

install blender 3.2 and run
```
python3 distribute_nodocker.py
```

# FACSVatar reproduction on Windows

## QuickStart

* Visit https://github.com/NumesSanguis/FACSvatar and clone the repo
* Downloads - Go to https://github.com/NumesSanguis/FACSvatar/releases and download:
  - openface_2.1.0_zeromq.zip
    - Unzip and execute download_models.sh or .ps1 to download trained models
  - Windows 7 / 8 / 10 Home: unity_FACSvatar_standalone_docker-ip.zip
  - Windows 10 Pro / Enterprise / Education: unity_FACSvatar_standalone.zip (mine is this one)
  - Windows / Linux / Mac: Unity3D editor (documentation)
  - Source code (zip / tar.gz) or download this repository with:
    - ```git clone https://github.com/NumesSanguis/FACSvatar.git```
    - Press the green Clone or Download button on this page --> Download ZIP
* Docker Install
* Docker Modules - Open a terminal (W7/8: cmd.exe / W10: PowerShell) and navigate to folder FACSvatar/modules, then execute:
  - ```docker-compose pull``` (Downloads FACSvatar Docker containers)
  - ```docker-compose up``` (Starts downloaded Docker containers)
* Facial Animation with Unity3D - Navigate inside folder unity_FACSvatar_standalone(_docker-ip) and Double-click ```unity_FACSvatar.exe``` / Press play button in Unity3D editor
  - This step will open a default scene with two avatars sitting at a desk face to face (side view)
### Offline
* Open a 2nd terminal in folder FACSvatar/modules and execute: ```docker-compose exec facsvatar_facsfromcsv bash```
* Inside Docker container - Start facial animation with: ```python main.py --pub_ip facsvatar_bridge```
* In host, there are some sample .csv files containing AUs at ```FACSvatar/modules/input_facsfromcsv/openface``` These are mounted to the docker container.
You can customize your own .csv files following the format in samples and do docker copy to use it.
* Use flags ```--csv_foler``` and ```--csv_arg``` to select input AUs. Check ```FACSvatar/modules/input_facsfromcsv/main.py``` for details.
### Webcam (windows only)
* Navigate inside folder ```openface_x.x.x_zeromq```
* (Windows 7/8/10 Home - only) Get Docker machine ip by opening a 2nd terminal and execute: ```docker-machine ip``` (likely to be 192.168.99.100) \
Mine is education version and can not install docker-machine command, but the ip is just the same.
* (Windows 7/8/10 Home - only) Open ```config.xml```, change ```<IP>127.0.0.1</IP>``` to ```<IP>machine ip from step 3</IP> (<IP>192.168.99.100</IP>)``` and save and close.
  - Double click ```OpenFaceOffline.exe``` –> select a saving location in menu bar and then -> File –> Open Webcam
  - Click stop to finish recording and copy the output .csv file to docker then repeate step 2 in ```Offline``` section

## Observations
* I tested on both the sample .csv files and my own recordings. This repo does a good job capturing head rotation and eye-gaze (when eyes are open). 
  - The head has about 45 degree freedom to all four directions (up, down, left, right). I believe this is related to the openface pipeline, where face detection is the first step. If you rotate too much (like a complete side view), the face detection fails and thus all following subnets shut down. However, within the "face detection range", head rotation is captured accurately.
  - With your eyes open and giving the camera a front view of your face, the eye-gaze detection works normally. However, eyeblink will not be detected. If you close your eyes for a long time the eye-gaze detection will fall into a chaos. 
  - Landmark detections are motion sensitive. For those around the mouth, which are extremely dynamic when you move your lips, they will fail in some edge cases. e.x. You make some exaggrate expressions and open your mouth really big.
  - When you put your tongue out, the landmark detection around mouth also fails. To be specific, it will detect a closed mouth. I think the reason is the visibility of certain parts of the face, which contribute to a landmark, matters when doing the capture. We can try covering some parts of the face and see how it works.



