'''
Display images or animations using Taichi GUI (WIP)
'''

import taichi as ti
import time
import os


@ti.data_oriented
class Animation:
    '''
    Handy Shadertoy-alike GUI base class.

    I'm able to:

    1. Enable you to focus on computation, no need to hand-write a GUI event loop.

    2. Easy-to-use image / video export wrapper like ``self.set_output_video(path)``.

    3. Shadertoy-alike input variables including ``self.iMouse``, ``self.iKeyDirection``.

    4. Callback style event processing system incuding ``self.on_click(x, y)``.

    See `examples/export_video.py <https://github.com/taichi-dev/taichi_glsl/blob/master/examples/export_video.py>`_ for example:

    .. code-block:: python

        import taichi as ti
        import taichi_glsl as ts

        ti.init()


        class MyAnimation(ts.Animation):
            def on_init(self):
                self.img = ti.Vector(3, ti.f32, (512, 512))
                self.set_output_video('/tmp/video.gif')
                self.define_input()

            @ti.kernel
            def on_render(self):
                for I in ti.grouped(self.img):
                    uv = I / self.iResolution
                    self.img[I] = ti.cos(uv.xyx + self.iTime +
                                         ts.vec(0, 2, 4)) * 0.5 + 0.5


        MyAnimation().start()

    And what's more, `examples/particles.py <https://github.com/taichi-dev/taichi_glsl/blob/master/examples/particles.py>`_:

    .. code-block:: python

        import taichi as ti
        import taichi_glsl as ts

        ti.init()


        class MyAnimation(ts.Animation):
            def on_init(self):
                self.N = 8192
                self.dt = 0.01
                self.pos = ti.Vector(2, ti.f32, self.N)
                self.vel = ti.Vector(2, ti.f32, self.N)
                self.circles = self.pos  # alias to make ts.Animation know
                self.attract_strength = ti.var(ti.f32, ())
                self.attract_pos = ti.Vector(2, ti.f32, ())
                self.resolution = (512, 512)
                self.title = 'Particles'
                self.define_input()

            @ti.kernel
            def on_start(self):
                for i in self.pos:
                    self.pos[i] = ts.randND(2)
                    self.vel[i] = ts.randSolid2D()

            @ti.kernel
            def on_advance(self):
                for i in self.pos:
                    acc = ts.vec(0.0, -1.0)
                    if any(self.iKeyDirection):  # ASWD?
                        acc = self.iKeyDirection
                    if any(self.iMouseButton):
                        dir = ts.normalize(self.iMouse - self.pos[i]) * 2
                        if self.iMouseButton[0]:  # LMB pressed?
                            acc += dir
                        if self.iMouseButton[1]:  # RMB pressed?
                            acc -= dir
                    self.vel[i] += acc * self.dt
                for i in self.pos:
                    self.vel[i] = ts.boundReflect(self.pos[i], self.vel[i], 0, 1, 0.8)
                for i in self.pos:
                    self.pos[i] += self.vel[i] * self.dt


        MyAnimation().start()
    '''
    def __init__(self,
                 img=None,
                 circles=None,
                 title='Animation',
                 res=(512, 512)):
        self.title = title
        self.img = img
        self.circles = circles
        self.circle_color = 0xffffff
        self.circle_radius = 1
        self.background_color = 0x000000
        self.gui = None
        self.has_input = False
        self.screenshot_dir = None
        self.output_video = None
        self.start_time = time.time()
        self._resolution = res
        self.on_init()

    def set_output_video(self, path, framerate=24):
        '''
        Export frames painted in GUI to a video.

        FIXME: Only work for ``self.img`` render, doesn't work for ``self.circles`` for now.
        Use ``self.screenshot_dir = '/tmp'``, then ``cd /tmp && ti video`` if you wish to.
        '''
        output_dir = os.path.dirname(path)
        output_file = os.path.basename(path)
        try:
            output_ext = output_file.split(os.path.extsep)[-1]
            assert output_ext in ['gif', 'mp4']
        except:
            output_ext = None
        self.video_manager = ti.VideoManager(output_dir,
                                             framerate=framerate,
                                             automatic_build=False)
        self.video_manager.taichi_glsl_output_ext = output_ext

        def _get_output_filename(suffix):
            if output_ext is not None:
                return path[:-(len(output_ext) + 1)] + suffix
            else:
                return path + suffix

        self.video_manager.get_output_filename = _get_output_filename

    def on_init(self):
        '''
        Called when initializing ``Animation()``.

        Set up self.* properties for application usage here:

        +--------------------+--------------+-----------------+-------------------------------+
        | Property           | Type         | Default         | Description                   |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``img``            | ``np.array`` | ``None``        | Image to display.             |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``circles``        | ``np.array`` | ``None``        | Circles to paint.             |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``circle_radius``  |   scalar     | ``1``           | Radius of circles.            |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``circle_color``   |   RGB hex    | ``0x000000``    | Color of circles.             |
        +--------------------+--------------+-----------------+-------------------------------+
        |``background_color``|   RGB hex    | ``0x000000``    | background color of window.   |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``title``          |   string     | ``"Animation"`` | Title of the window.          |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``screenshot_dir`` |   boolean    | ``None``        | Path to save screenshots.     |
        +--------------------+--------------+-----------------+-------------------------------+
        | ``resolution``     |   tuple      | ``img.shape()`` | The size of window / screen.  |
        +--------------------+--------------+-----------------+-------------------------------+
        '''
        pass

    def on_advance(self):
        '''
        Called to advance / step the physics scene.

        I.e. update ``self.circles`` if you're using it.
        '''
        pass

    def on_render(self):
        '''
        Called to render the displayed image.

        I.e. update ``self.img`` if it's used.
        '''
        pass

    def on_show(self):
        pass

    def on_press(self, key):
        pass

    def on_pressing(self, key):
        pass

    def on_not_pressing(self):
        pass

    def on_release(self, key):
        pass

    def on_click(self, x, y, btn):
        pass

    def on_clicking(self, x, y, btn):
        pass

    def on_not_clicking(self, x, y):
        pass

    def on_unclick(self, x, y, btn):
        pass

    def on_hover(self, x, y):
        pass

    def on_drag(self, x, y):
        pass

    def on_close(self):
        self.gui.running = False

    def on_escape(self):
        self.on_close()

    def on_pre_event(self):
        '''
        Called per GUI main loop.
        '''
        MOUSE = [ti.GUI.LMB, ti.GUI.MMB, ti.GUI.RMB]
        had_any = False
        for btn in MOUSE:
            if self.gui.is_pressed(btn):
                self.on_clicking(*self.mouse, btn)
                had_any = True
        if not had_any:
            self.on_not_clicking(*self.mouse)
        had_any = False
        for key in self.gui.key_pressed:
            if key not in MOUSE:
                self.on_pressing(key)
                had_any = True
        if not had_any:
            self.on_not_pressing()

    def on_start(self):
        '''
        Called when GUI main loop started, i.e. ``Animation().start()``.
        '''
        pass

    def on_post_render(self):
        pass

    def on_pre_exit(self):
        if hasattr(self, 'video_manager'):
            ext = self.video_manager.taichi_glsl_output_ext
            ti.info('Saving result to {}.{}',
                    self.video_manager.get_output_filename(''), ext
                    or 'gif and mp4')
            self.video_manager.make_video(gif=(not ext or ext == 'gif'),
                                          mp4=(not ext or ext == 'mp4'))

    def on_exit(self):
        pass

    def define_input(self):
        '''
        Should be called if you wish to use ``self.iXXX`` as uniform scalars.

        If you are familiar with `Shadertoy <https://shadertoy.com>`_, then this is for you :)
        '''
        self._iTime = ti.var(ti.f32, ())
        self._iFrame = ti.var(ti.i32, ())
        self._iMouse = ti.Vector(2, ti.f32, ())
        self._iMouseButton = ti.Vector(3, ti.i32, ())
        self._iKeyDirection = ti.Vector(2, ti.f32, ())
        self.has_input = True

    def on_update_input(self):
        if not self.has_input:
            return
        self._iTime[None] = self.time
        self._iFrame[None] = self.frame
        self._iMouse[None] = self.mouse
        ip = lambda *x: int(self.gui.is_pressed(*x))
        lmb, mmb, rmb = ip(ti.GUI.LMB), ip(ti.GUI.MMB), ip(ti.GUI.RMB)
        self._iMouseButton[None] = [lmb, mmb, rmb]
        dx = ip('d', ti.GUI.RIGHT) - ip('a', ti.GUI.LEFT)
        dy = ip('w', ti.GUI.UP) - ip('s', ti.GUI.DOWN)
        self._iKeyDirection[None] = [dx, dy]

    @property
    def iTime(self):
        '''
        (TS, float32, RO) Current time in seconds.
        '''
        if not self.has_input:
            raise Exception(
                'Add ``self.define_input()`` to ``on_init`` if you '
                'wish to use inputs')
        if ti.inside_kernel():
            return ti.subscript(self._iTime, None)
        else:
            return self._iTime[None]

    @property
    def iFrame(self):
        '''
        (TS, int32, RO) Current frame number start from 0.
        '''
        if not self.has_input:
            raise Exception(
                'Add ``self.define_input()`` to ``on_init`` if you '
                'wish to use inputs')
        if ti.inside_kernel():
            return ti.subscript(self._iFrame, None)
        else:
            return self._iFrame[None]

    @property
    def iMouse(self):
        '''
        (TS, 2D float32 vector, RO) Current mouse position from 0 to 1.
        '''
        if not self.has_input:
            raise Exception(
                'Add ``self.define_input()`` to ``on_init`` if you '
                'wish to use inputs')
        if ti.inside_kernel():
            return self._iMouse.subscript(None)
        else:
            return self._iMouse[None]

    @property
    def iMouseButton(self):
        '''
        (TS, 3D int32 vector, RO) Current mouse button status.

        ``self.iMouseButton[0]`` is ``1`` if LMB is pressed.
        ``self.iMouseButton[1]`` is ``1`` if MMB is pressed.
        ``self.iMouseButton[2]`` is ``1`` if RMB is pressed.
        Otherwise, ``0``.
        '''
        if not self.has_input:
            raise Exception(
                'Add ``self.define_input()`` to ``on_init`` if you '
                'wish to use inputs')
        if ti.inside_kernel():
            return self._iMouseButton.subscript(None)
        else:
            return self._iMouseButton[None]

    @property
    def iKeyDirection(self):
        '''
        (TS, 2D float32 vector, RO) Direction according to ASWD / arrow keys.

        If A or left arrow is pressed, then ``self.iKeyDirection`` is ``vec(-1.0, 0.0)``.
        If D or right arrow is pressed, then ``self.iKeyDirection`` is ``vec(1.0, 0.0)``.
        If W or up arrow is pressed, then ``self.iKeyDirection`` is ``vec(0.0, 1.0)``.
        If S or down arrow is pressed, then ``self.iKeyDirection`` is ``vec(0.0, -1.0)``.
        '''
        if not self.has_input:
            raise Exception(
                'Add ``self.define_input()`` to ``on_init`` if you '
                'wish to use inputs')
        if ti.inside_kernel():
            return self._iKeyDirection.subscript(None)
        else:
            return self._iKeyDirection[None]

    @property
    def iResolution(self):
        '''
        (TS, 2D int32 vector, RO) Window size / screen resolution.
        '''
        return self.resolution

    def on_event(self, e):
        '''
        Called when a event occurred, hook me if you want a raw event control.
        '''
        MOUSE = [ti.GUI.LMB, ti.GUI.MMB, ti.GUI.RMB]
        if e.type == ti.GUI.PRESS:
            if e.key in MOUSE:
                self.on_click(*e.pos, e.key)
            else:
                if e.key == ti.GUI.ESCAPE:
                    self.on_escape()
                if e.key == ti.GUI.EXIT:
                    self.on_close()
                self.on_press(e.key)
        elif e.type == ti.GUI.RELEASE:
            if e.key in MOUSE:
                self.on_unclick(*e.pos, e.key)
            else:
                self.on_release(e.key)
        elif e.type == ti.GUI.MOTION:
            had_any = False
            for btn in MOUSE:
                if gui.is_pressed(btn):
                    self.on_drag(*e.pos, btn)
                    had_any = True
            if not had_any:
                self.on_hover(*e.pos)

    @property
    def mouse(self):
        '''
        (PS, tuple of two float, RO) Get mouse position / cursor coordinate from 0 to 1.
        '''
        return self.gui.get_cursor_pos()

    @property
    def resolution(self):
        '''
        (PS, tuple of two int, RW) Get or set window size / screen resolution.
        '''
        if self.img is not None:
            return self.img.shape()[0:2]
        else:
            return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    @property
    def time(self):
        '''
        (PS, float32, RO) Get current time in seconds.
        '''
        return time.time() - self.start_time

    @property
    def frame(self):
        '''
        (PS, int, RO) Get current frame number start from 0.
        '''
        return self.gui.frame

    def start(self):
        '''
        Call me when GUI is ready to start shows up.

        A common usage for application can be: ``MyAnimation().start()``.
        '''
        self.on_start()
        with ti.GUI(self.title,
                    self.resolution,
                    background_color=self.background_color) as self.gui:
            if not hasattr(self.gui, 'running'):
                self.gui.running = True
            if not hasattr(self.gui, 'frame'):
                self.gui.frame = 0
            if not hasattr(ti.GUI, 'EXIT'):
                ti.GUI.EXIT = 'WMClose'
            while self.gui.running:
                self._per_loop()
        self.on_pre_exit()
        self.on_exit()
        self.gui = None

    def _per_loop(self):
        self.on_pre_event()
        for e in self.gui.get_events():
            self.on_event(e)
        self.on_update_input()
        self.on_advance()
        self.on_render()
        self.on_post_render()
        if self.img is not None:
            self.gui.set_image(self.img)
        if self.circles is not None:
            self.gui.circles(self.circles.to_numpy(), self.circle_color,
                             self.circle_radius)
        self.on_show()
        if self.screenshot_dir is None:
            self.gui.show()
        else:
            self.gui.show(f'{self.screenshot_dir}/{self.frame:06d}.png')
        if hasattr(self, 'video_manager'):
            self.video_manager.write_frame(self.img.to_numpy())
            ti.debug('Frame {} recorded', self.gui.frame)
        self.gui.frame += 1
