import pygame, random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Groups")
clock = pygame.time.Clock()

blue_monster_image = pygame.image.load("sprites/blue-monster.png")
green_monster_image = pygame.image.load("sprites/green-monster.png")
purple_monster_image = pygame.image.load("sprites/purple-monster.png")
orange_monster_image = pygame.image.load("sprites/orange-monster.png")
monster_images = [blue_monster_image, green_monster_image, purple_monster_image, orange_monster_image]

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = monster_images[random.randint(0, len(monster_images)-1)]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.velocity = random.randint(1,5)

    def update(self):
        self.rect.y += self.velocity


monsters = pygame.sprite.Group()
for i in range(10):
    monster = Monster((i*100, 10))
    monsters.add(monster)

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

    display_surface.fill((0,0,0))

    monsters.update()
    monsters.draw(display_surface)


    clock.tick(FPS)

pygame.quit()