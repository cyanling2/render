import bpy
import os
import time
import sys


start=time.time()
cyclesPref = bpy.context.preferences.addons["cycles"].preferences
cyclesPref.compute_device_type = "CUDA"       
devices = cyclesPref.get_devices_for_type("CUDA")

gpu=int(sys.argv[-1])
num_gpus=int(sys.argv[-2])
end=int(sys.argv[-4])
start=int(sys.argv[-3])
animation=int(sys.argv[-5])

for i in range(len(devices)):
    devices[i].use = (False and i!=gpu) or (True and i==gpu)
    print("CUDA" + " Device:", devices[i]["id"], devices[i]["use"])

MINX=gpu/num_gpus
MAXX=(gpu+1)/num_gpus
MINY=0
MAXY=1

print(start, end)


scn = bpy.context.scene
scn.render.filepath="./nodocker_"+str(gpu)
scn.render.resolution_x = 1280
scn.render.resolution_y = 720
scn.render.resolution_percentage = 100
if not animation:
    scn.render.use_border=True
    scn.render.border_min_x = MINX
    scn.render.border_max_x = MAXX
    scn.render.border_min_y = MINY
    scn.render.border_max_y = MAXY
    scn.frame_set(100)
    scn.render.image_settings.file_format="PNG"
else:
    scn.frame_start = start
    scn.frame_end = end
scn.render.engine="CYCLES"
scn.cycles.device='GPU'
bpy.context.scene.cycles.device = "GPU"
bpy.ops.render.render(animation=animation, write_still=True)
end=time.time()