import basic as sim_control

wc = sim_control.WorldController()

red_sphere = wc.create_object('ssph', [0.1], [-1, 1, 1], [1, 0, 0])
green_box = wc.create_object('sbox', [0.2, 0.2, 0.2], [0, 1, 1], [0, 1, 0])
blue_cylinder = wc.create_object('scyl', [0.1, 0.1], [1, 1, 1], [0, 0, 1])

wc.move_object(red_sphere, [1, 0.5, 1])
wc.move_object(green_box, [-1, 0.5, 1])
wc.move_object(blue_cylinder, [0, 0.5, 1])

print wc.get_object_location(green_box)

wc.del_all()

monolith = wc.create_object('sbox', [0.8, 1.8, 0.2], [0, 0.9, 1], [0, 0, 0])

del wc
