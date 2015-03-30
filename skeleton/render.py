#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Simple ORIENTED Physics for 38Engine
# vel is rate of change of pos
# Sushil Louis

from vector import Vector3
import utils
import math

class Renderable:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        #----------position-----------------------------------
        self.ent.node.setPosition(self.ent.pos)
        #------------heading----------------------------------
        self.ent.node.resetOrientation()
        self.ent.node.yaw(self.ent.heading)



