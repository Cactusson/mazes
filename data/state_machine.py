import pygame as pg

from . import prepare


class StateMachine:
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.fullscreen = False

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup({})

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        if not self.done:
            self.state.update(self.screen, dt)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(persist)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pg.display.set_mode(prepare.SCREEN_SIZE, pg.FULLSCREEN)
        else:
            pg.display.set_mode(prepare.SCREEN_SIZE)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    if (pg.key.get_pressed()[pg.K_LALT] or
                            pg.key.get_pressed()[pg.K_RALT]):
                        self.done = True
                elif event.key == pg.K_f:
                    self.toggle_fullscreen()
            self.state.get_event(event)

    def main(self):
        while not self.done:
            dt = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(dt)
            pg.display.update()
            fps = self.clock.get_fps()
            with_fps = '{} - {:.2f} FPS'.format(self.caption, fps)
            pg.display.set_caption(with_fps)


class _State:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, persistant):
        self.persist = persistant

    def cleanup(self):
        self.done = True
        return self.persist

    def update(self, surface, dt):
        pass
