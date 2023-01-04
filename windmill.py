import pygame
import numpy as np


class RP:
    def __init__(self, screen, vertices, color, width=0):
        self.screen = screen
        self.vertices = vertices
        self.color = color
        self.width = width
        self.AD=0

        n = len(vertices) # = 꼭짓점
        x, y = 0, 0
        for a, b in vertices:
            x += a
            y += b
        self.centroid = (x//n, y//n)
        self.rx, self.ry = self.centroid

    def rotate(self, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])  #회전변환행렬

        delta_v = [([a - self.rx], [b - self.ry]) for a, b in self.vertices]
       
        rotated_delta = [np.dot(rotation_matrix, v) for v in delta_v]

        self.vertices = [(self.rx + r[0][0], self.ry + r[1][0]) for r in rotated_delta]
        self.AD += angle
    
    def data(self):
        return self.screen, self.color, [(int(v[0]), int(v[1])) for v in self.vertices], self.width

if __name__ == "__main__":
    t = 0
    pygame.init()
    screen = pygame.display.set_mode((500,500))                                        
    pygame.display.set_caption("windmill")

#전역변수
    FPS = 60
    clock = pygame.time.Clock()

    BLACK = (0,0,0)
    GREEN = (0,255,0)
    RED = (255,0,0)
    PINK = (255, 200, 180)
    WHITE = (255,255,255)
    
    windmill = RP(screen, [(150,250), (350,250), (250,150), (250,350)], WHITE , width=10)
    
    
    
    
    playing = False
    while not playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = True

        screen.fill(BLACK)
        
        
        pygame.draw.polygon(*windmill.data())
        windmill.rotate(np.pi / 120)
        pygame.draw.polygon(screen, WHITE, [[250,250], [200, 500], [300,500]], 5)
        pygame.display.update()

        clock.tick(FPS)

pygame.quit()        
