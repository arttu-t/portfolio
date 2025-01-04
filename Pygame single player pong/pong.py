import pygame, sys, time

#setup
pygame.init()
screen = pygame.display.set_mode((800, 500))
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
clock = pygame.time.Clock()
count = 0

#wait in the beginning before starting
wait = 0

#ball properties
ball_radius = 20
ball_pos = [420, 205]
speed = [3, 3]

#rectangle (paddle) proerties
rect_width = 20
rect_height = 100
rect_pos = [720, 200]
rect_speed = 5

#wall proerties
wall_width = 20
wall_height = 900
wall_pos = [380, 0]

#text properties
x=10
y=100
font = pygame.font.SysFont(None, 30)

#elapsed time counting
start_time1 = time.time()
start_time2 = time.time()

move_up = False
move_down = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        #moves paddle when w or s are pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False
    
    end_time = time.time()
    elapsed_time = end_time-start_time1
    playtime = end_time-start_time2

    if elapsed_time >= 10:
        speed[0] *= 1.5
        speed[1] *= 1.5
        rect_speed *= 1.3
        start_time1 = time.time()
    

    #block paddle from going off the screen
    if move_up and rect_pos[1] > 0: 
        rect_pos[1] -= rect_speed
    if move_down and rect_pos[1] < 400:
        rect_pos[1] += rect_speed
    
    #make hitbox for ball and paddle
    ball_hitbox = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius*2, ball_radius*2)
    paddle_rect = pygame.Rect(rect_pos[0], rect_pos[1], rect_width, rect_height)

    #detect a collision
    if ball_hitbox.colliderect(paddle_rect):
        speed[0] = -speed[0]
       
    
    ball_pos[0] += speed[0]
    ball_pos[1] += speed[1]

    #bounce if ball hits the borders of the screen
    if ball_pos[0] - ball_radius <= 400:
        speed[0] = -speed[0]

    if ball_pos[1] + ball_radius >= 500 or ball_pos[1] - ball_radius <= 0:
        speed[1] = -speed[1]
    
    if speed[0] <= 5:
        if ball_pos[0] + ball_radius >= 730:
            font = pygame.font.SysFont(None, 36)
            gameover_text = font.render("Game over!", True, red)
            result_text = font.render(f"You survived for {playtime:.1f} seconds", True, red)
            screen.blit(gameover_text, (500,200))
            screen.blit(result_text, (400,250))
            pygame.display.flip()
            time.sleep(3)
            sys.exit()
    
    else:
        if ball_pos[0] + ball_radius >= 790:
            font = pygame.font.SysFont(None, 36)
            gameover_text = font.render("Game over!", True, red)
            result_text = font.render(f"You survived for {playtime:.1f} seconds", True, red)
            screen.blit(gameover_text, (500,200))
            screen.blit(result_text, (400,250))
            pygame.display.flip()
            time.sleep(3)
            sys.exit() 
    
    
   
    screen.fill(white)

    #text stuff
    text1 = font.render("This is a simple single-player pong", True, black)
    text2 = font.render("Control the paddle with w and s", True, black)
    text3 = font.render("The ball speeds up every 10 seconds", True, black)

    screen.blit(text1, (x, y))
    screen.blit(text2, (x, y+20))
    screen.blit(text3, (x, y+40))

    #draw objects on screen
    pygame.draw.circle(screen, black, ball_pos, ball_radius)
    pygame.draw.rect(screen, black, (rect_pos[0], rect_pos[1], rect_width, rect_height))
    pygame.draw.rect(screen, black, (wall_pos[0], wall_pos[1], wall_width, wall_height))

    pygame.display.flip()
    
    #cap the game to 60 fps to ensure game running as intended
    clock.tick(60)

    #wait for 3 seconds
    if wait == 0:
        time.sleep(3)
        elapsed_time -= 3
        playtime -= 3
        wait += 1

pygame.quit()
