import bpy

delete_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

for obj in delete_list:
    bpy.data.objects[obj].select = True

bpy.objs.objects.delete()

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)