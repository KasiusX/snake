import pygame
pygame.font.init()

WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SNAKE")
FPS = 8

WHITE = (255,255,255)
BLACK = (0,0,0)
PLAYER_COLOR = (0,0,0)
PLAYER_VEL = 10

GAME_OVER = pygame.USEREVENT + 1
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 25)

PLAYGROUND = pygame.Rect(0,0,WIDTH,HEIGHT)

def draw_window(head,score):    
    pygame.draw.rect(WIN,WHITE, PLAYGROUND)
    pygame.draw.rect(WIN,PLAYER_COLOR, head)

    score_text = SCORE_FONT.render(f"Score: {score}",1,BLACK)
    WIN.blit(score_text,(WIDTH- score_text.get_width() - 10,10))
    pygame.display.update()

def move_left(head):
    head.x -= PLAYER_VEL
    if head.x < 0:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def move_right(head):
    head.x += PLAYER_VEL
    if head.x + head.width > WIDTH:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def move_down(head):
    head.y += PLAYER_VEL
    if head.y + head.height > HEIGHT:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def move_up(head):
    head.y -= PLAYER_VEL
    if head.y < 0:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def game_over():
    text = GAME_OVER_FONT.render("GAME OVER",1,BLACK)
    WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))    
    pygame.display.update() 
    pygame.time.delay(3000)

def main():
    run = True    
    clock = pygame.time.Clock()
    head = pygame.Rect(WIDTH/2 - 5,HEIGHT/2 - 5,10,10)
    score = 0
    move = move_right
    while run:        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == GAME_OVER and run:
                game_over()
                main()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and move != move_up:
                    move = move_down
                if event.key == pygame.K_UP and move != move_down:
                    move = move_up
                if event.key == pygame.K_LEFT and move != move_right:
                    move = move_left
                if event.key == pygame.K_RIGHT and move != move_left:
                    move = move_right
                
        
        move(head)
        print(head.x,head.y)
        draw_window(head,score)
        

if __name__ == "__main__":
    main()
