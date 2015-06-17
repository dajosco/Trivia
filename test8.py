#!/usr/bin/env python
# http://www.fileformat.info/format/mpeg/sample/index.dir
import pygame

FPS = 30
count_down_timer=0

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('media/output8.mpg')
#movie = pygame.movie.Movie('media/hst_1.mpg')

#screen = pygame.display.set_mode(pygame.Surface(movie.get_size()),pygame.FULLSCREEN)
screen = pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
movie_screen = pygame.Surface(movie.get_size()).convert()

#1280x720

movie.set_display(movie_screen)

font = pygame.font.SysFont("renegademaster", 50, bold = 0)
count_down = font.render("{:02d}".format(count_down_timer),True, (255,255,0)) 
count_down_pos = count_down.get_rect()
count_down_pos.centerx = movie_screen.get_rect().centerx
count_down_pos.centery = movie_screen.get_rect().centery

movie.play()

frames=0

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            movie.stop()
            playing = False
        if event.type == pygame.KEYDOWN:
            movie.stop()
            pygame.quit()
            exit(1)
            break
        

    if not movie.get_busy():
        movie.rewind()
        movie.play()
        
        
    count_down = font.render("{:02d}".format(count_down_timer),True, (255,255,0)) 

    screen.blit(movie_screen,(0,0))
    screen.blit(count_down, count_down_pos)
    frames+=1
    if frames>FPS:
        frames=0
        count_down_timer+=1

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
