# 재시작 버튼만들기_완료_v4
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ 메인루틴, 메인ルーチン """
    def reset_game():
        nonlocal game_over, ship_y, velocity, score, slope, holes
        game_over = False
        ship_y = 250
        velocity = 0
        score = 0
        slope = randint(1, 6)
        holes = []
        for xpos in range(walls):
            holes.append(Rect(xpos * 10, 100, 10, 400))

    walls = 80
    ship_y = 250
    velocity = 0
    score = 0
    slope = randint(1, 6)
    sysfont = pygame.font.SysFont(None, 36)
    ship_image = pygame.image.load("ship.png")
    bang_image = pygame.image.load("bang.png")
    restart_button = pygame.image.load("restart_button.png")  # 재시작 버튼 이미지
    restart_button_rect = restart_button.get_rect()
    restart_button_rect.topleft = (10, 520)  # 버튼 위치
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    game_over = False

    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True

        if game_over:
            # 재시작 버튼 클릭 처리
            if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # 마우스 왼쪽 버튼 클릭
                    reset_game()
        else:
            score += 10
            velocity += -3 if is_space_down else 1
            ship_y += velocity

            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]

            if holes[0].top > ship_y or \
                    holes[0].bottom < ship_y + 80:
                game_over = True

        SURFACE.fill((0, 255, 0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        SURFACE.blit(restart_button, restart_button_rect.topleft)  # 재시작 버튼 그리기
        score_image = sysfont.render("score is {}".format(score),
                                     True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20))

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y - 40))

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()

