import bpy
import random
import math
import time
import os

BOUNDS_X1 = -4
BOUNDS_X2 = 4
BOUNDS_Y1 = -4
BOUNDS_Y2 = 0

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

INIT_FILE_PATH = "/Users/cemcan/sim.blend"

sample_no = 0

#dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "/Users/zeynep/Desktop"

class RandomDesktopGenerator:

    before = True

    def __init__(self):
        global sample_no
        self.init_scene()
        sample_no += 1

    def init_scene(self):
        self.create_plane()
        pass

    def create_plane(self):
        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.active_object
        plane.location.zero()
        plane.scale = [10000,10000,0]

    def open_init_file(self):
        bpy.ops.wm.open_mainfile(filepath=INIT_FILE_PATH)

    def delete_objects(self):

    	delete_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    	for obj in delete_list:
    	    bpy.data.objects[obj].select = True

    	bpy.ops.object.delete()

    	for item in bpy.data.meshes:
    	    bpy.data.meshes.remove(item)


    def create_mat(self,color):

        mat = bpy.data.materials.new(str(color))
        mat.diffuse_color = color
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = 1
        mat.ambient = 1
        return mat

    def set_mat(self,obj,mat):

        obj.data.materials.append(mat)

    def create_cube(self):

        bpy.ops.mesh.primitive_cube_add()
        return bpy.context.active_object

    def create_cylinder(self):

        bpy.ops.mesh.primitive_cylinder_add()
        bpy.ops.object.shade_smooth()
        return bpy.context.active_object

    def create_cone(self):

        bpy.ops.mesh.primitive_cone_add()
        bpy.ops.object.shade_smooth()
        return bpy.context.active_object

    def put_objects(self):

        available = []

        for i in range(BOUNDS_X1,BOUNDS_X2+1):
            for j in range(BOUNDS_Y1,BOUNDS_Y2+1):
                available.append([i,j,0,0])

        num_objects = random.randint(MIN_NUM_OBJECTS,MAX_NUM_OBJECTS)

        force_towering_here = None

        for i in range(num_objects):

            location = None
            if force_towering_here == None:
                location = random.choice(available)
            else:
                location = force_towering_here
                force_towering_here = None

            location[3] = location[3] + 1

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


            max_offset_x = (1 - o.scale.x)/(8*location[3])
            max_offset_y = (1 - o.scale.y)/(8*location[3])

            offset_x = random.uniform(-max_offset_x,max_offset_x)
            offset_y = random.uniform(-max_offset_y,max_offset_y)
            offset_z = o.scale.z

            if obj_type == 2:

                o.scale = [o.scale.x,o.scale.x,random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)]

                max_offset_xy = (1 - o.scale.z)/(8*location[3])
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

    def randomize_scale(self,obj):

        x = random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)
        y = random.uniform(MIN_OBJECT_SIZE_XY,MAX_OBJECT_SIZE_XY)
        z = random.uniform(MIN_OBJECT_SIZE_Z,MAX_OBJECT_SIZE_Z)

        obj.scale = [x,y,z]

    def reconfigure_objects(self):

        available = []

        for i in range(BOUNDS_X1,BOUNDS_X2+1):
            for j in range(BOUNDS_Y1,BOUNDS_Y2+1):
                available.append([i,j,0,0])

        force_towering_here = None

        for o in bpy.data.objects:

            obj_type = None

            if o.name.startswith('Cu'):
                obj_type = 'CUBE'
            elif o.name.startswith('Cy'):
                obj_type = 'CYLINDER'
            elif o.name.startswith('Co'):
                obj_type = 'CONE'
            else:
                continue

            if force_towering_here == None:
                location = random.choice(available)
            else:
                location = force_towering_here
                force_towering_here = None

            location[3] = location[3] + 1

            o.rotation_euler.zero()


            if (obj_type == 'CYLINDER' or obj_type == 'CUBE') and random.random() < TOWERING_TENDENCY:
                force_towering_here = location

            if (obj_type == 'CONE'):
                available.remove(location)

            max_offset_x = (1 - o.scale.x)/(8*location[3])
            max_offset_y = (1 - o.scale.y)/(8*location[3])

            offset_x = random.uniform(-max_offset_x,max_offset_x)
            offset_y = random.uniform(-max_offset_y,max_offset_y)
            offset_z = o.scale.z

            if obj_type == 'CYLINDER' and o.scale.z < MAX_OBJECT_SIZE_XY and random.random() < 0.7:

                o.rotation_euler.x = math.pi/2

                max_offset_xy = (1 - o.scale.z)/(8*location[3])
                offset_x = random.uniform(-max_offset_xy,max_offset_xy)
                offset_y = random.uniform(-max_offset_xy,max_offset_xy)
                offset_z = o.scale.x

                available.remove(location)
                force_towering_here = None

            o.rotation_euler.z = random.uniform(0,math.pi)

            pos = [location[0]+offset_x,location[1]+offset_y,offset_z+location[2]]

            location[2] = location[2] + 2*o.scale.z

            o.location = pos


    def save_files(self):
    	try:
    		os.makedirs(dir_path + "/Samples/sample_" + str(sample_no))
    	except OSError as e:
    		return

    def save_blender(self):
        if self.before:
            self.render(dir_path + "/Samples/sample_" + str(sample_no) + "/before_" + str(sample_no))
            self.before = False
        else:
            self.render(dir_path + "/Samples/sample_" + str(sample_no) + "/after_" + str(sample_no))
            self.before = True
        self.log(dir_path + "/Samples/sample_" + str(sample_no) + '/scene_info_' + str(sample_no))

    def log(self, filename):
        f = open(filename, 'w')
        item_no = 1

        for obj in bpy.data.objects:
            f.write("Object #" + str(item_no) + "\n")
            item_no += 1
            obj_type = None
            if obj.name.startswith("Cu"):
                obj_type = "CUBE"
            elif obj.name.startswith("Cy"):
                obj_type = "CYLINDER"
            elif obj.name.startswith("Co"):
                obj_type = "CONE"
            else:
                obj_type = "OTHER-" + obj.name

            f.write("Type: " + obj_type + "\n")
            f.write("Location: " + str(obj.location.x) + " " + str(obj.location.y) + " " + str(obj.location.z) + "\n")
            f.write("Rotation: " + str(obj.rotation_euler.x) + " " + str(obj.rotation_euler.y) + " " + str(obj.rotation_euler.z) + "\n")
            f.write("Scale: " + str(obj.scale.x) + " " + str(obj.scale.y) + " " + str(obj.scale.z) + "\n")

            if obj.name != 'Plane' and obj.name != 'Lamp' and obj.name != 'Camera':
                col = obj.data.materials[0].diffuse_color
                f.write("Color: " + str(col[0]) + " " + str(col[1]) + " " + str(col[2]) + "\n")
            else:
                f.write("Color: NA\n")

            f.write("\n")

        f.write("\n")

    def render(self,path):
        bpy.data.scenes["Scene"].render.filepath = path
        bpy.ops.render.render(write_still = True)


if __name__ == "__main__":
    for i in range(1000):
        r  = RandomDesktopGenerator()
        r.put_objects()
        r.save_blender()
        r.reconfigure_objects()
        r.save_blender()
        r.delete_objects()
