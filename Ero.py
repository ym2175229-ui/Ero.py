import math
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Heart Code - Crisp Burgundy")
clock = pygame.time.Clock()

glow_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
text_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

WHITE = (255, 255, 255)
BURGUNDY = (110, 0, 28)
PINK_HEART = (245, 130, 160)



class FlyingHeart:
    def __init__(self):
        self.reset()
        self.y = random.randint(0, HEIGHT)

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(10, 50)
        self.speed = random.uniform(1.2, 2.5)
        self.size = random.randint(10, 18)
        self.alpha = random.randint(70, 150)

    def update(self):
        self.y -= self.speed
        if self.y < -30:
            self.reset()

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        color = (PINK_HEART[0], PINK_HEART[1], PINK_HEART[2], self.alpha)
        r = self.size // 2
        pygame.draw.circle(s, color, (r, r), r)
        pygame.draw.circle(s, color, (3 * r, r), r)
        points = [(0, r), (4 * r, r), (2 * r, 3 * r)]
        pygame.draw.polygon(s, color, points)
        surface.blit(s, (self.x, int(self.y)))



class Particle:
    def __init__(self, x, y, word, font, color, delay):
        self.x = x
        self.y = y
        self.word = word
        self.font = font
        self.color = color
        self.delay = delay
        self.alpha = 0
        self.flicker = random.uniform(0, math.pi * 2)



def get_heart_position(t, scale=15.0):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    return WIDTH // 2 + int(x * scale), HEIGHT // 2 + int(y * scale)



def draw_crisp_text(surface, font, text, color, pos, alpha):
    r, g, b = color
    # رسم النص مباشرة بأعلى جودة بدون طبقات توهج ضبابية
    text_surface = font.render(text, True, (r, g, b))
    text_surface.set_alpha(alpha)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)



font = pygame.font.SysFont("Trebuchet MS", 18, bold=True)
center_font = pygame.font.SysFont("Georgia", 36, bold=True)

flying_hearts = [FlyingHeart() for _ in range(25)]

particles = []
num_particles = 110
border_symbols = ["♥", "♥", "•", "♥"]


for i in range(num_particles):
    t = (i / num_particles) * math.pi * 2
    for scale_offset in [14.6, 15.4]:  # طبقتين فقط لمنع التزاحم والملغشة
        px, py = get_heart_position(t, scale=scale_offset)
        word = random.choice(border_symbols)
        delay = int((1 - math.sin(t)) * 20) + random.randint(0, 10)
        particles.append(Particle(px, py, word, font, BURGUNDY, delay))


running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill(WHITE)
    glow_layer.fill((0, 0, 0, 0))
    frame += 1


    for heart in flying_hearts:
        heart.update()
        heart.draw(screen)


    for p in particles:
        if frame > p.delay and p.alpha < 255:
            p.alpha = min(255, p.alpha + 15)

        if p.alpha >= 255:
            flick = 0.90 + 0.10 * math.sin(frame * 0.05 + p.flicker)
        else:
            flick = 1.0

        alpha = int(p.alpha * flick)
        if alpha <= 0:
            continue

        draw_crisp_text(glow_layer, p.font, p.word, p.color, (p.x, p.y), alpha)

    
    center_alpha = min(255, max(0, (frame - 15) * 10))
    if center_alpha > 0:
        draw_crisp_text(glow_layer, center_font, "I Love You Ereny", BURGUNDY, (WIDTH // 2, HEIGHT // 2), center_alpha)

    screen.blit(glow_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
