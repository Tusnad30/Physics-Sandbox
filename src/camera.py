from math import sin, cos, radians
from panda3d.core import Vec3, ClockObject, WindowProperties


class CameraController:
    def __init__(self, base):
        self.base = base

        self.camera_pos = Vec3(0.0, 0.0, 2.0)
        self.camera_front = Vec3(0.0, 1.0, 0.0)
        self.camera_right = Vec3(-1.0, 0.0, 0.0)

        self.mouse_sensitivity = 0.1
        self.jaw = 0
        self.pitch = 0
        self.speed = 15

        base.disableMouse()
        self.globalClock = ClockObject().getGlobalClock()
        base.taskMgr.add(self.updateCam, "update_cam")

        base.accept("escape", self.toggleMouseVis)
        self.mouse_hidden = base.config.GetBool("cursor-hidden", 0)


    def processMouseMovement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.jaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 89:
                self.pitch = 89
            if self.pitch < -89:
                self.pitch = -89

        self.updateCameraVectors()


    def updateCameraVectors(self):
        front = Vec3(0.0, 1.0, 0.0)
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.z = sin(radians(self.pitch))
        front.y = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = front.normalized()
        self.camera_right = (self.camera_front.cross(Vec3(0.0, 0.0, 1.0))).normalized()


    def toggleMouseVis(self):
        if (self.mouse_hidden):
            props = WindowProperties()
            props.setCursorHidden(False)
            self.base.win.requestProperties(props)
            self.mouse_hidden = False
        else:
            props = WindowProperties()
            props.setCursorHidden(True)
            self.base.win.requestProperties(props)
            self.mouse_hidden = True


    def updateCam(self, task):
        dt = self.globalClock.dt

        # mouse input
        if (self.mouse_hidden):
            md = self.base.win.getPointer(0)
            display_center = (self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)
            mouse_pos = (md.getX(), md.getY())
            mouse_move = [mouse_pos[i] - display_center[i] for i in range(2)]

            self.processMouseMovement(-mouse_move[0], -mouse_move[1])

            self.base.win.movePointer(0, display_center[0], display_center[1])


        # keyboard input
        key_down = self.base.mouseWatcherNode.isButtonDown
        if key_down("a"):
            self.camera_pos -= self.camera_right * self.speed * dt
        if key_down("d"):
            self.camera_pos += self.camera_right * self.speed * dt
        if key_down("w"):
            self.camera_pos += self.camera_front * self.speed * dt
        if key_down("s"):
            self.camera_pos -= self.camera_front * self.speed * dt


        # update camera vectors
        self.base.camera.setPos(self.camera_pos)
        self.base.camera.look_at(self.camera_pos + self.camera_front)

        return task.cont