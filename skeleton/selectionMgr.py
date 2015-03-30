#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Selection manager.
#     maintain and manage the list of selected entities
import ogre.io.OIS as OIS
import ogre.renderer.OGRE as ogre
import math

class SelectionMgr:
    def __init__(self, engine):
        self.engine = engine
        self.entMgr = engine.entityMgr
        self.sceneManager = self.engine.gfxMgr.sceneManager
        self.selectedEntIndices = {}
        self.selectedEntIndices[0] = -1
        pass

    def init(self):
    	if len(self.selectedEntIndices) == 0 and len(self.entMgr.entities) > 0:
            self.selectedEntIndices[0] = 0
            print "EntMgr selected: ", str(self.entMgr.entities[self.selectedEntIndices[0]])
            self.entMgr.entities[self.selectedEntIndices[0]].node.showBoundingBox(True)
        self.raySceneQuery = self.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray())
        pass

    def tick(self, dt):
        if self.engine.inputMgr.PRIOR_TAB == False and self.engine.inputMgr.CURRENT_TAB == True and self.engine.inputMgr.keyboard.isKeyDown(OIS.KC_LSHIFT):
            self.shiftSelectNextEnt()
        elif self.engine.inputMgr.PRIOR_TAB == False and self.engine.inputMgr.CURRENT_TAB == True:
            self.selectNextEnt()
        if self.engine.inputMgr.PRIOR_LClick == False and self.engine.inputMgr.CURRENT_LClick == True:
            if self.engine.inputMgr.keyboard.isKeyDown(OIS.KC_LSHIFT):
                self.mouseSelect(self.engine.inputMgr.currMouse, True)
            else:
                self.mouseSelect(self.engine.inputMgr.currMouse, False) 
        pass

    def stop(self):
        pass

    def clearBoundingBoxes(self):
        for i in range(len(self.entMgr.entities)):
            self.entMgr.entities[i].node.showBoundingBox(False)
        
    def shiftSelectNextEnt(self):
        #select the next one to the trailing entity
        if len(self.selectedEntIndices) < len(self.entMgr.entities):
            newEntI = self.findNext()
            self.selectedEntIndices[len(self.selectedEntIndices)] = newEntI
            print "EntMgr selected: ", str(self.entMgr.entities[newEntI])
            self.entMgr.entities[newEntI].node.showBoundingBox(True)

    def findNext(self):
        tempList = []
        for iEnt in self.selectedEntIndices:
            tempList.append(self.selectedEntIndices[iEnt])
        newEntI = max(tempList)
        while newEntI in tempList:
        	newEntI += 1
        	if newEntI == len(self.entMgr.entities):
        		newEntI = 0
        return newEntI

    def selectNextEnt(self):
        #select the next one in line if only 1 entity is selected
        if len(self.selectedEntIndices) == 1:
            self.selectedEntIndices[0] += 1
            print str(self.selectedEntIndices[0])
            if self.selectedEntIndices[0] >= len(self.entMgr.entities) or self.selectedEntIndices[0] < 0:
                self.selectedEntIndices[0] = 0
            print "EntMgr selected: ", str(self.entMgr.entities[self.selectedEntIndices[0]])

        #select the first entity in the list if more than one entity is currently selected
        else:
            self.selectedEntIndices.clear()
            self.selectedEntIndices[0] = 0
            print "EntMgr selected: ", str(self.entMgr.entities[self.selectedEntIndices[0]])
        self.clearBoundingBoxes()
        self.entMgr.entities[self.selectedEntIndices[0]].node.showBoundingBox(True)

    def getSelected(self):
        entList = []
        if self.selectedEntIndices[0] >= 0 and self.selectedEntIndices[0] < len(self.entMgr.entities):
            #return a list of all the selected entities
            for key in self.selectedEntIndices:
                entList.append(self.entMgr.entities[self.selectedEntIndices[key]])
        return entList
    
    def mouseSelect(self, mouseState, shift = False):
        renderWindow = self.engine.inputMgr.renderWindow
        # Setup the ray scene query
        mousePosX = mouseState.X.abs;
        mousePosY = mouseState.Y.abs;
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay( mousePosX / float(renderWindow.getWidth()),
                                                      mousePosY / float(renderWindow.getHeight()))
        print mousePosX / float(renderWindow.getWidth())
        print mousePosY / float(renderWindow.getHeight())
        self.raySceneQuery.setRay(mouseRay)
        self.raySceneQuery.setSortByDistance(True)
        #Get Intersetion with the plane
        result = mouseRay.intersects(ogre.Plane ((0, 1, 0), 0))
        #If there is an intersection
        if result.first:
#            print "HIT"
            intersectingPoint = mouseRay.getPoint(result.second)
            shortestDist = 9999999
            closestEnt = -1
            #look for closest entity using the distance formula
            for key in range(len(self.entMgr.entities)):
                x = (self.entMgr.entities[key].pos.x - intersectingPoint.x) * (self.entMgr.entities[key].pos.x - intersectingPoint.x)
                z = (self.entMgr.entities[key].pos.z - intersectingPoint.z) * (self.entMgr.entities[key].pos.z - intersectingPoint.z)
                tempDist = math.sqrt(x + z)
                print tempDist
                if  tempDist < shortestDist:
                    shortestDist = tempDist
                    closestEnt = key
            #select closest entity
            if closestEnt >= 0:
                if not shift:
                    self.selectedEntIndices.clear()
                    self.clearBoundingBoxes()
                self.selectedEntIndices[len(self.selectedEntIndices)] = closestEnt
                print "EntMgr selected: ", str(self.entMgr.entities[closestEnt])
                self.entMgr.entities[closestEnt].node.showBoundingBox(True)
        pass