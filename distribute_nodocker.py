import docker
import os
from PIL import Image
import time
import threading
import sys
from multiprocessing import Process



def render(gpu, num_gpus, start, end):
    blendfile = "Car_Sci_FI.blend"

    cmd = f"./blender-3.2.1-linux-x64/blender -b {blendfile} --python pyblender_nodocker.py -- {end} {start} {num_gpus} {gpu}"
    os.system(cmd)

num_gpus = 1
processList = []
# resolution = (2560, 1440)s
# render(sys.argv[1], 1, resolution)
start=time.time()
num_frames = 128
for gpu in range(num_gpus):
    # gpu=sys.argv[1]
    p = Process(target=render, args=(gpu, num_gpus, num_frames//num_gpus*gpu, num_frames//num_gpus*(gpu+1)-1))
    p.start()
    processList.append(p)

for pp in processList:
    pp.join()
end=time.time()
print("total time: ", end-start)
