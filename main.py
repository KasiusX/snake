import os
from random import randint
import os
import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SNAKE")
FPS = 10

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
HEAD_COLOR = (0,0,0)
TAIL_COLOR = (0, 255, 204)
PLAYER_VEL = 10
PLAYER_SIZE = 10
POINT_SIZE =10
STARTING_LENGTH = 5

GAME_OVER = pygame.USEREVENT + 1
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 25)

POINT_PICKED_SOUND = pygame.mixer.Sound(os.path.join('Assets','point_picked.mp3'))
END_SOUND = pygame.mixer.Sound(os.path.join('Assets','end.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets','background_music.mp3'))

PLAYGROUND = pygame.Rect(0,0,WIDTH,HEIGHT)

def draw_window(head,point,tail, score):    
    pygame.draw.rect(WIN,WHITE, PLAYGROUND)
    pygame.draw.rect(WIN,HEAD_COLOR, head)   
    pygame.draw.rect(WIN,RED,point)

    for tail_piece in tail:
        pygame.draw.rect(WIN,TAIL_COLOR,tail_piece)

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

def game_over(score):
    text = GAME_OVER_FONT.render(f"GAME OVER ({score})",1,BLACK)
    WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))    
    pygame.display.update() 
    BACKGROUND_SOUND.stop()
    END_SOUND.play()
    pygame.time.delay(5000)

def get_new_point():
    return pygame.Rect(randint(0,WIDTH/POINT_SIZE - 1) * POINT_SIZE, randint(0,HEIGHT/POINT_SIZE - 1) *POINT_SIZE,POINT_SIZE,POINT_SIZE)

def move_opposite(move, tail):
    if move == move_up:
        move_down(tail)
    if move == move_down:
        move_up(tail)
    if move == move_left:
        move_right(tail)
    if move == move_right:
        move_left(tail)

def move_tail(tail,head ):    
    previous_piece = pygame.Rect(head.x, head.y,0,0)
    for tail_piece in tail:
        tail_piece.x, previous_piece.x = previous_piece.x, tail_piece.x
        tail_piece.y, previous_piece.y = previous_piece.y, tail_piece.y

def add_tail_piece(tail,head,move):
    tail_piece = pygame.Rect(head.x,head.y,PLAYER_SIZE,PLAYER_SIZE)
    move_opposite(move,tail_piece)  
    tail.append(tail_piece)

def check_tail_collision(tail,head):
    for tail_piece in tail:
        if tail_piece.colliderect(head):
            pygame.event.post(pygame.event.Event(GAME_OVER))

def main():
    run = True    
    clock = pygame.time.Clock()
    head = pygame.Rect(WIDTH/2 - PLAYER_SIZE/2,HEIGHT/2 - PLAYER_SIZE/2,PLAYER_SIZE,PLAYER_SIZE)
    point = get_new_point()
    score = 0
    move = move_right
    tail = []
    for i in range(STARTING_LENGTH):
        add_tail_piece(tail,head,move)
    BACKGROUND_SOUND.play(loops=-1,fade_ms=500)
    while run:               
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == GAME_OVER and run:
                game_over(score)
                main()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and move != move_up:
                    move = move_down
                elif event.key == pygame.K_UP and move != move_down:
                    move = move_up
                elif event.key == pygame.K_LEFT and move != move_right:
                    move = move_left
                elif event.key == pygame.K_RIGHT and move != move_left:
                    move = move_right
            
        if head.colliderect(point):
            score += 1
            point = get_new_point()
            add_tail_piece(tail,head,move)
            POINT_PICKED_SOUND.play()
        
        check_tail_collision(tail,head)
        
        
        move_tail(tail,head)
        move(head)
        print(head.x,head.y)
        draw_window(head,point,tail,score)
        
        

if __name__ == "__main__":
    main()
