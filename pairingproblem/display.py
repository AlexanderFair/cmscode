import pygame
from time import sleep

class Display():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
    
    def draw_points(self, blue_pts, red_pts):
        self.screen.fill('white')
        for p in blue_pts:
            pygame.draw.circle(self.screen, "blue", p, 4)
        for p in red_pts:
            pygame.draw.circle(self.screen, "red", p, 4)
        pygame.display.flip()
        sleep(1)
    
    def draw_pairing(self, blue_pts, red_pts):
        self.screen.fill('white')
        for p in blue_pts:
            pygame.draw.circle(self.screen, "blue", p, 4)
        for p in red_pts:
            pygame.draw.circle(self.screen, "red", p, 4)
        for i in range(len(blue_pts)):
            pygame.draw.line(self.screen, "black", blue_pts[i], red_pts[i])
        pygame.display.flip()

        sleep(min(5/len(blue_pts), 0.3))
