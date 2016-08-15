import bpy

def clear_scene():
	"""
	delete all existing objects
	"""
	delete_list = [item.name for item in bpy.data.objects if item.type == "MESH" or item.type == "LAMP"]

	for obj in delete_list:
	    bpy.data.objects[obj].select = True

	bpy.ops.object.delete()

	for item in bpy.data.meshes:
	    bpy.data.meshes.remove(item)

def add_light():
	"""
	add light source
	"""
	scene = bpy.context.scene
	lamp_data = bpy.data.lamps.new(name="Lamp", type='POINT')
	lamp_obj = bpy.data.objects.new(name="Lamp", object_data=lamp_data)
	scene.objects.link(lamp_obj)
	lamp_obj.location = (5.0, 5.0, 5.0)
	lamp_obj.select = True
	scene.objects.active = lamp_obj

def run():
	clear_scene()
	add_light()

if __name__ == "__main__":
	run()