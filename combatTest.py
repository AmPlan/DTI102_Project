import pygame
import random
import operator
import time
import playerData
 
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TIME_PER_QUESTION = 10
TOTAL_QUESTIONS = 20
BUTTON_SIZE = 80

RESTART_BUTTON_WIDTH = 250
RESTART_BUTTON_HEIGHT = 60

ANSWER_BUTTON_RANGE_X = (SCREEN_WIDTH/7, SCREEN_WIDTH - SCREEN_WIDTH/7)
ANSWER_BUTTON_RANGE_Y = (SCREEN_HEIGHT/3.5, SCREEN_HEIGHT - BUTTON_SIZE * 2)
 
ANSWER_BUTTON_SCALE_X = 10
ANSWER_BUTTON_SCALE_Y = 8
 
 
# Set up
pygame.init()
pygame.font.init()
screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True
 
buttonFont = pygame.font.SysFont("Arial Black", 25)
questionFont = pygame.font.SysFont("Arial Black", 50)
infoFont = pygame.font.SysFont("Arial Black", 20)
restartFont = pygame.font.SysFont("Arial Black", 30)

level = 1
questionLabel = None
choices = {}
game_over = False
time_start = time.time()
restart_button_rect = None
 
def lerp(start, end, amount):
    return start + ((end - start) * amount)
 
def random_question(is_hard_mode = False):
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
    }
    first_num = random.randint(0, 10)
    second_num = random.randint(0, 10)
    third_num = random.randint(0, 10)
 
    operation_symbol1 = random.choice(list(operators.keys()))
    operation_symbol2 = random.choice(list(operators.keys()))
    operation_func1 = operators.get(operation_symbol1)
    operation_func2 = operators.get(operation_symbol2)
 
    result_step1 = operation_func1(first_num, second_num)
 
    if is_hard_mode:
        fourth_num = random.randint(0, 10)
        operation_symbol3 = random.choice(list(operators.keys()))
        operation_func3 = operators.get(operation_symbol3)
 
        result_step2 = operation_func2(result_step1, third_num)
        answer = operation_func3(result_step2, fourth_num)
        question_str = f"  {first_num} {operation_symbol1} {second_num}  {operation_symbol2} {third_num}  {operation_symbol3} {fourth_num} = ?"
    else:
        answer = operation_func2(result_step1, third_num)
        question_str = f" {first_num} {operation_symbol1} {second_num}  {operation_symbol2} {third_num} = ?"
    return question_str, answer
 
def generateChoices(choicesAmount, rightAnswer, wrongAnswers):
    global choices
    choices.clear() 
    availPos = list(range(ANSWER_BUTTON_SCALE_X * ANSWER_BUTTON_SCALE_Y))

    for i in range(choicesAmount):
        pos = random.choice(availPos)
        del availPos[availPos.index(pos)]
        choices[pos] = {}

        if i == 0:
            choices[pos]["label"] = rightAnswer
            choices[pos]["answer"] = True

        else:
            choices[pos]["label"] = wrongAnswers[i - 1]
            choices[pos]["answer"] = False

    scale_x = ANSWER_BUTTON_RANGE_X[1] - ANSWER_BUTTON_RANGE_X[0]
    scale_y = ANSWER_BUTTON_RANGE_Y[1] - ANSWER_BUTTON_RANGE_Y[0]

    grid_width = scale_x / ANSWER_BUTTON_SCALE_X 
    grid_height = scale_y / ANSWER_BUTTON_SCALE_Y
 
    for pos in choices.keys():
        col = pos % ANSWER_BUTTON_SCALE_X
        row = pos // ANSWER_BUTTON_SCALE_X

        center_x = ANSWER_BUTTON_RANGE_X[0] + col * grid_width + grid_width / 2
        center_y = ANSWER_BUTTON_RANGE_Y[0] + row * grid_height + grid_height / 2
 
        x = center_x - BUTTON_SIZE / 2
        y = center_y - BUTTON_SIZE / 2 
        rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE) 
        choices[pos]["rect"] = rect
 
 
def createQuiz(question_number):
    global questionLabel
    choices.clear()
 
    is_hard_mode = (question_number % 5 == 0 and question_number > 0)
    choicesAmount = min((question_number // 5) + 4, 10)
 
    question, answer = random_question(is_hard_mode)
    questionLabel = questionFont.render(question, 0, (0, 0, 0))
 
    wrong_choices = []
    while len(wrong_choices) < (choicesAmount-1):
        deviation = random.randint(-10, 10)
 
        if deviation == 0:
            continue
 
        wrong_choice = str(answer + deviation)
 
        if wrong_choice != answer and wrong_choice not in wrong_choices:
            wrong_choices.append(wrong_choice)
 
 
    generateChoices(choicesAmount, str(answer), wrong_choices)
 
createQuiz(level)

def reset_game():
    global level, game_over, time_start
    level = 1
    game_over = False
    time_start = time.time()
    createQuiz(level)

def mouseInput():
    global level, game_over, time_start, restart_button_rect
    if game_over and restart_button_rect is not None:
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            reset_game()
            restart_button_rect = None
            return
    if not game_over:
        for choice in choices.values():
            rect = choice["rect"]
            if rect.collidepoint(pygame.mouse.get_pos()):
                if choice["answer"]:
                    playerData.addCoins(1)
                    level += 1
                    if level > TOTAL_QUESTIONS:
                        game_over = True
                    else: 
                            createQuiz(level)
                            time_start = time.time()
                else:
                    game_over = True
                return
           
 
while running:
    mouse_pos = pygame.mouse.get_pos() 
    sky_color = (135, 206, 235)
    screen.fill(sky_color) 
    grass_color = (34, 139, 34) 
    grass_start_y = SCREEN_HEIGHT * 2 // 3
    grass_rect = pygame.Rect(0, grass_start_y, SCREEN_WIDTH, SCREEN_HEIGHT - grass_start_y)
    pygame.draw.rect(screen, grass_color, grass_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseInput()

    if not game_over:
        elapsed = time.time() - time_start
        remaining = TIME_PER_QUESTION - elapsed

        if remaining <= 0:
            game_over = True    
            remaining = 0
 
       
        question_box_color = (255, 255, 240) 
        q_width = questionLabel.get_width() + 40
        q_height = questionLabel.get_height() + 20
        q_x = SCREEN_WIDTH/2 - q_width/2
        q_y = 80 - 10 

        playerCoins = playerData.coins

        question_rect = pygame.Rect(q_x, q_y, q_width, q_height)

        pygame.draw.rect(screen, question_box_color, question_rect, border_radius=10) 
        screen.blit(questionLabel, (SCREEN_WIDTH/2 - questionLabel.get_width()/2, 80))

        for choice in choices.values():
            rect = choice["rect"]
            if rect.collidepoint(mouse_pos):
                button_color = (255, 120, 0) 
            else:
                button_color = (255, 223, 0) 

            center_x = rect.x + rect.width // 2
            center_y = rect.y + rect.height // 2
            radius = BUTTON_SIZE // 2

            pygame.draw.circle(screen, button_color, (center_x, center_y), radius)
            label_color = (101, 67, 33) 
            label = buttonFont.render(choice["label"], True, label_color) 
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        info_text = infoFont.render(f"Coins: {playerCoins} | Question: {level}/{TOTAL_QUESTIONS}", True, (200, 0, 0))

        timer_text = infoFont.render(f"Time Left: {remaining:.1f}s", True, (200, 0, 0))
        screen.blit(info_text, (120, 20))
        screen.blit(timer_text, (SCREEN_WIDTH - 250, 20))

    else:
        gameover_text = questionFont.render("Game Over!", 0, (255, 0, 0))
        screen.blit(gameover_text, (SCREEN_WIDTH/2 - gameover_text.get_width()/2, 250))

        coins_text = questionFont.render(f"Your Coins: {playerData.coins}", 0, (0, 0, 0))

        screen.blit(coins_text, (SCREEN_WIDTH/2 - coins_text.get_width()/2, 350))

    if playerCoins == TOTAL_QUESTIONS:

        msg = "You are a Math Genius!"

    elif playerCoins >= TOTAL_QUESTIONS * 0.75:

        msg_text = infoFont.render(msg, 0, (0, 0, 0))
        screen.blit(msg_text, (SCREEN_WIDTH/2 - msg_text.get_width()/2, 40))  

        btn_x = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
        btn_y = 450

        restart_button_rect = pygame.Rect(btn_x, btn_y, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

        if restart_button_rect.collidepoint(mouse_pos):
            btn_color = (255, 110, 0)
        else:
            btn_color = (255, 155, 0)
    
        pygame.draw.rect(screen, btn_color, restart_button_rect, border_radius=10)

        restart_label = restartFont.render("TRY AGAIN", True, (255, 255, 255))
        restart_label_rect = restart_label.get_rect(center=restart_button_rect.center)
        screen.blit(restart_label, restart_label_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
 