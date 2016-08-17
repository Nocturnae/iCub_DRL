import bpy
import random
import math

BOUNDS_X = 5
BOUNDS_Y = 7

MIN_NUM_OBJECTS = 3
MAX_NUM_OBJECTS = 7

MIN_OBJECT_SIZE_XY = 0.1
MIN_OBJECT_SIZE_Z = 0.1
MAX_OBJECT_SIZE_XY = 0.3
MAX_OBJECT_SIZE_Z = 0.5

WEIGHT_CUBES = 5
WEIGHT_CYLINDERS_TOWERABLE = 3
WEIGHT_CONES = 1
WEIGHT_CYLINDERS = 1

TOWERING_TENDENCY = 0.3

class RandomSceneGenerator:

	objects = None
	available_levels = None

	def __init__(self):
		self.init_scene()
		self.objects = []
		self.available_levels = []

	def init_scene(self):
		self.clear_scene()
		self.add_light()

	def clear_scene(self):
		"""
		delete all existing objects
		"""
		delete_list = [item.name for item in bpy.data.objects if item.type == "MESH" or item.type == "LAMP"]

		for obj in delete_list:
			bpy.data.objects[obj].select = True

		for item in bpy.data.meshes:
			bpy.data.meshes.remove(item)

		self.objects = None
		self.available_levels = None

	def add_light(self):
		"""
		add a point light source
		"""
		scene = bpy.context.scene
		lamp_data = bpy.data.lamps.new(name="Lamp", type='POINT')
		lamp_obj = bpy.data.objects.new(name="Lamp", object_data=lamp_data)
		scene.objects.link(lamp_obj)
		lamp_obj.location = (5.0, 5.0, 5.0)
		lamp_obj.select = True
		scene.objects.active = lamp_obj

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

	def create_cube(self):

        bpy.ops.mesh.primitive_cube_add()
        return bpy.context.active_object

    def set_mat(self,obj,mat):
		obj.data.materials.append(mat)

    def create_cylinder(self):

        bpy.ops.mesh.primitive_cylinder_add()
        bpy.ops.object.shade_smooth()
        return bpy.context.active_object

    def create_cone(self):

        bpy.ops.mesh.primitive_cone_add()
        bpy.ops.object.shade_smooth()
        return bpy.context.active_object

    def randomize_scale(self,obj):

        x = random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)
        y = random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)
        z = random.uniform(MIN_OBJECT_SIZE_Z,MAX_OBJECT_SIZE_Z)

        obj.scale = [x,y,z]

	def random_generate(self):
		available = []

        for i in range(BOUNDS_X):
            for j in range(BOUNDS_Y):
                available.append([i,j,0])

        num_objects = random.randint(MIN_NUM_OBJECTS,MAX_NUM_OBJECTS)

        force_towering_here = None

        for i in range(num_objects):

            location = None
            if force_towering_here == None:
                location = random.choice(available)
            else:
                location = force_towering_here
                force_towering_here = None

            obj_type = random.randint(0,3)

            o = None

            if obj_type == 0:

                o = self.create_cube()
                self.randomize_scale(o)
                if random.random() < TOWERING_TENDENCY:
                    force_towering_here = location

            elif obj_type == 1:

                o = self.create_cylinder()
                self.randomize_scale(o)
                o.scale = [o.scale.x,o.scale.x,o.scale.z]

                if random.random() < TOWERING_TENDENCY:
                    force_towering_here = location

            elif obj_type == 2:

                o = self.create_cylinder()
                self.randomize_scale(o)
                o.scale = [o.scale.x,o.scale.x,o.scale.z]

                available.remove(location)

            elif obj_type == 3:

                o = self.create_cone()
                self.randomize_scale(o)
                o.scale = [o.scale.x,o.scale.x,o.scale.z]

                available.remove(location)


            max_offset_x = (1 - o.scale.x)/8
            max_offset_y = (1 - o.scale.y)/8

            offset_x = random.uniform(-max_offset_x,max_offset_x)
            offset_y = random.uniform(-max_offset_y,max_offset_y)
            offset_z = o.scale.z

            if obj_type == 2:

                o.scale = [o.scale.x,o.scale.x,random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)]

                max_offset_xy = (1 - o.scale.z)/8
                offset_x = random.uniform(-max_offset_xy,max_offset_xy)
                offset_y = random.uniform(-max_offset_xy,max_offset_xy)
                offset_z = o.scale.x

                o.rotation_euler.x = math.pi/2

            o.rotation_euler.z = random.uniform(0,math.pi)

            pos = [location[0]+offset_x,location[1]+offset_y,offset_z+location[2]]

            location[2] = location[2] + 2*o.scale.z

            o.location = pos
            r = random.random()
            g = random.random()
            b = random.random()
            self.set_mat(o,self.create_mat([r,g,b]))
