#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Graphics manager. 
#   initialize python ogre graphics 
#   (as in Tutorial 6), initialize the camera, 
#   and initialize the scene (water plane). 
#   This class' tick function calls python ogre's renderOneFrame
#   as shown in Tutorial 6
#   Zachary Carlson
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class GfxMgr:
    def __init__(self, engine):
        self.engine = engine
        self.createRoot()

    def createRoot(self):
        self.root = ogre.Root("plugins.cfg", "resources2.cfg", "textput.log" )
        #self.root = ogre.Root
        pass

    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")
 
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
 
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
    
    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
    def createRenderWindow(self):
        self.root.initialise(True, "CS381 Render Window")
 
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
    def setupScene(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")
        #Camera
        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 5
        viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        node = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode1',
                                                               (-400, 200, 400))
        node.yaw(ogre.Degree(-45))
        node = node.createChildSceneNode('PitchNode1')
        node.attachObject(self.camera)
        # Setup a scene with a low level of ambient light.
        self.sceneManager.ambientLight = 1, 1, 1
 
        # Setup a ground plane.
        plane = ogre.Plane ((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton ()
        self.plane = meshManager.createPlane ('Ground', 'General', plane,
                                     10000, 10000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (ent)
        ent.setMaterialName ('OceanCg')
        ent.castShadows = False
 
        #self.sceneManager.setSkyBox (True, "Examples/MorningSkyBox", 5000, False)
        self.sceneManager.setSkyDome (True, "Examples/CloudySky", 5, 8)

#Primary Functions
    def init(self):
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()
        pass

    def tick(self, dt):
        self.root.renderOneFrame()
        pass

    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        del self.root