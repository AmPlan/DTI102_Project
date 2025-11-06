import pygame
import random
import operator
import time
 
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TIME_PER_QUESTION = 10
TOTAL_QUESTIONS = 20
BUTTON_SIZE = 80
 
ANSWER_BUTTON_RANGE_X = (SCREEN_WIDTH/7, SCREEN_WIDTH - SCREEN_WIDTH/7)
ANSWER_BUTTON_RANGE_Y = (SCREEN_HEIGHT/3.5, SCREEN_HEIGHT - BUTTON_SIZE * 2)
 
ANSWER_BUTTON_SCALE_X = 10
ANSWER_BUTTON_SCALE_Y = 5
 
 
# Set up
pygame.init()
pygame.font.init()
screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True
 
buttonFont = pygame.font.SysFont("Arial", 25)
questionFont = pygame.font.SysFont("Arial", 50)
infoFont = pygame.font.SysFont("Arial", 20)
 
running = True
level = 1
score = 0
questionLabel = None
choices = {}
game_over = False
time_start = time.time()
 
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
 
def generateChoices(choicesAmount, rightAnswer, wrongAnswers): # int, string, [string]
    # Available positions for button
    availPos = list(range(ANSWER_BUTTON_SCALE_X * ANSWER_BUTTON_SCALE_Y))
   
    # set position for choices
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
 
    #   0   1   2   3   4
    #   5   6   7   8   9
    #   10  11  12  13  14
    for pos in choices.keys():
        x = lerp(ANSWER_BUTTON_RANGE_X[0], ANSWER_BUTTON_RANGE_X[1], (pos % ANSWER_BUTTON_SCALE_X) / ANSWER_BUTTON_SCALE_X)
        y = lerp(ANSWER_BUTTON_RANGE_Y[0], ANSWER_BUTTON_RANGE_Y[1], (pos // ANSWER_BUTTON_SCALE_X) / ANSWER_BUTTON_SCALE_Y)
 
        rect = pygame.Rect(x, y + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
        choices[pos]["rect"] = rect
 
def createQuiz(question_number):
    global questionLabel
 
    # Clear old question and answers
    choices.clear()
 
    is_hard_mode = (question_number % 5 == 0)
    choicesAmount = (question_number // 5) + 4
 
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
 
def mouseInput():
    global level, score, game_over
    for choice in choices.values():
        rect = choice["rect"]
        if rect.collidepoint(pygame.mouse.get_pos()):
            if choice["answer"]:
                score += 1  
                level += 1
                if level > TOTAL_QUESTIONS:
                    game_over = True
                else:
                    createQuiz(level)
            else:
                game_over = True
            return
           
 
while running:
 
    screen.fill((255, 255, 255))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over and event.type == pygame.MOUSEBUTTONUP:
            mouseInput()
 
    if not game_over:
        #time
        elapsed = time.time() - time_start
        remaining = TIME_PER_QUESTION - elapsed
 
        if remaining <= 0:
            game_over = True    
            remaining = 0
 
        screen.blit(questionLabel, (SCREEN_WIDTH/2 - questionLabel.get_width()/2, 80))
 
        for choice in choices.values():
            rect = choice["rect"]
            pygame.draw.rect(screen, (0, 110, 255), rect)
            label = buttonFont.render(choice["label"], True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
       
        info_text = infoFont.render(f"Score: {score} | Question: {level}/{TOTAL_QUESTIONS}", True, (200, 0, 0))
        timer_text = infoFont.render(f"Time Left: {remaining:.1f}s", True, (200, 0, 0))
        screen.blit(info_text, (120, 20))
        screen.blit(timer_text, (SCREEN_WIDTH - 250, 20))
    else:
        gameover_text = questionFont.render("Game Over!", 0, (255, 0, 0))
        screen.blit(gameover_text, (SCREEN_WIDTH/2 - gameover_text.get_width()/2, 250))
 
        score_text = questionFont.render(f"Your Score: {score}", 0, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, 350))
 
    if score == TOTAL_QUESTIONS:
        msg = "Perfect Score ! You are a Math Genius!"
    elif score >= TOTAL_QUESTIONS * 0.75:
        msg = "Excellent work!"      
    else:
        msg = ""
 
    msg_text = infoFont.render(msg, 0, (0, 0, 0))
    screen.blit(msg_text, (SCREEN_WIDTH/2 - msg_text.get_width()/2, 40))  
 
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()