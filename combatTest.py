import pygame
import random

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720

BUTTON_SIZE = 65

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

questionLabel = "Test"

# 0 = {answer = false, label = "test", rect = (x, y, sx, sy)}
choices = {}

def lerp(start, end, amount):
    return start + ((end - start) * amount)

import random
import operator
import time

TIME_PER_QUESTION = 10
TOTAl_QUESTIONS = 20

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
        question_str = f"{first_num} {operation_symbol1} {second_num} {operation_symbol2} {third_num} {operation_symbol3} {fourth_num} = ?"
    else:
        answer = operation_func2(result_step1, third_num)
        question_str = f"{first_num} {operation_symbol1} {second_num} {operation_symbol2} {third_num} = ?"
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

def createQuiz(question_number, hardMode = False):
    is_hard_mode = (question_number % 5 == 0)
    choicesAmount = (question_number // 5) + 1

    question, answer = random_question(hardMode)

    generateChoices(choicesAmount, str(answer), ["7", "8", "9"])
    
    

generateChoices(4, "5", ["7", "8", "9"])

while running:
    #choices.clear()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))

    #screen.blit(questionLabel, (500, 0))

    for choice in choices.values():
        rect = choice["rect"]

        pygame.draw.rect(screen, (0, 0, 0), choice["rect"])
        
        label = buttonFont.render(choice["label"], 0, (255, 255, 255))
        labelRect = label.get_rect()
        labelRect.center = rect.center
        screen.blit(label, labelRect)

    pygame.display.flip()

    clock.tick(60)

