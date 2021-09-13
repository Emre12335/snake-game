from random import randrange
import pygame


class redbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((40, 40))
        self.image.fill("Red")
        self.rect = self.image.get_rect(bottomright=(400, 280))
        self.movement = (40, "d")
        self.old = self.rect.copy()

    def move(self):
        self.old = self.rect.copy()
        if self.movement[1] == "w":
            self.rect.y += self.movement[0]
        elif self.movement[1] == "s":
            self.rect.y += self.movement[0]
        elif self.movement[1] == "d":
            self.rect.x += self.movement[0]
        elif self.movement[1] == "a":
            self.rect.x += self.movement[0]
        if self.rect.left >= 800:
            self.rect.left = 0
        elif self.rect.right <= 0:
            self.rect.right = 800
        elif self.rect.bottom <= 0:
            self.rect.bottom = 600
        elif self.rect.top >= 600:
            self.rect.top = 0

    def update(self):
        self.move()


class tail(pygame.sprite.Sprite):
    tail_list = []

    def __init__(self):
        super().__init__()
        if len(tail.tail_list) == 0:
            self.nxt = a
        else:
            self.nxt = tail.tail_list[0]
        tail.tail_list.insert(0, self)
        self.image = a.image
        self.rect = self.nxt.old
        self.old = self.rect.copy()
        self.movement = self.nxt.movement

    def move(self):
        self.old = self.rect.copy()
        self.rect = self.nxt.old

    def update(self):
        self.move()


class target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((40, 40))
        self.image.fill("Green")
        self.rect = self.image.get_rect(center=(randrange(20, 800, 40), randrange(20, 600, 40)))


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

a = redbox()
group1 = pygame.sprite.GroupSingle(a)
group2 = pygame.sprite.Group()
target1 = target()
group3 = pygame.sprite.GroupSingle(target1)


def draw_lines(rows):
    distance_btw_x = 800 // rows
    a = 0
    for l in range(rows + 2):
        pygame.draw.line(screen, "White", (a, 0), (a, 600))
        pygame.draw.line(screen, "White", (0, a), (800, a))
        a += distance_btw_x


def eat_check():
    global score
    global group2
    global group3
    global target1
    if pygame.sprite.spritecollide(a, group3, True):
        group2.add(tail())
        score += 1
        target1 = target()
        group3.add(target1)


def play_active_check():
    if pygame.sprite.spritecollide(a, group2, False):
        return False
    return True


play_active = False

# Play off screen
main_image = pygame.image.load("pygame-head-party.png")
main_image_r = main_image.get_rect(center=(400, 250))
font = pygame.font.Font(None, 100)
Snake_s = font.render("Snake Game", True, (255, 250, 250))
snake_r = Snake_s.get_rect(midbottom=(main_image_r.centerx, main_image_r.top + 70))
font2 = pygame.font.Font(None, 40)
start_game = font2.render("press enter to start the game", True, (255, 250, 250))
start_game_r = start_game.get_rect(midtop=(main_image_r.centerx, main_image_r.bottom - 40))

# Scoreboard
font3 = pygame.font.Font(None, 60)
score = 0
score_s = font3.render(f"Score:{score}", True, (255, 250, 250))
score_s2 = font2.render(f"Score:{score}", True, (255, 250, 250))
score_s_m = score_s.get_rect(midtop=(start_game_r.centerx, start_game_r.bottom + 23))
score_s_r = score_s.get_rect(midbottom=(445, 610))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if play_active:
            if event.type == pygame.KEYDOWN:
                if len(tail.tail_list) == 0:
                    if event.key == pygame.K_w:
                        a.movement = (-40, "w")
                    elif event.key == pygame.K_s:
                        a.movement = (40, "s")
                    elif event.key == pygame.K_a:
                        a.movement = (-40, "a")
                    elif event.key == pygame.K_d:
                        a.movement = (40, "d")
                else:
                    if event.key == pygame.K_w and a.movement[1] != "s":
                        a.movement = (-40, "w")
                    elif event.key == pygame.K_s and a.movement[1] != "w":
                        a.movement = (40, "s")
                    elif event.key == pygame.K_a and a.movement[1] != "d":
                        a.movement = (-40, "a")
                    elif event.key == pygame.K_d and a.movement[1] != "a":
                        a.movement = (40, "d")
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    group2.empty()
                    a.rect = a.image.get_rect(bottomright=(400, 280))
                    a.movement = (40, "d")
                    play_active = True
                    target1 = target()
                    group3.add(target1)
                    score = 0

    # pygame.time.delay(500)
    if play_active:
        score_s2 = font2.render(f"Score:{score}", True, (255, 250, 250))
        screen.fill("Black")
        group1.draw(screen)
        pygame.draw.circle(screen, "Black", (a.rect.centerx - 9, a.rect.centery - 5), radius=3)
        pygame.draw.circle(screen, "Black", (a.rect.centerx + 9, a.rect.centery - 5), radius=3)
        group1.update()
        group2.draw(screen)
        group2.update()
        group3.draw(screen)
        group3.update()
        screen.blit(score_s2, score_s_r)
        draw_lines(20)
        eat_check()
        play_active = play_active_check()
    else:
        score_s = font3.render(f"Score:{score}", True, (255, 250, 250))
        screen.fill((64, 64, 64))
        screen.blit(main_image, main_image_r)
        screen.blit(Snake_s, snake_r)
        screen.blit(start_game, start_game_r)
        screen.blit(score_s, score_s_m)
        group3.empty()
        tail.tail_list.clear()

    pygame.display.update()
    clock.tick(10)
