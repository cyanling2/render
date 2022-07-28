import docker
import os
from PIL import Image
import time
import threading
import sys
from multiprocessing import Process



def render(animation, gpu, num_gpus, resolution, start, end):
    docker_image = "nvidia/cuda:11.6-base-ubuntu18.04-blender3.2"
    blendfile = "Car_Sci_FI.blend"
    envlist = {"gpuidx":gpu, "num_gpus":num_gpus, \
            "WIDTH":resolution[0], "HEIGHT":resolution[1], \
            "ANIMATION":animation, "START_FRAME":start, "END_FRAME":end}
    cmd = f"blender -b {blendfile} --python pyblender.py"
    client = docker.from_env()
    s=time.time()
    # c = client.containers.run(docker_image, command=f"blender -b /host/{blendfile} --python /host/pyblender.py",\
    #                     environment=[f"CUDA_VISIBLE_DEVICES={gpu}", f"num_gpus={num_gpus}", f"WIDTH={resolution[0]}", f"HEIGHT={resolution[1]}"],\
    #                     volumes=["/home/cyan:/host"], runtime="nvidia", name=f"gpu{gpu}", detach=True)
    c = client.containers.get(f"gpu{gpu}")
    c.exec_run(cmd, environment=envlist)
    e=time.time()
    print("time taken to execute on gpu",gpu, " = ", e-s)

num_gpus = 1
processList = []
resolution = (1280, 720)
# render(sys.argv[1], 1, resolution)
num_frames = 4
start=time.time()
for gpu in range(num_gpus):
    # gpu=sys.argv[1]
    p = Process(target=render, args=(True, gpu, num_gpus, resolution, num_frames//num_gpus*gpu, num_frames//num_gpus*(gpu+1)-1))
    p.start()
    # processList.append(p)
    # render(True, gpu, num_gpus, resolution, num_frames//num_gpus*gpu, num_frames//num_gpus*(gpu+1)-1)

# while processList:
#     p = processList.pop()
#     p.join()

# print(time.time()-start)

# w, h = resolution
# dst = Image.new('RGB', (w, h))
# for i in range(num_gpus):
    
#     img = Image.open(f"CAR{i}.png")
#     img = img.crop((i*w/num_gpus, 0, (i+1)*w/num_gpus, h))
#     dst.paste(img, (i*w//num_gpus, 0))
# dst.save("dst.png")
