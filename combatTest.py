import pygame
import random
import operator
import time
import playerData
import math
 
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TIME_PER_QUESTION = 10
TOTAL_ENEMIES = 20
BUTTON_SIZE = 95

RESTART_BUTTON_WIDTH = 250
RESTART_BUTTON_HEIGHT = 60

ANSWER_BUTTON_RANGE_X = (SCREEN_WIDTH/7, SCREEN_WIDTH - SCREEN_WIDTH/7)
ANSWER_BUTTON_RANGE_Y = (SCREEN_HEIGHT/2.5, SCREEN_HEIGHT - BUTTON_SIZE * 1.5)

player_data = {
    "temp_power_ups": {}, 
    "max_player_hp": 3,
    "player_hp": 3,
    "enemy_base_hp": 5,
    "enemy_hp": 5,
    "enemy_difficulty": 0,
    "clue_master_in_effect": False 
}

SHOP_POWER_UPS = [
    {"name": "+3 Time", "description": "+3 Sec Time", "cost": 15, "effect_key": "TIME_BOOST", "effect_value": 3, "is_active": False, "rect": None, "color": (100, 180, 255)}, 
    {"name": "Remove", "description": "Remove 2 Wrong", "cost": 40, "effect_key": "CLUE_MASTER", "effect_value": 2, "is_active": True, "rect": None, "color": (180, 100, 255)}, 
    {"name": "2x DMG", "description": "2x Attack", "cost": 50, "effect_key": "DMG_MULTIPLIER", "effect_value": 2, "is_active": False, "rect": None, "color": (255, 100, 100)}, 
    {"name": "+1 Shield", "description": "+1 Extra Life", "cost": 30, "effect_key": "LIFE_SAVER", "effect_value": 1, "is_active": False, "rect": None, "color": (218, 165, 32)},
    {"name": "+1 HP", "description": "+1 Max HP", "cost": 80, "effect_key": "MAX_HP_BOOST", "effect_value": 1, "is_active": False, "rect": None, "color": (34, 139, 34)}, 
]


ANSWER_BUTTON_SCALE_X = 10
ANSWER_BUTTON_SCALE_Y = 8
 
 
# Set up
pygame.init()
pygame.font.init()
screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True
 
buttonFont = pygame.font.SysFont("Arial Black", 28)
questionFont = pygame.font.SysFont("Arial Black", 60)
infoFont = pygame.font.SysFont("Arial Black", 20)
restartFont = pygame.font.SysFont("Arial Black", 35)
complimentFont = pygame.font.SysFont("Arial Black", 40)
hpFont = pygame.font.SysFont("Arial Black", 25)

level = 1
questionLabel = None
choices = {}
game_over = False
time_start = time.time()
restart_button_rect = None

GAME_STATE = "PLAYING"
shop_coins_to_add = 0
coin_boxes =[]
coin_mini_game_result = None
reward_box_index = 0

def respawn_enemy():
    global player_data
    player_data["enemy_difficulty"] += 1
    new_max_hp = player_data["enemy_base_hp"] + math.ceil(player_data["enemy_difficulty"] / 2)
    player_data["enemy_hp"] = new_max_hp
    player_data["enemy_max_hp_calc"] = new_max_hp
    print(f"Enemy Respawned! New HP: {new_max_hp}")

def apply_power_up(power_up):
    global player_data
    key = power_up["effect_key"]
    value = power_up["effect_value"]
    if key == "MAX_HP_BOOST":
        player_data["max_player_hp"] += int(value)
        player_data["player_hp"] = player_data["max_player_hp"] 
    if key in ["CLUE_MASTER", "TIME_BOOST", "DMG_MULTIPLIER", "LIFE_SAVER", "MAX_HP_BOOST"]:
        if key in player_data["temp_power_ups"]:
            player_data["temp_power_ups"][key] += value
        else:
            player_data["temp_power_ups"][key] = value 

def buy_power_up(power_up):
    if playerData.coins >= power_up["cost"]:
        playerData.addCoins(-power_up["cost"])
        apply_power_up(power_up)
        return True
    return False

def use_active_power_up(key):
    global player_data
    if key == "CLUE_MASTER":
        if player_data["temp_power_ups"].get(key, 0) >= 1 and not player_data["clue_master_in_effect"]:
            player_data["temp_power_ups"][key] -= 1
            player_data["clue_master_in_effect"] = True
            return True
    return False   

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
        question_str = f"  {first_num} {operation_symbol1} {second_num} {operation_symbol2} {third_num} {operation_symbol3} {fourth_num} = ?"
    else:
        answer = operation_func2(result_step1, third_num)
        question_str = f" {first_num} {operation_symbol1} {second_num} {operation_symbol2} {third_num} = ?"
    return question_str, answer
 
def generateChoices(choicesAmount, rightAnswer, wrongAnswers):
    global choices
    choices.clear() 
    min_x, max_x = ANSWER_BUTTON_RANGE_X
    min_y, max_y = ANSWER_BUTTON_RANGE_Y
    existing_rects = []
    MAX_ATTEMPTS = 150 
    PADDING = 15
    for i in range(choicesAmount):
        choices[i] = {}
        if i == 0:
            choices[i]["label"] = rightAnswer
            choices[i]["answer"] = True
        else:
            choices[i]["label"] = wrongAnswers[i - 1]
            choices[i]["answer"] = False
        
        placed = False
        attempt_count = 0
        while not placed and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            
            rand_x = random.randint(int(min_x), int(max_x - BUTTON_SIZE))
            rand_y = random.randint(int(min_y), int(max_y - BUTTON_SIZE))
            
            new_rect = pygame.Rect(rand_x, rand_y, BUTTON_SIZE, BUTTON_SIZE)
            
            collision = False
            for existing_rect in existing_rects:
                if new_rect.colliderect(existing_rect.inflate(PADDING, PADDING)):
                    collision = True
                    break
            
            if not collision:
                choices[i]["rect"] = new_rect
                existing_rects.append(new_rect)
                placed = True

        if not placed:
            pass

def createQuiz(question_number):
    global questionLabel, player_data
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
    
    if player_data["clue_master_in_effect"]:
        num_to_remove = 2 
        if len(wrong_choices) >= num_to_remove:
            for _ in range(num_to_remove):
                wrong_choices.pop(random.randrange(len(wrong_choices)))
            choicesAmount -= num_to_remove 
        player_data["clue_master_in_effect"] = False

    generateChoices(choicesAmount, str(answer), wrong_choices)
    
createQuiz(level)

def reset_game():
    global level, game_over, time_start, GAME_STATE, coin_mini_game_result, shop_coins_to_add
    level = 1
    score = 0
    game_over = False
    time_start = time.time()
    GAME_STATE = "PLAYING"
    coin_mini_game_result = None
    shop_coins_to_add = 0
    global player_data
    player_data["temp_power_ups"] = {}
    player_data["max_player_hp"] = 3
    player_data["player_hp"] = player_data["max_player_hp"]
    player_data["enemy_base_hp"] = 5
    player_data["enemy_hp"] = 5
    player_data["enemy_difficulty"] = 0
    player_data["enemy_max_hp_calc"] = 5
    player_data["clue_master_in_effect"] = False
    
    createQuiz(level)

def start_coin_minigame():
    global GAME_STATE, coin_boxes, shop_coins_to_add, coin_mini_game_result, reward_box_index
    GAME_STATE = "COIN_MINI_GAME"
    coin_mini_game_result = None

    if level == 6:
       min_c, max_c = 5, 15
    elif level == 11: 
        min_c, max_c = 10, 25
    elif level == 16: 
        min_c, max_c = 15, 35
    else:
        min_c, max_c = 20, 45

    shop_coins_to_add = random.randint(min_c, max_c)
    reward_box_index = random.randint(0, 2)
    coin_boxes.clear()
    box_width = 150
    box_height = 150

    x1 = SCREEN_WIDTH/2 - box_width/2 - 200
    x2 = SCREEN_WIDTH/2 - box_width/2
    x3 = SCREEN_WIDTH/2 - box_width/2 + 200
    
    y = SCREEN_HEIGHT/2 - box_height/2 + 50
    
    coin_boxes.append(pygame.Rect(x1, y, box_width, box_height))
    coin_boxes.append(pygame.Rect(x2, y, box_width, box_height))
    coin_boxes.append(pygame.Rect(x3, y, box_width, box_height))

def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp, is_player=True):
    bg_color = (100, 100, 100)
    if is_player:
        hp_color = (34, 139, 34) 
    else:
        hp_color = (139, 0, 0)
    
    pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=5)
    current_hp = max(0, current_hp) 
    
    fill_width = (current_hp / max_hp) * width
    fill_rect = pygame.Rect(x, y, fill_width, height)
    
    pygame.draw.rect(screen, hp_color, fill_rect, border_radius=5)

def mouseInput():
    global level, score, game_over, time_start, restart_button_rect, GAME_STATE, coin_mini_game_result, player_data
    mouse_pos = pygame.mouse.get_pos()
    if game_over and restart_button_rect is not None:
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            reset_game()
            restart_button_rect = None
        return
    
    if GAME_STATE == "COIN_MINI_GAME":
        if coin_mini_game_result is None:
            for i, box_rect in enumerate(coin_boxes):
                if box_rect.collidepoint(mouse_pos):
                    if i == reward_box_index:
                        playerData.addCoins(shop_coins_to_add)
                        coin_mini_game_result = shop_coins_to_add
                    else:
                        coin_mini_game_result = 0
                    return
        else:
            btn_x = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
            btn_y = 600
            continue_button_rect = pygame.Rect(btn_x, btn_y, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

            if continue_button_rect.collidepoint(mouse_pos):
                GAME_STATE = "SHOP"
                return

    if GAME_STATE == "SHOP":
        for power_up in SHOP_POWER_UPS:
            if power_up.get("rect") and power_up["rect"].collidepoint(mouse_pos):
                if buy_power_up(power_up):
                    return

        btn_x_cont = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
        btn_y_cont = 600
        continue_level_rect = pygame.Rect(btn_x_cont, btn_y_cont, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

        if continue_level_rect.collidepoint(mouse_pos):
            GAME_STATE = "PLAYING"
            coin_mini_game_result = None
            createQuiz(level) 
            time_start = time.time()
            return

    if GAME_STATE == "PLAYING" and not game_over:
        use_skill_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, 650, 200, 40) 
        if use_skill_rect.collidepoint(mouse_pos):
            if use_active_power_up("CLUE_MASTER"):
                createQuiz(level)
            return
        for choice in choices.values():
            rect = choice["rect"]
            if rect.collidepoint(mouse_pos):
                if choice["answer"]:
                    damage = 1
                    playerData.addCoins(2)
                    score += 1 
                    if player_data["temp_power_ups"].get("DMG_MULTIPLIER"):
                        damage *= player_data["temp_power_ups"]["DMG_MULTIPLIER"]
                    player_data["enemy_hp"] -= damage 
                    if player_data["enemy_hp"] <= 0: 
                        level += 1
                        if level > TOTAL_ENEMIES:
                            game_over = True
                        elif level == 4 or level == 7 or level == 10 or level == 13 or level == 16 or level == 19: 
                            start_coin_minigame()
                        else:
                            respawn_enemy() 
                            createQuiz(level)
                            time_start = time.time()
                    else:
                        createQuiz(level) 
                        time_start = time.time()
                else:
                    is_safe = False
                    if player_data["temp_power_ups"].get("LIFE_SAVER", 0) > 0:
                        player_data["temp_power_ups"]["LIFE_SAVER"] -= 1
                        is_safe = True
                        
                    if not is_safe:
                        player_data["player_hp"] -= 1 
                        
                    if player_data["player_hp"] <= 0:
                        game_over = True
                    else:
                        createQuiz(level)
                        time_start = time.time()
                return

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    if GAME_STATE == "PLAYING" or GAME_STATE == "COIN_MINI_GAME":
        sky_color = (135, 206, 235) 
        screen.fill(sky_color) 
        grass_color = (34, 139, 34)
        grass_start_y = SCREEN_HEIGHT * 2 // 3
        grass_rect = pygame.Rect(0, grass_start_y, SCREEN_WIDTH, SCREEN_HEIGHT - grass_start_y)
        pygame.draw.rect(screen, grass_color, grass_rect)

    elif GAME_STATE == "SHOP" or game_over:
        background_top_color = (240, 240, 240)
        background_bottom_color = (180, 220, 255)
        
        screen.fill(background_top_color) 
        
        bottom_rect = pygame.Rect(0, SCREEN_HEIGHT * 2 // 3, SCREEN_WIDTH, SCREEN_HEIGHT // 3)
        pygame.draw.rect(screen, background_bottom_color, bottom_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playerData.saveData()
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseInput()

    if GAME_STATE == "PLAYING" and not game_over:
        time_boost = player_data["temp_power_ups"].get("TIME_BOOST", 0)
        max_time = TIME_PER_QUESTION + time_boost
        elapsed = time.time() - time_start
        remaining = max_time - elapsed

        if remaining <= 0:
            is_safe = False
            if player_data["temp_power_ups"].get("LIFE_SAVER", 0) > 0:
                player_data["temp_power_ups"]["LIFE_SAVER"] -= 1
                is_safe = True

            if not is_safe:
                player_data["player_hp"] -= 1 
            
            if player_data["player_hp"] <= 0:
                game_over = True
            else:
                createQuiz(level) 
                time_start = time.time()
            remaining = 0
            
        bar_width = 250
        bar_height = 30
        
        player_hp_bar_x = 30
        player_hp_bar_y = 60
        draw_hp_bar(screen, player_hp_bar_x, player_hp_bar_y, bar_width, bar_height, player_data["player_hp"], player_data["max_player_hp"], is_player=True)

        playerCoins = playerData.coins
        info_text = infoFont.render(f"Coins: {playerCoins} | Level: {level}/{TOTAL_ENEMIES}", True, (255, 0, 0))
        info_text_x = player_hp_bar_x + (bar_width - info_text.get_width()) / 2 
        screen.blit(info_text, (info_text_x, player_hp_bar_y - info_text.get_height() - 5))
        
        enemy_max_hp_calc = player_data.get("enemy_max_hp_calc", player_data["enemy_base_hp"])
        enemy_hp_bar_x = SCREEN_WIDTH - player_hp_bar_x - bar_width
        enemy_hp_bar_y = 60
        draw_hp_bar(screen, enemy_hp_bar_x, enemy_hp_bar_y, bar_width, bar_height, player_data["enemy_hp"], enemy_max_hp_calc, is_player=False)

        timer_text = infoFont.render(f"Time Left: {remaining:.1f}s", True, (255, 0, 0))
        timer_text_x = enemy_hp_bar_x + (bar_width - timer_text.get_width()) / 2
        screen.blit(timer_text, (timer_text_x, enemy_hp_bar_y - timer_text.get_height() - 5))
        
        question_box_color = (255, 255, 240) 
        q_width = questionLabel.get_width() + 40
        q_height = questionLabel.get_height() + 20
        q_x = SCREEN_WIDTH/2 - q_width/2
        q_y = 150

        question_rect = pygame.Rect(q_x, q_y, q_width, q_height)
        pygame.draw.rect(screen, question_box_color, question_rect, border_radius=10) 
        
        q_center_x = q_x + q_width / 2
        q_center_y = q_y + q_height / 2
        screen.blit(questionLabel, questionLabel.get_rect(center=(q_center_x, q_center_y)))


        for choice in choices.values():
            rect = choice["rect"]
            if rect.collidepoint(mouse_pos):
                button_color = (255, 120, 0) 
            else:
                button_color = (255, 223, 0) 
            if player_data["clue_master_in_effect"] and not choice["answer"]:
                button_color = (150, 150, 150)
            center_x = rect.x + rect.width // 2
            center_y = rect.y + rect.height // 2
            radius = BUTTON_SIZE // 2

            pygame.draw.circle(screen, button_color, (center_x, center_y), radius)
            label_color = (101, 67, 33) 
            label = buttonFont.render(choice["label"], True, label_color) 
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        use_skill_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, 650, 200, 40)
        clue_master_count = player_data["temp_power_ups"].get("CLUE_MASTER", 0)

        if clue_master_count > 0:
            clue_color = (255, 215, 0)
            skill_text = f"SKILL ({clue_master_count})"
        else:
            clue_color = (180, 120, 80)
            skill_text = f"SKILL (0)"

        pygame.draw.rect(screen, clue_color, use_skill_rect, border_radius=5)
        clue_label = infoFont.render(skill_text, True, (0, 0, 0))
        screen.blit(clue_label, clue_label.get_rect(center=use_skill_rect.center))


    elif GAME_STATE == "COIN_MINI_GAME":
        title_text = questionFont.render("Choose a Treasure Box!", 0, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, 150))
        box_color = (139, 69, 19)
        for i, rect in enumerate(coin_boxes):
            current_box_color = (160, 82, 45) if rect.collidepoint(mouse_pos) and coin_mini_game_result is None else box_color
            pygame.draw.rect(screen, current_box_color, rect, border_radius=10)

            if coin_mini_game_result is None:
                box_label = questionFont.render("?", True, (255, 255, 255))
            else:
                if i == reward_box_index:
                    box_label = questionFont.render(f"+{coin_mini_game_result}", True, (255, 255, 0))
                else:
                    box_label = questionFont.render("X", True, (255, 0, 0))

            screen.blit(box_label, box_label.get_rect(center=rect.center))

        if coin_mini_game_result is not None:
            continue_label_text = "GO TO SHOP"

            btn_x = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
            btn_y = 600
            continue_button_rect = pygame.Rect(btn_x, btn_y, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

            if continue_button_rect.collidepoint(mouse_pos):
                btn_color = (0, 150, 200)
            else:
                btn_color = (0, 191, 255)

            pygame.draw.rect(screen, btn_color, continue_button_rect, border_radius=10)
            continue_label = restartFont.render(continue_label_text, True, (255, 255, 255))
            screen.blit(continue_label, continue_label.get_rect(center=continue_button_rect.center))
    
    elif GAME_STATE == "SHOP":
        shop_title = questionFont.render("SHOP - Buy Power-Ups", 0, (0, 0, 0))
        screen.blit(shop_title, (SCREEN_WIDTH/2 - shop_title.get_width()/2, 100))

        current_coins = infoFont.render(f"Your Coins: {playerData.coins}", 0, (200, 0, 0))
        screen.blit(current_coins, (SCREEN_WIDTH/2 - current_coins.get_width()/2, 200))

        start_x = SCREEN_WIDTH/2 - 500
        start_y = 250
        box_width = 180
        box_height = 200
        padding = 40

        for i, power_up in enumerate(SHOP_POWER_UPS):
            x = start_x + (box_width + padding) * i
            rect = pygame.Rect(x, start_y, box_width, box_height)
            power_up["rect"] = rect 

            can_afford = playerData.coins >= power_up["cost"]
            base_color = power_up.get("color", (50, 200, 50))
            if rect.collidepoint(mouse_pos) and can_afford:
                box_color = (min(255, base_color[0] + 30), min(255, base_color[1] + 30), min(255, base_color[2] + 30))
            elif not can_afford:
                box_color = (base_color[0]//2, base_color[1]//2, base_color[2]//2) 
            else:
                box_color = base_color
            pygame.draw.rect(screen, box_color, rect, border_radius=10)

            text_color = (255, 255, 255)
            
            name_label = restartFont.render(power_up["name"], True, (255, 255, 255))
            screen.blit(name_label, name_label.get_rect(center=(rect.centerx, rect.top + 30)))

            desc_label = infoFont.render(power_up["description"], True, (255, 255, 255))
            screen.blit(desc_label, desc_label.get_rect(center=(rect.centerx, rect.top + 70)))

            key = power_up["effect_key"]
            if key != "MAX_HP_BOOST":
                count = player_data["temp_power_ups"].get(key, 0)
                count_label = infoFont.render(f"Own: {count}", True, (255, 255, 0))
                screen.blit(count_label, count_label.get_rect(center=(rect.centerx, rect.bottom - 70)))
            cost_label = restartFont.render(f"{power_up['cost']}", True, (255, 255, 0))
            screen.blit(cost_label, cost_label.get_rect(center=(rect.centerx, rect.bottom - 30)))
        
        btn_x_cont = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
        btn_y_cont = 600
        continue_level_rect = pygame.Rect(btn_x_cont, btn_y_cont, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

        if continue_level_rect.collidepoint(mouse_pos):
            btn_color_cont = (0, 150, 200)
        else:
            btn_color_cont = (0, 191, 255)

        pygame.draw.rect(screen, btn_color_cont, continue_level_rect, border_radius=10)
        continue_label = restartFont.render("CONTINUE", True, (255, 255, 255))
        screen.blit(continue_label, continue_label.get_rect(center=continue_level_rect.center))

    elif game_over:
        playerData.saveData()
        gameover_text = questionFont.render("Game Over!", 0, (255, 0, 0))
        screen.blit(gameover_text, (SCREEN_WIDTH/2 - gameover_text.get_width()/2, 180))
        coins_text = questionFont.render(f"Your Coins: {playerData.coins}", 0, (0, 0, 0))
        screen.blit(coins_text, (SCREEN_WIDTH/2 - coins_text.get_width()/2, 280))

        if level - 1 == TOTAL_ENEMIES:
            msg = "You are a Math Genius!"
        elif level - 1 >= TOTAL_ENEMIES * 0.75:
            msg = "Excellent work! Keep it up!"
        else:
            msg = "Try a little harder next time!"

        msg_text = complimentFont.render(msg, 0, (0, 0, 0))
        screen.blit(msg_text, (SCREEN_WIDTH/2 - msg_text.get_width()/2, 40)) 

        btn_x = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
        btn_y = 400

        restart_button_rect = pygame.Rect(btn_x, btn_y, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

        if restart_button_rect.collidepoint(mouse_pos):
            btn_color = (255, 110, 0)
        else:
            btn_color = (255, 155, 0)
        
        pygame.draw.rect(screen, btn_color, restart_button_rect, border_radius=10)

        restart_text_color = (255, 255, 255) 
        restart_label = restartFont.render("TRY AGAIN", True, restart_text_color)
        restart_label_rect = restart_label.get_rect(center=restart_button_rect.center)
        screen.blit(restart_label, restart_label_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
