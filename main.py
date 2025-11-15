import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
CHARACTER_WIDTH = 300
CHARACTER_HEIGHT = 375

FPS = 60

font = pg.font.Font(None, 40)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.load_animations()

        self.image = self.idle_animation_right[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_right

        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.side = 'right'
        self.animation_mode = True

    
    def load_animations(self):
        self.idle_animation_right = [load_image(f"images/fire wizard/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 4)]
        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.move_animation_right = [load_image(f"images/fire wizard/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 5)] 
        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]  
    
    def update(self):
        keys = pg.key.get_pressed()
        direction = 0
        if keys[pg.K_a]:
            direction = -1
            self.side = 'left'
        elif keys[pg.K_d]:
            direction = 1
            self.side = 'right'

        self.handle_movement(direction, keys)

        self.handle_animation()
    
    def handle_movement(self, direction, keys):
        if direction != 0:
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right

        else:
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

    def handle_animation(self):

        if self.animation_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.frontground = load_image("images/frontground.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.player = Player()

        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        self.player.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.frontground, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)

        pg.display.flip()


if __name__ == "__main__":
    Game()