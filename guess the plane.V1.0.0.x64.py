import os
import random

import pygame


WIDTH, HEIGHT = 1100, 700
FPS = 60
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "planes")
ICON_PATH = os.path.join(os.environ.get("TEMP", os.getcwd()), "copilot_20260909_163256.png")

PLANES = [
    {
        "name": "F-16 Fighting Falcon",
        "primary": (66, 133, 244),
        "secondary": (11, 42, 84),
        "background": (12, 24, 44),
        "filename": "f16.png",
    },
    {
        "name": "Boeing 747",
        "primary": (29, 185, 84),
        "secondary": (9, 64, 32),
        "background": (11, 30, 55),
        "filename": "boeing_747.png",
    },
    {
        "name": "Concorde",
        "primary": (244, 180, 0),
        "secondary": (82, 59, 0),
        "background": (28, 28, 44),
        "filename": "concorde.png",
    },
    {
        "name": "SR-71 Blackbird",
        "primary": (219, 68, 55),
        "secondary": (88, 24, 20),
        "background": (22, 25, 34),
        "filename": "sr71.png",
    },
    {
        "name": "Spitfire",
        "primary": (153, 51, 255),
        "secondary": (53, 14, 85),
        "background": (20, 20, 35),
        "filename": "spitfire.png",
    },
    {
        "name": "C-17 Globemaster III",
        "primary": (0, 172, 193),
        "secondary": (0, 77, 84),
        "background": (14, 25, 39),
        "filename": "c17.png",
    },
]


def normalize(text):
    return " ".join(text.strip().lower().split())


def create_plane_art(name, primary, secondary, background):
    surface = pygame.Surface((800, 500), pygame.SRCALPHA)
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(background[0] * (1 - ratio) + 45 * ratio)
        g = int(background[1] * (1 - ratio) + 55 * ratio)
        b = int(background[2] * (1 - ratio) + 75 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

    pygame.draw.ellipse(surface, (255, 255, 255, 40), (40, 60, 220, 70))
    pygame.draw.ellipse(surface, (255, 255, 255, 35), (310, 45, 260, 90))
    pygame.draw.ellipse(surface, (255, 255, 255, 30), (580, 80, 140, 60))

    runway = pygame.Rect(0, 420, 800, 80)
    pygame.draw.rect(surface, (35, 35, 40), runway)
    for x in range(0, 800, 60):
        pygame.draw.rect(surface, (230, 230, 230), (x, 450, 30, 10))

    body = [(120, 285), (500, 185), (650, 210), (710, 260), (650, 318), (170, 320)]
    wing = [(230, 245), (430, 210), (610, 235), (520, 300), (280, 300)]
    tail = [(520, 190), (610, 150), (670, 180), (560, 240)]
    nose = [(660, 250), (720, 230), (760, 260), (710, 285)]

    pygame.draw.polygon(surface, primary, body)
    pygame.draw.polygon(surface, secondary, wing)
    pygame.draw.polygon(surface, secondary, tail)
    pygame.draw.polygon(surface, primary, nose)
    pygame.draw.rect(surface, (18, 18, 22), (420, 220, 90, 55), border_radius=10)
    pygame.draw.circle(surface, (210, 230, 255), (540, 250), 18)

    for x in range(230, 640, 105):
        pygame.draw.circle(surface, (255, 255, 255, 220), (x, 350), 17)

    overlay = pygame.Surface((800, 500), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 40), (0, 0, 800, 500), border_radius=20)
    surface.blit(overlay, (0, 0))

    font = pygame.font.SysFont("arial", 28, bold=True)
    label = font.render(name, True, (255, 255, 255))
    surface.blit(label, (30, 30))
    return surface


def create_icon_surface():
    icon_size = (128, 128)
    surface = pygame.Surface(icon_size, pygame.SRCALPHA)

    plane = create_plane_art("PLANE", (66, 133, 244), (11, 42, 84), (12, 24, 44))
    plane = pygame.transform.smoothscale(plane, icon_size)
    surface.blit(plane, (0, 0))

    border = pygame.Surface(icon_size, pygame.SRCALPHA)
    pygame.draw.rect(border, (255, 255, 255, 220), border.get_rect().inflate(-12, -12), 4, border_radius=20)
    surface.blit(border, (0, 0))
    return surface


def ensure_asset_images():
    os.makedirs(ASSET_DIR, exist_ok=True)
    images = {}
    for plane in PLANES:
        path = os.path.join(ASSET_DIR, plane["filename"])
        if not os.path.exists(path):
            art = create_plane_art(
                plane["name"],
                plane["primary"],
                plane["secondary"],
                plane["background"],
            )
            pygame.image.save(art, path)
        images[plane["name"]] = path
    return images


class GuessThePlaneGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        if os.path.exists(ICON_PATH):
            icon = pygame.image.load(ICON_PATH).convert_alpha()
        else:
            icon = create_icon_surface()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Guess the Plane")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30)
        self.small_font = pygame.font.SysFont("arial", 22)
        self.big_font = pygame.font.SysFont("arial", 46, bold=True)

        self.images = ensure_asset_images()
        self.score = 0
        self.round = 1
        self.answer = ""
        self.message = "Type the aircraft name and press Enter"
        self.current_plane = None
        self.round_complete = False
        self.pick_plane()

    def pick_plane(self):
        self.current_plane = random.choice(PLANES)
        self.answer = ""
        self.round_complete = False
        self.message = "Type the aircraft name and press Enter"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if self.round_complete:
                    if event.key == pygame.K_RETURN:
                        self.round += 1
                        self.pick_plane()
                    continue

                if event.key == pygame.K_RETURN:
                    guess = self.answer.strip()
                    if normalize(guess) == normalize(self.current_plane["name"]):
                        self.score += 1
                        self.message = "Correct! Press Enter for the next plane."
                    else:
                        self.message = f"Not quite — it was {self.current_plane['name']}. Press Enter for the next plane."
                    self.round_complete = True
                elif event.key == pygame.K_BACKSPACE:
                    self.answer = self.answer[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.answer += event.unicode

        return True

    def draw(self):
        self.screen.fill((9, 13, 20))

        title = self.big_font.render("GUESS THE PLANE", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(WIDTH / 2, 50)))

        score_text = self.small_font.render(f"Score: {self.score}   Round: {self.round}", True, (180, 210, 255))
        self.screen.blit(score_text, (60, 90))

        image_panel = pygame.Rect(120, 120, 860, 470)
        pygame.draw.rect(self.screen, (24, 31, 44), image_panel, border_radius=20)
        pygame.draw.rect(self.screen, (120, 145, 200), image_panel, 2, border_radius=20)

        plane_image = pygame.image.load(self.images[self.current_plane["name"]]).convert_alpha()
        plane_image = pygame.transform.smoothscale(plane_image, (720, 360))
        image_rect = plane_image.get_rect(center=(WIDTH / 2, 350))
        self.screen.blit(plane_image, image_rect)

        answer_box = pygame.Rect(180, 565, 740, 55)
        pygame.draw.rect(self.screen, (22, 27, 39), answer_box, border_radius=12)
        pygame.draw.rect(self.screen, (140, 170, 250), answer_box, 2, border_radius=12)

        text_surface = self.font.render(self.answer, True, (255, 255, 255))
        self.screen.blit(text_surface, (210, 575))

        message_surface = self.small_font.render(self.message, True, (220, 225, 255))
        self.screen.blit(message_surface, (180, 635))

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    GuessThePlaneGame().run()
