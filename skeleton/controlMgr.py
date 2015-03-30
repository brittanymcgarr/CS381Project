#######
#AS5
#Name: Zachary Carlson
#Partner: Brittany McGarr
#######
# Control manager.
#    handle entity control through the arrow keys on the keyboard. The
#    arrow keys on your keyboard control all selected entities. Up/Down 
#    will increase and decrease desiredSpeed in the current direction of 
#    motion. Left/Right arrow keys turn the entity, they change the entity's
#    desiredHeading.
import ogre.io.OIS as OIS

class ControlMgr:
    def __init__(self, engine):
        self.engine = engine
        pass

    def init(self):
        self.entMgr = self.engine.entityMgr
        self.selMgr = self.engine.selectionMgr
        self.keyboard = self.engine.inputMgr.keyboard
        self.toggle = 0.0
        pass

    def tick(self, dt):
    	# Update the toggle timer.
        if self.toggle >= 0:
            self.toggle -= dt

        import utils
        entList = self.selMgr.getSelected()
        if entList:
            for selectedEnt in entList:
                #change desired speed and current direction
                #------------------------------------------
                # Speed Up
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_UP):
                    selectedEnt.desiredSpeed = utils.clamp(selectedEnt.desiredSpeed + selectedEnt.deltaSpeed, 0, selectedEnt.maxSpeed)
                    print "Speeding UP", selectedEnt.desiredSpeed

                # Slow down
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_DOWN):
                    selectedEnt.desiredSpeed = utils.clamp(selectedEnt.desiredSpeed - selectedEnt.deltaSpeed, 0, selectedEnt.maxSpeed)
                    print "Slowing down", selectedEnt.desiredSpeed

                # Turn Left.
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_LEFT):
                    selectedEnt.desiredHeading += selectedEnt.deltaYaw
                    selectedEnt.desiredHeading = utils.fixAngle(selectedEnt.desiredHeading)
                    print "Turn left", selectedEnt.desiredHeading

                # Turn Right.
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_RIGHT):
                    selectedEnt.desiredHeading -= selectedEnt.deltaYaw
                    selectedEnt.desiredHeading = utils.fixAngle(selectedEnt.desiredHeading)
                    print "Turn right", selectedEnt.desiredHeading
            if self.toggle < 0:
                toggle = 0.2
        pass

    def stop(self):
        pass