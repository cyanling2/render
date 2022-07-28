import bpy
import os
import sys
import time
#device config: use GPU and don't use CPU
start=time.time()
cyclesPref = bpy.context.preferences.addons["cycles"].preferences
cyclesPref.compute_device_type = "CUDA"       
devices = cyclesPref.get_devices_for_type("CUDA")
for d in devices:
    d.use = (False and d.type == "CPU") or (True and d.type != "CPU")
    # print("CUDA" + " Device:", d["name"], d["use"])


num_gpus = int(os.environ.get("num_gpus"))
gpu = int(os.environ.get("gpuidx"))
animation = int(os.environ.get("ANIMATION"))
MINX = gpu/num_gpus if not animation else 0
MAXX = (gpu+1)/num_gpus if not animation else 1
MINY = 0
MAXY = 1

scn = bpy.context.scene
scn.render.filepath="/host/"
scn.render.resolution_x = int(os.environ.get("WIDTH"))
scn.render.resolution_y = int(os.environ.get("HEIGHT"))
scn.render.resolution_percentage = 100
if not animation:
    scn.render.use_border=True
    scn.render.border_min_x = MINX-0.01 if MINX!=0 else MINX
    scn.render.border_max_x = MAXX+0.01 if MAXX!=1 else MAXX
    scn.render.border_min_y = MINY
    scn.render.border_max_y = MAXY
    scn.render.image_settings.file_format="PNG"
    scn.frame_set(100)
else:
    scn.frame_start = int(os.environ.get("START_FRAME"))
    scn.frame_end = int(os.environ.get("END_FRAME"))
scn.render.engine="CYCLES"
scn.cycles.device='GPU'
bpy.context.scene.cycles.device = "GPU"
bpy.ops.render.render(animation=animation, write_still=True)
with open("time.txt", "w") as f:
    f.write(str(time.time()-start)+"\n")
