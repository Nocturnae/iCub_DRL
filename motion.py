import yarp

yarp.Network.init()

prop = yarp.Property()
prop.put("device", "remote_controlboard")
prop.put("local", "/client/right_arm")
prop.put("remote", "/icubSim/right_arm")

# create remote driver
arm_driver = yarp.PolyDriver(prop)

# query motor control interfaces
i_pos = arm_driver.viewIPositionControl()
i_vel = arm_driver.viewIVelocityControl()
i_enc = arm_driver.viewIEncoders()

# retrieve number of joints
joints = i_pos.getAxes()

print 'Controlling', joints, 'joints...'

# read encoders
encoders = yarp.Vector(joints)
i_enc.getEncoders(encoders.data())

# store as home position
home = yarp.Vector(joints, enc.data())

# initialize a new temp vector identical to encoders
temp = yarp.Vector(joints)

temp.set(0, temp.get(0) + 10)
temp.set(1, temp.get(1) + 10)
temp.set(2, temp.get(2) + 10)

i_pos.positionMove(temp.data())

# wait and restore to initial position
i_pos.positionMove(encoders.data())