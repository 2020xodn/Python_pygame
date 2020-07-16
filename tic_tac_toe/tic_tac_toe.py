'''
    최초 작성자 : 17 권태우
    최초 작성일 : 2020.06.12
    최초 변경일 : 2020.xx
    목적 : pygame을 이용한 Tic Tac Toe
    개정 이력 : OOO, 2020.xx(ver. 01)
'''

import pygame
###################################################
pygame.init() # 초기화

# 화면 크기 설정
screen_width = 400 # 가로 크기
screen_height = 500 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 
pygame.display.set_caption("Tic Tac Toe") # 게임 이름

####################################################

# 이미지 불러오기 Load Image

board = pygame.image.load("board.png")
board_size = board.get_rect().size # 이미지 크기를 구해옴
board_width = board_size[0]   #보드판의 가로 크기
board_height = board_size[1]  #보드판의 세로 크기

blank_rect_list = list()
blank_list = list()
for i in range(9):
    blank_list.append(pygame.image.load("blank.png"))


# 폰트 정의
game_font = pygame.font.Font('arial.ttf', 30) # 폰트 객체 생성 (폰트, 크기)

# O or X 의 이미지를 불러오는 함수
def draw_O_or_X(board, board_select_image, turn, choice):
    if turn == 1:
        board_select_image[choice] = pygame.image.load("circle.png")
    elif turn == 2:
        board_select_image[choice] = pygame.image.load("cross.png")

    board[choice] = turn     # 각 보드는 선택한 플레이어의 숫자로 변함
    print(board)

# 승리조건 체크 함수
def check_win(board, who):
    for i in range(3):
        if board[0 + i * 3] == who and board[1 + i * 3] == who and board[2 + i * 3] == who:    # 가로 체크
            win_image = pygame.image.load("win_horizontal.png")
            return who, win_image, i
        if board[i] == who and board[i + 3] == who and board[i + 6] == who:                    # 세로 체크
            win_image = pygame.image.load("win_vertical.png")
            return who, win_image, 3 + i
    
    if board[0] == who and board[4] == who and board[8] == who:                            # \
        win_image = pygame.image.load("win_diagonal1.png")
        return who, win_image, 6
    if board[2] == who and board[4] == who and board[6] == who:                            # /
        win_image = pygame.image.load("win_diagonal2.png")
        return who, win_image, 7
        
    return 0, None, 0            # nothing → 0, None, 0

# 게임 시작
def game_start():
    whos_turn = 1
    winner = 0
    winner_po = None  # 0 ~ 2 → 가로, 3 ~ 5 → 세로,  6 7  \ / 대각선
    winner_image = None
    Waiting = True
    running = True
    how_to_quit = None  # 휠을 눌러 종료
    board_select = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    board_select_image = [None, None, None, None, None, None, None, None, None]

    while running:
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Waiting = False
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # print(mouse)

                if event.button == 2:   # 휠 클릭 시 종료
                    running = False
                    Waiting = False

                if event.button == 1:

                    for i in range(9):
                        if blank_rect_list[i].collidepoint(mouse):
                            if board_select[i] == 0:
                                draw_O_or_X(board_select, board_select_image, whos_turn, i)
                                winner, winner_image, winner_po = check_win(board_select, whos_turn)

                                whos_turn = 2 if whos_turn == 1 else 1  # whos_turn 토글

                                running = True if winner == 0 else False # 승자가 정해졌다면 종료
                                if 0 not in board_select and running == True:   # 모든 칸이 차있는데 승자가 정해지지 않았다면 비김처리
                                    running = False
                                    winner = 3

            # End if event.type  MOUSEBUTTONDOWN

        # 화면에 그리기
        
        screen.fill((255, 255, 255)) # RGB 값
        screen.blit(board, (0, 0)) # 보드 그리기

        image_po = ((2, 2), (134, 2), (266, 2),    (2, 133), (134, 133), (268, 133),    (2,264), (134, 264), (268, 264))

        for i in range(9):
            if board_select_image[i] != None:
                screen.blit(board_select_image[i], image_po[i]) # OX 이미지
            else:    
                screen.blit(blank_list[i], image_po[i]) # 보드 빈칸
        
        if len(blank_rect_list) == 0:       # 최초 blank_rect_list 생성
            for i in range(9):
                blank_rect_list.append(None)
                blank_rect_list[i] = blank_list[i].get_rect(x = screen_width / 3 * (i % 3), y = screen_width / 3 * int(i / 3))
        
        if winner == 0:
            turn_text = game_font.render(str(str(whos_turn) + "P's Turn") + ("(O)" if whos_turn == 1 else "(X)"), True, (0, 0, 0))
            screen.blit(turn_text, (board_width / 2 - 80, board_height + 20))

        elif winner == 3:
            draw_text = game_font.render("Draw....", True, (0, 0, 0))
            screen.blit(draw_text, (board_width / 2 - 80, board_height + 20))
            how_to_quit = game_font.render("Press Mouse Wheel To Quit", True, (0, 0, 0))
            screen.blit(how_to_quit, (20 , board_height + 60))
        else:
            winner_text = game_font.render(str(str(winner) + "P is Winner !"), True, (0, 0, 0))
            screen.blit(winner_text, (board_width / 2 - 80, board_height + 20))
            how_to_quit = game_font.render("Press Mouse Wheel To Quit", True, (0, 0, 0))
            screen.blit(how_to_quit, (20 , board_height + 60))
            if winner_po <= 2:   # 가로
                screen.blit(winner_image, (2, 2 + 130 * (winner_po)))
            elif winner_po <= 5: # 세로
                screen.blit(winner_image, (3 + 130 * (winner_po - 3), 2))
            elif winner_po == 6: # \ 대각선
                screen.blit(winner_image, (0, 0))
            elif winner_po == 7: # / 대각선
                screen.blit(winner_image, (0, 0))
            
        
        pygame.display.update() # 게임화면을 다시 그리기 (필수)



    # 휠을 누르면 종료
    while Waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Waiting = False        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    Waiting = False

# main
game_start()

pygame.quit()