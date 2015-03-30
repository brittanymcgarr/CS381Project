#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Entity manager. 
#     Create and keep track of all game entities.
import ent
from vector import Vector3

class EntityMgr:
    def __init__(self, engine):
        self.engine = engine
        self.entities = {}
        self.nEnts = 0
        pass

    def init(self):
    	self.entTypes = [ent.CIGARETTE, ent.CVN68, ent.DDG51, ent.BOAT, ent.BOAT2, ent.SLEEK, ent.MONTEREY, ent.JETSKI, ent.ALIENSHIP, ent.SAILBOAT]
        pass

    def tick(self, dt):
        for i in range(len(self.entities)):
            self.entities[i].tick(dt)
        pass

    def stop(self):
        del self.entities
        pass

    def createGent(self, mid, mmesh, mpos, myaw):
        sceneManager = self.engine.gfxMgr.sceneManager
        e = sceneManager.createEntity(mid, mmesh)
        fileRoot = mmesh.split('.')
        materialName = fileRoot[0]+".material"
        node = sceneManager.getRootSceneNode().createChildSceneNode(mid + 'node', mpos)
        node.attachObject(e)
        return node

    def createEnt(self, entType, pos = Vector3(0,0,0), yaw = 0 ):
        ent = entType(len(self.entities) + 1, pos = pos, yaw = yaw)
        self.entities[self.nEnts] = ent;
        self.nEnts += 1
        #Sushil Louis' Code: Add entity to a node
        gfxNode = self.createGent(ent.uiname + str(ent.eid), ent.mesh, ent.pos, ent.heading)
        ent.node = gfxNode
        return ent