from panda3d.core import DirectionalLight, AmbientLight, Vec3

class Lighting():
    def __init__(self, base, sun_direction = (0.5, -0.75, -1.0), sun_color = (0.9, 0.8, 0.7, 1.0), ambient_color = (0.3, 0.4, 0.5, 1.0), resolution = 2048, range = 50):

        self.base = base
        self.range = range

        # directional light
        self.dlight = DirectionalLight("dlight")
        self.dlight.setColor(sun_color)

        if (resolution):
            self.dlight.setShadowCaster(True, resolution, resolution, -2000)
            dl_lens = self.dlight.getLens()
            dl_lens.setNearFar(-200, 100)
            dl_lens.setFilmSize((range, range))

        self.dlnp = self.base.render.attachNewNode(self.dlight)
        self.dlnp.lookAt(sun_direction)
        self.base.render.setLight(self.dlnp)

        # ambient light
        self.alight = AmbientLight("alight")
        self.alight.setColor(ambient_color)

        alnp = self.base.render.attachNewNode(self.alight)
        self.base.render.setLight(alnp)

        # generate shaders
        self.base.render.setShaderAuto()

        if (resolution):
            base.taskMgr.add(self.update, "update_shadow")
    
    def update(self, task):
        self.dlnp.setPos(self.base.camera.getPos(self.base.render) + self.base.render.getRelativeVector(self.base.camera, Vec3.forward()) * self.range * 0.5)

        return task.cont