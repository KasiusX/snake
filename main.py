import pygame

WIDTH, HEIGHT = 500,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SNAKE")
FPS = 30

PLAYGROUND = pygame.Rect(0,0,WIDTH,HEIGHT)

WHITE = (255,255,255)

def draw_window():
    pygame.draw.rect((0,0),WHITE, PLAYGROUND)

def main():
    run = True    
    clock = pygame.time.Clock()
    while run:        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        

if __name__ == "__name__":
    main()
