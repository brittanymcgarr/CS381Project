#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Input manager.
#    initialize the keyboard and mouse and setup buffered input.
#    Handle mouse selection and, for now, handle camera movemement
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import platform
from vector import Vector3

class InputMgr():
    def __init__(self, engine):
        self.engine = engine
        self.windowHandle = 0
        self.move = 250
        self.rotate = 0.13
        self.renderWindow = engine.gfxMgr.root.getAutoCreatedWindow()

    def initKeyStates(self):
        #selection manager
        self.CURRENT_TAB = False
        self.PRIOR_TAB = False
        self.CURRENT_LClick = False
        self.PRIOR_LClick = False
        #CAMERA
        self.CURRENT_W = False
        self.PRIOR_W = False
        self.CURRENT_A = False
        self.PRIOR_A = False
        self.CURRENT_S = False
        self.PRIOR_S = False
        self.CURRENT_D = False
        self.PRIOR_D = False
        self.CURRENT_PGUP = False
        self.PRIOR_PGUP = False
        self.CURRENT_PGDN = False
        self.PRIOR_PGDN = False
        

    def init(self):
        self.initKeyStates()
        self.camNode = self.engine.gfxMgr.camera.parentSceneNode.parentSceneNode
        int64 = False
        for bit in platform.architecture():
            if '64' in bit:
                int64 = True
        if int64:
            self.windowHandle = self.renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        else:
            self.windowHandle = self.renderWindow.getCustomAttributeInt("WINDOW")
        paramList = [("WINDOW", str(self.windowHandle))]
        t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "false")]
        paramList.extend(t)
        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, False)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, False)
        except Exception, e:
            raise e

    def tick(self, dt):
        self.keyboard.capture()
        self.mouse.capture()
        currMouse = self.mouse.getMouseState()
        self.currMouse = currMouse
        #TAB KEY
        self.PRIOR_TAB = self.CURRENT_TAB
        if self.keyboard.isKeyDown(OIS.KC_TAB):
            self.CURRENT_TAB = True
        else:
            self.CURRENT_TAB = False
        #Left Mouse Click
        self.PRIOR_LClick = self.CURRENT_LClick
        if currMouse.buttonDown(OIS.MB_Left):
            self.CURRENT_LClick = True
        else:
            self.CURRENT_LClick = False
        # Move the camera using keyboard input.
        transVector = Vector3(0.0,0.0,0.0)
        # Move Forward.
        if self.keyboard.isKeyDown(OIS.KC_W):
           transVector.z -= self.move
        # Move Backward.
        if self.keyboard.isKeyDown(OIS.KC_S):
            transVector.z += self.move
        # Strafe Left.
        if self.keyboard.isKeyDown(OIS.KC_A):
            transVector.x -= self.move
        # Strafe Right.
        if self.keyboard.isKeyDown(OIS.KC_D):
           transVector.x += self.move
        #YAW Q - Counter-clockwise
        if self.keyboard.isKeyDown(OIS.KC_Q):
           self.camNode.yaw(ogre.Degree(self.rotate * self.move * dt).valueRadians())
        #YAW E - Clockwise
        if self.keyboard.isKeyDown(OIS.KC_E):
           self.camNode.yaw(ogre.Degree(-self.rotate * self.move * dt).valueRadians())
        #Pitch Z - Up
        if self.keyboard.isKeyDown(OIS.KC_Z):
           self.camNode.getChild(0).pitch(ogre.Degree(self.rotate * self.move * dt).valueRadians())
        #Pitch X - Down
        if self.keyboard.isKeyDown(OIS.KC_X):
           self.camNode.getChild(0).pitch(ogre.Degree(-self.rotate * self.move * dt).valueRadians())
        # Move Up.        
        if self.keyboard.isKeyDown(OIS.KC_PGUP):
            transVector.y += self.move
        # Move Down.
        if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
            transVector.y -= self.move
        #ESCAPE KEY
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.keepRunning = False
        # Translate the camera based on time.
        self.camNode.translate(self.camNode.orientation
                              * transVector
                              * dt)
 
        # Rotate the camera when the Right mouse button is down.
        if currMouse.buttonDown(OIS.MB_Right):
           self.camNode.yaw(ogre.Degree(-self.rotate 
                            * currMouse.X.rel).valueRadians())
           self.camNode.getChild(0).pitch(ogre.Degree(-self.rotate
                                          * currMouse.Y.rel).valueRadians())

    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None