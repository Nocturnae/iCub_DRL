# usr/bin/bash -tt

import bpy
import random
import math
from mathutils import Vector
import os

"""
TODO:
    check collisions
    improve log
"""

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

def check_x(object_name):
	objects = [item.name for item in bpy.data.objects if item.type == "MESH"]
	loc = bpy.data.objects[object_name].location.x
	size = bpy.data.objects[object_name].dimensions.x
	for obj in objects:
		loc2 = bpy.data.objects[obj].location.x
		size2 = bpy.data.objects[obj].dimensions.x
		if abs(loc - loc2) < size + size2:
			return False
	return True

def check_y(object_name):
	objects = [item.name for item in bpy.data.objects if item.type == "MESH"]
	loc = bpy.data.objects[object_name].location.y
	size = bpy.data.objects[object_name].dimensions.y
	for obj in objects:
		loc2 = bpy.data.objects[obj].location.y
		size2 = bpy.data.objects[obj].dimensions.y
		if abs(loc - loc2) < size + size2:
			return False
	return True

def check_z(object_name):
	objects = [item.name for item in bpy.data.objects if item.type == "MESH"]
	loc = bpy.data.objects[object_name].location.z
	size = bpy.data.objects[object_name].dimensions.z
	for obj in objects:
		loc2 = bpy.data.objects[obj].location.z
		size2 = bpy.data.objects[obj].dimensions.z
		if abs(loc - loc2) < size + size2:
			return False
	return True

def check_cog(object_name):
    objects = [item.name for item in bpy.data.objects if item.type == "MESH"]
    for obj in objects:
        #if euclidean_distance(bpy.data.objects[object_name], obj) >= obj.
        pass

def make_material(name, diffuse, specular, alpha):
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = diffuse
	mat.diffuse_shader = 'LAMBERT'
	mat.diffuse_intensity = 1.0
	mat.specular_color = specular
	mat.specular_shader = 'COOKTORR'
	mat.specular_intensity = 0.5
	mat.alpha = alpha
	mat.ambient = 1
	return mat

def color():
    objects = [item for item in bpy.data.objects if item.type == "MESH"]
    for obj in objects:
	    # create random material
	    random_color = make_material('colorName', (random.random(), random.random(), random.random()), (random.random(), random.random(), random.random()), random.random())
	    obj.data.materials.append(random_color)

        
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
        initial_loc = (random.randrange(-5, 5), random.randrange(-5, 5), random.choice(available_levels))
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
            available_levels.append(2 * x)
            cube = create_mesh('Cube', origin, verts, faces)

def save_files(sample_no):
	try:
		dir_path = "/Users/zeynep/Development/iCub_DRL/BlenderGenerator"
		for no in range(1, sample_no + 1):
			os.makedirs(dir_path + "/Samples/sample_" + str(no))
			for s in range(1, len(bpy.data.objects) + 1):
				log(dir_path + "/Samples/sample_" + str(no) + '/scene_info_' + str(s))
	except OSError as e:
		return

def log(filename):
    f = open(filename, 'w')

    for obj in bpy.data.objects.items():
        f.write(obj.type)
        #print(obj[1].type)

    f.write("asdkjaksdj")
        
def run():
    clear_scene()
    add_light()
    random_generate(6)
    color()
    #log("sess.txt")
    return

def attempt():
	save_files(3)

if __name__ == "__main__":  
	attempt()