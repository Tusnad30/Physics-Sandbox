from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import loadPrcFile, loadPrcFileData, Vec3, ClockObject, SamplerState, Texture, TextureStage, NodePath, AntialiasAttrib
from panda3d.bullet import BulletWorld, BulletDebugNode, BulletHingeConstraint

from camera import CameraController
from lighting import Lighting
from physics import Physics


class Application(ShowBase):
    def __init__(self, window_resolution = (1280, 720), shadow_resolution = (2048, 50), msaa = 0, vsync = 1):
        
        loadPrcFile("config/config.prc")

        config_data = f"""
        win-size {window_resolution[0]} {window_resolution[1]}
        sync-video {vsync}
        """
        loadPrcFileData("Config Data", config_data)


        super().__init__()


        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))

        if self.config.GetBool("bullet-debug-render", 0):
            debugNode = BulletDebugNode("debug_collider")
            debugNode.showWireframe(True)
            debugNode.showConstraints(True)
            debugNode.showBoundingBoxes(False)
            debugNode.showNormals(False)
            debugNP = self.render.attachNewNode(debugNode)
            debugNP.show()
            self.bullet_world.setDebugNode(debugNP.node())


        self.camera_controller = CameraController(self)
        
        
        self.camLens.setFov(90)
        self.camLens.setNearFar(0.1, 1000)

        self.setBackgroundColor(0.6, 0.8, 1.0, 1.0)

        self.lighting = Lighting(self, resolution = shadow_resolution[0], range = shadow_resolution[1])

        filter = CommonFilters(self.win, self.cam)
        filter.setSrgbEncode()
        
        if (msaa):
            filter.setMSAA(msaa)
            self.render.setAntialias(AntialiasAttrib.MMultisample)

        self.taskMgr.add(self.update, "update_main")
        self.globalclock = ClockObject().getGlobalClock()


        self.accept("x", self.spawnCube)
        self.accept("c", self.shootCube)
        self.accept("v", self.spawnManyCubes)
        self.accept("b", self.spawnTower)
        self.accept("space", self.spawnBomb)
        self.accept("g", self.removeCubes)
        self.accept("q", self.toggleSloMo)

        self.time_mul = 1.0


        self.grid_texture = self.loader.loadTexture("textures/grid.png")
        self.grid_texture.setMagfilter(SamplerState.FT_linear)
        self.grid_texture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        self.grid_texture.setWrapU(Texture.WM_repeat)
        self.grid_texture.setWrapV(Texture.WM_repeat)
        self.grid_texture.setAnisotropicDegree(4)


        floor = self.loader.loadModel("models/cube.egg")
        floor.setScale((150.0, 150.0, 0.5))
        floor.setPos((0.0, 0.0, -0.25))
        floor.setTexture(self.grid_texture)
        floor.setTexScale(TextureStage.getDefault(), 5, 5)
        floor.reparentTo(self.render)
        floor_col = Physics.applyBoxCollider(self, floor)

        backup_floor = NodePath("backup_floor")
        backup_floor.setPos((0.0, 0.0, -0.25))
        backup_floor_col = Physics.applyPlaneCollider(self, backup_floor)

        ramp = self.loader.loadModel("models/ramp.egg")
        ramp.setPos((-30.0, 0.0, 0.0))
        ramp.setTexture(self.grid_texture)
        ramp.setTexScale(TextureStage.getDefault(), 4, 4)
        ramp.reparentTo(self.render)
        ramp_col = Physics.applyMeshCollider(self, ramp)


        spin_platform = self.loader.loadModel("models/cube.egg")
        spin_platform.setTexture(self.grid_texture)
        spin_platform.setTexScale(TextureStage.getDefault(), 2/3, 2/3)
        spin_platform.setColorScale((0.1, 0.3, 1.0, 1.0))
        spin_platform.reparentTo(self.render)
        spin_col = Physics.applyDynamicBoxCollider(self, spin_platform, mass = 10000.0)
        spin_col.setScale(20.0, 20.0, 1.0)
        spin_col.setPos((0.0, -30.0, 0.5))

        spin_constraint = BulletHingeConstraint(spin_col.node(), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        spin_constraint.enableAngularMotor(True, 1.0, 10000.0)
        self.bullet_world.attachConstraint(spin_constraint)


        blend_border = self.loader.loadModel("models/blender.egg")
        blend_border.setPos((30.0, 0.0, 0.0))
        blend_border.setTexture(self.grid_texture)
        blend_border.setTexScale(TextureStage.getDefault(), 2, 2)
        blend_border.reparentTo(self.render)
        blend_border_col = Physics.applyMeshCollider(self, blend_border)

        blender = self.loader.loadModel("models/cube.egg")
        blender.setTexture(self.grid_texture)
        blender.setTexScale(TextureStage.getDefault(), 2/3, 2/3)
        blender.setColorScale((0.1, 0.3, 1.0, 1.0))
        blender.reparentTo(self.render)
        blender_col = Physics.applyDynamicBoxCollider(self, blender, mass = 10000.0)
        blender_col.setScale(21.0, 1.0, 5.0)
        blender_col.setPos((30.0, 0.0, 2.5))

        blender_constraint = BulletHingeConstraint(blender_col.node(), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        blender_constraint.enableAngularMotor(True, 1.0, 10000.0)
        self.bullet_world.attachConstraint(blender_constraint)


        seesaw_base = self.loader.loadModel("models/cube.egg")
        seesaw_base.setPos((15.0, 33.0, 2.0))
        seesaw_base.setScale((1.0, 1.0, 4.0))
        seesaw_base.setTexture(self.grid_texture)
        seesaw_base.setTexScale(TextureStage.getDefault(), 2, 2)
        seesaw_base.reparentTo(self.render)
        blend_border_col = Physics.applyBoxCollider(self, seesaw_base)

        seesaw = self.loader.loadModel("models/cube.egg")
        seesaw.setTexture(self.grid_texture)
        seesaw.setTexScale(TextureStage.getDefault(), 2/3, 1/6)
        seesaw.setColorScale((0.1, 0.3, 1.0, 1.0))
        seesaw.reparentTo(self.render)
        seesaw_col = Physics.applyDynamicBoxCollider(self, seesaw, mass = 100.0)
        seesaw_col.setScale(20.0, 5.0, 1.0)
        seesaw_col.setPos((15.0, 30.0, 3.5))

        seesaw_constraint = BulletHingeConstraint(seesaw_col.node(), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        self.bullet_world.attachConstraint(seesaw_constraint)


        turbine = self.loader.loadModel("models/cube.egg")
        turbine.setTexture(self.grid_texture)
        turbine.setTexScale(TextureStage.getDefault(), 2/3, 2/3)
        turbine.setColorScale((0.1, 0.3, 1.0, 1.0))
        turbine.reparentTo(self.render)
        turbine_col = Physics.applyDynamicBoxCollider(self, turbine, mass = 500.0)
        turbine_col.setScale(20.0, 1.0, 5.0)
        turbine_col.setPos((-20.0, 30.0, 2.5))

        turbine_constraint = BulletHingeConstraint(turbine_col.node(), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        self.bullet_world.attachConstraint(turbine_constraint)


        self.cube_array = []


    def spawnCube(self):
        cube = self.loader.loadModel("models/cube.egg")
        cube.setTexture(self.grid_texture)
        cube.setTexScale(TextureStage.getDefault(), 0.4, 0.4)
        cube.setColorScale((1.0, 0.1, 0.1, 1.0))
        cube.reparentTo(self.render)
        cube_col = Physics.applyDynamicBoxCollider(self, cube)
        cube_col.setPos(self.camera.getPos(self.render) + self.render.getRelativeVector(self.camera, Vec3.forward()) * 4.0)

        self.cube_array.append((cube, cube_col))

    def shootCube(self):
        cube = self.loader.loadModel("models/cube.egg")
        cube.setTexture(self.grid_texture)
        cube.setTexScale(TextureStage.getDefault(), 0.4, 0.4)
        cube.setColorScale((1.0, 0.1, 0.1, 1.0))
        cube.reparentTo(self.render)
        cube_col = Physics.applyDynamicBoxCollider(self, cube)
        cube_col.setPos(self.camera.getPos(self.render) + self.render.getRelativeVector(self.camera, Vec3.forward()) * 4.0)
        cube_col.node().setLinearVelocity(self.render.getRelativeVector(self.camera, Vec3.forward()) * 40.0)

        self.cube_array.append((cube, cube_col))

    def spawnManyCubes(self):
        for i in range(100):
            cube = self.loader.loadModel("models/cube.egg")
            cube.setTexture(self.grid_texture)
            cube.setTexScale(TextureStage.getDefault(), 0.4, 0.4)
            cube.setColorScale((1.0, 0.1, 0.1, 1.0))
            cube.reparentTo(self.render)
            cube_col = Physics.applyDynamicBoxCollider(self, cube)
            cube_col.setPos(self.camera.getPos(self.render) + Vec3(0, 0, i) + self.render.getRelativeVector(self.camera, Vec3.forward()) * 4.0)

            self.cube_array.append((cube, cube_col))

    def spawnTower(self):
        for x in range(8):
            for y in range(8):
                for z in range(14):
                    cube = self.loader.loadModel("models/cube.egg")
                    cube.setTexture(self.grid_texture)
                    cube.setTexScale(TextureStage.getDefault(), 0.4, 0.4)
                    cube.setColorScale((1.0, 0.1, 0.1, 1.0))
                    cube.reparentTo(self.render)
                    cube_col = Physics.applyDynamicBoxCollider(self, cube)
                    cube_col.setPos(Vec3(-4, -4, 0.5) + Vec3(x, y, z))

                    self.cube_array.append((cube, cube_col))

    def spawnBomb(self):
        cube = self.loader.loadModel("models/sphere.egg")
        cube.setTexture(self.grid_texture)
        cube.setTexScale(TextureStage.getDefault(), 0.4, 0.4)
        cube.setColorScale((0.4, 0.4, 0.4, 1.0))
        cube.reparentTo(self.render)
        cube_col = Physics.applyDynamicSphereCollider(self, cube, mass = 100.0)
        cube_col.setPos(self.camera.getPos(self.render) + self.render.getRelativeVector(self.camera, Vec3.forward()) * 4.0)
        cube_col.node().setLinearVelocity(self.render.getRelativeVector(self.camera, Vec3.forward()) * 10.0)

        self.taskMgr.doMethodLater(3.0, self.detonate, "detonate", extraArgs = [cube_col], appendTask=True)

    def detonate(self, col, task):
        for i in range(len(self.cube_array)):
            cube = self.cube_array[i][1]

            cube_pos = cube.getPos(self.render)
            direction = Vec3(cube_pos - col.getPos(self.render)).normalized()

            cube.setZ(cube.getZ() + 0.01) # make cube dynamic again by doing this weird method
            cube.node().setLinearVelocity(direction * 40.0)

        self.bullet_world.removeRigidBody(col.node())
        col.removeNode()

        return task.done
    
    def removeCubes(self):
        for i in range(len(self.cube_array)):
            cube_col = self.cube_array[i][1]
            self.bullet_world.removeRigidBody(cube_col.node())
            cube_col.removeNode()

        self.cube_array = []

    def toggleSloMo(self):
        if (self.time_mul == 1.0):
            self.time_mul = 0.2
        else:
            self.time_mul = 1.0


    def update(self, task):
        dt = self.globalclock.dt

        self.bullet_world.doPhysics(dt * self.time_mul)

        return task.cont