import bpy
import os
import sys
#device config: use GPU and don't use CPU

cyclesPref = bpy.context.preferences.addons["cycles"].preferences
cyclesPref.compute_device_type = "CUDA"       
devices = cyclesPref.get_devices_for_type("CUDA")
for d in devices:
    d.use = (False and d.type == "CPU") or (True and d.type != "CPU")
    # print("CUDA" + " Device:", d["name"], d["use"])

num_gpus = int(os.environ.get("num_gpus"))
gpu = int(os.environ.get("gpuidx"))
MINX=gpu/num_gpus
MAXX=(gpu+1)/num_gpus
MINY=0
MAXY=1

scn = bpy.context.scene
scn.render.image_settings.file_format="PNG"
scn.render.filepath="/host/CAR"+str(gpu)
scn.render.resolution_x = int(os.environ.get("WIDTH"))
scn.render.resolution_y = int(os.environ.get("HEIGHT"))
scn.render.resolution_percentage = 100
scn.render.use_border=True
scn.render.border_min_x = MINX-0.01 if MINX!=0 else MINX
scn.render.border_max_x = MAXX+0.01 if MAXX!=1 else MAXX
scn.render.border_min_y = MINY
scn.render.border_max_y = MAXY
scn.render.engine="CYCLES"
scn.cycles.device='GPU'
bpy.context.scene.cycles.device = "GPU"
scn.frame_set(100)
bpy.ops.render.render(animation=False, write_still=True)
# print(end-start)
# print("time to render on gpu "+os.environ.get("gpuidx")," = ", end-start)

# filepath = scn.render.filepath
# absolutepath = bpy.path.abspath(filepath)
# print(filepath, absolutepath)
