import bpy
import random
import math
from mathutils import Vector

#grid_size = 
available_levels = [0.0]
objects = []

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

def check_for_collision():
    pass

def color():
    objects = [item.name for item in bpy.data.objects if item.type == "MESH"]

def create_mesh(name, origin, verts, faces):
	"""
	create mesh and add it to scene
	"""
	mesh = bpy.data.meshes.new(name + 'Mesh')
	obj = bpy.data.objects.new(name, mesh)
	obj.location = origin
	obj.show_name = True

	scene = bpy.context.scene
	scene.objects.link(obj)
	scene.objects.active = obj
	obj.select = True

	mesh.from_pydata(verts, [], faces)

	mesh.update()

	return obj

def random_generate(num):
    while num:
        num -= 1
        initial_loc = (random.randrange(-5, 5), random.randrange(-5, 5), 0)
        origin = Vector(initial_loc)
        (x, y, z) = (random.random(), random.random(), random.random())
        choose_shape = math.floor(random.randrange(0, 3))
        if choose_shape == 0:
            verts = ((x,x,-1), (x,-x,-1), (-x,-x,-1), (-x,x,-1), (0,0,1))
            faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
            cone = create_mesh('Cone', origin, verts, faces)
        else:
            verts = [(x, x, -x),(x, -x, -x),(-x, -x, -x),(-x, x, -x),(x, x, x),(x, -x, x),(-x, -x, x),(-x, x, x)]
            faces = [(0, 1, 2, 3),(4, 7, 6, 5),(0, 4, 5, 1),(1, 5, 6, 2),(2, 6, 7, 3),(4, 0, 3, 7)]
            cube = create_mesh('Cube', origin, verts, faces)

def log():
    f = open('session.txt', 'w')
    for obj in objects:
        f.write(obj.type)
        
def run():
    clear_scene()
    add_light()
    random_generate(6)
    #log('session.txt')
    log()
    return

if __name__ == "__main__":  
	run()