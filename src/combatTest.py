import pygame
import random
import operator
import time
import playerData
import math

import pygame.mixer_music as music

from constants.ShopPowerUps import SHOP_POWER_UPS

# Player at game over screen
player = pygame.image.load(r"./Asset/Player.png")
player = pygame.transform.scale(player, (550, 550))
playerX, playerY = (0, 440)

# Player but hurting at game over screen
Hurt = pygame.image.load(r"./Asset/HURT.png")
Hurt = pygame.transform.scale(Hurt, (600, 700))
HurtX, HurtY = (0, 360)

# Player at combat scene
playerCharacter = pygame.image.load(playerData.playerCharacter)
playerCharacter = pygame.transform.scale(playerCharacter, (225, 225))

# Player Hurt at combat scene
playerCharacterHurt = pygame.image.load(r"./Asset/Hurt.png")
playerCharacterHurt = pygame.transform.scale(playerCharacterHurt, (300, 350))

# name = {NormalImage : ... , HurtImage : ...}
enemyCharacters = {}

# set player last damage time 
lastPlayerDamageTime = time.time()
lastEnemyDamageTime = time.time()

def addEnemy(name, normalPath, normalTransform, hurtPath, hurtTransform, pos, hurtPos):
    enemy = pygame.image.load(normalPath)
    enemy = pygame.transform.scale(enemy, normalTransform)

    enemyHurt = pygame.image.load(hurtPath)
    enemyHurt = pygame.transform.scale(enemyHurt, hurtTransform)

    enemyCharacters[name] = {
        "NormalImage" : enemy,
        "HurtImage" : enemyHurt,
        "Position" : pos,
        "HurtPosition" : hurtPos
        }
        
addEnemy("enemy1", r"Asset\mini_Boss1.png", (300, 300), r"./Asset/C1.png", (300, 300), (1000, 330), (1000, 330))
addEnemy("enemy2", r"Asset\mini_Boss2.png", (350, 350), r"./Asset/C3.png", (350, 350), (960, 310), (960, 310))
addEnemy("enemy3", r"Asset\mini_Boss3.png", (400, 400), r"./Asset/C4.png", (200, 200), (925, 240), (1025, 440))

addEnemy("Final", r"Asset\Final Boss1.png", (400, 400), r"Asset\Final Boss1.png", (400, 400), (925, 240), (1025, 440))

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TIME_PER_QUESTION = 10
TOTAL_ENEMIES = 20
BUTTON_SIZE = 95

HP_BAR_WIDTH  = 250
HP_BAR_HEIGHT = 30

PLAYER_HP_BAR_X = 30
PLAYER_HP_BAR_Y = 650

ENEMY_HP_BAR_X = SCREEN_WIDTH - PLAYER_HP_BAR_X - HP_BAR_WIDTH
ENEMY_HP_BAR_Y = 650

RESTART_BUTTON_WIDTH = 250
RESTART_BUTTON_HEIGHT = 60

WHITE_FONT_COLOR = (255, 255, 255)
BLACK_FONT_COLOR = (0, 0, 0)
CHOICE_FONT_COLOR = (101, 67, 33)

SHOP_PRODUCT_X = SCREEN_WIDTH/2 - 525
SHOP_PRODUCT_Y = 250
SHOP_PRODUCT_WIDTH  = 180
SHOP_PRODUCT_HEIGHT = 200
SHOP_PRODUCT_PADDING = 40

CONTINUE_BUTTON_COLOR = ((0, 191, 255), (0, 150, 200)) # (Default, Hover)
RESTART_BUTTON_COLOR = ((255, 155, 0), (255, 110, 0))
CLUE_BUTTON_COLOR = ((255, 215, 0), (255, 170, 0))

ANSWER_BUTTON_RANGE_X = (SCREEN_WIDTH/7, SCREEN_WIDTH - SCREEN_WIDTH/7)
ANSWER_BUTTON_RANGE_Y = (SCREEN_HEIGHT/2.5, SCREEN_HEIGHT - BUTTON_SIZE * 1.5)

ANSWER_BUTTON_SCALE_X = 10
ANSWER_BUTTON_SCALE_Y = 8

CONTINUE_LEVEL_RECT = pygame.Rect(SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2, 600, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

RESTART_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2, 500, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)
USE_SKILL_RECT      = pygame.Rect(SCREEN_WIDTH/2 - 150, 650, 300, 40) 

# Sounds
PLAYER_ATTACK_SOUNDS = [
    pygame.mixer.Sound(r"Asset\sounds\DSGNImpt_MELEE-Magic Kick_HY_PC-001.wav"),
    pygame.mixer.Sound(r"Asset\sounds\DSGNImpt_MELEE-Magic Kick_HY_PC-002.wav"),
    pygame.mixer.Sound(r"Asset\sounds\DSGNImpt_MELEE-Magic Kick_HY_PC-003.wav")
]
ENEMY_ATTACK_SOUNDS = [
    pygame.mixer.Sound(r"Asset\sounds\FGHTImpt_MELEE-Swish Hit_HY_PC-001.wav"),
    pygame.mixer.Sound(r"Asset\sounds\FGHTImpt_MELEE-Swish Hit_HY_PC-002.wav"),
    pygame.mixer.Sound(r"Asset\sounds\FGHTImpt_MELEE-Swish Hit_HY_PC-003.wav")
]
ENEMY_DEFEAT_SOUND = pygame.mixer.Sound(r"Asset\sounds\DSGNMisc_HIT-Gore Pierce_HY_PC-006.wav")
SHOP_UPGRADE_SOUND = pygame.mixer.Sound(r"Asset\sounds\DSGNSynth_BUFF-Mecha Level Up_HY_PC-006.wav")
CLUE_MASTER_SOUND  = pygame.mixer.Sound(r"Asset\sounds\DSGNTonl_SKILL RELEASE-Whimsy Kick_HY_PC-006.wav")
LIFE_SAVER_SOUND   = pygame.mixer.Sound(r"Asset\sounds\MAGAngl_BUFF-Mecha Regen_HY_PC-002.wav")
TREASURE_BOX_SOUND = pygame.mixer.Sound(r"Asset\sounds\DSGNTonl_USABLE-Coin Spend_HY_PC-006.wav")
GAME_OVER_SOUND    = pygame.mixer.Sound(r"Asset\sounds\shocked-sound-effect.mp3")

# Fonts
HEALTH_FONT     = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 30)
INFO_FONT       = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 30)
BUTTON_FONT     = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 28)
RESTART_FONT    = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 35)
COMPLIMENT_FONT = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 40)
QUESTION_FONT   = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 60)


player_data = {
    "temp_power_ups": {}, 
    "max_player_hp": 4,
    "player_hp":4,
    "enemy_base_hp": 5,
    "enemy_hp": 5,
    "enemy_difficulty": 0,
    "enemy_max_hp": 5,
    "enemy_damage": 1,
    "clue_master_in_effect": False 
}

def createBackground(path):
    background = pygame.image.load(path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    rect = background.get_rect()
    rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    return background, rect

def playRandomSound(sounds):
    sound = random.choice(sounds)
    sound.play()

def playMusic(musicName):
    match musicName:
        case "NORMAL_BATTLE":
            music.load(r"Asset\musics\Battle-Noble.mp3")
        case "BOSS_BATTLE":
            music.load(r"Asset\mini.mp3")
        case "FINAL_BATTLE":
            music.load(r"Asset\musics\Battle-ricercare.mp3")
        case "GAME_OVER":
            music.load(r"Asset\musics\childhood.mp3")
        case "SHOP":
            music.load(r"Asset\musics\Sneaky Snitch.mp3")
    music.play(loops=-1) # เล่นไปเรื่อยๆ ไม่มีวันจบ

def init(screen, clock):
    # Combat background
    backgroundCombat, backgroundCombatRect = createBackground(r"Asset\images\battleBackground.jpg")
    backgroundShop,   backgroundShopRect   = createBackground(r"Asset\images\SevenEleven.jpg")

    operators = {
            "+": operator.add,
            "-": operator.sub,
            "×": operator.mul,
        }

    global current_enemy, choices, questionLabel, GAME_STATE, level, RESTART_BUTTON_RECT, time_start, coin_boxes, coin_mini_game_result, shop_coins_to_add, reward_box_index

    running = True
    level = 1
    questionLabel = None
    choices = {}
    time_start = 0

    # switch to show normal player or show hurting player
    ShowPlayer = False
    ShowHurt = False

    current_enemy = None

    GAME_STATE = "SHOP"
    playMusic("SHOP")
    
    reward_box_index = 0
    shop_coins_to_add = 0
    coin_mini_game_result = None
    coin_boxes =[]

    def respawn_enemy():
        
        global player_data, current_enemy

        if level != 20:
            enemiesToSelect = list(enemyCharacters.keys())

            enemiesToSelect.remove("Final")

            if current_enemy in enemiesToSelect:
                enemiesToSelect.remove(current_enemy)

            current_enemy = random.choice(enemiesToSelect)
        else:
            current_enemy = "Final"

        player_data["enemy_difficulty"] += 1

        new_max_hp = player_data["enemy_base_hp"] + math.floor(player_data["enemy_difficulty"] / 3)

        player_data["enemy_hp"] = new_max_hp
        player_data["enemy_max_hp"] = new_max_hp

        player_data["enemy_damage"] = math.ceil(player_data["enemy_difficulty"] / 3)

        if level == 20:
            playMusic("FINAL_BATTLE")
            player_data["enemy_max_hp"] = 100
            player_data["enemy_hp"] = 100
            player_data["enemy_damage"] = 10
        elif level % 3 == 0:
            playMusic("BOSS_BATTLE")

        print(f"Enemy Respawned! New HP: {new_max_hp}")

    def apply_power_up(power_up):
        # "name": "+1 HP",
        # "description": "+1 Max HP",
        # "cost": 80,
        # "effect_key": "MAX_HP_BOOST",
        # "effect_value": 1,
        # "is_active": False,
        # "rect": None,
        # "color": (34, 139, 34),
# 
        global player_data

        key   = power_up["effect_key"]
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
            power_up["cost"] = math.ceil(power_up["cost"] * 1.2)
            apply_power_up(power_up)
            return True
        return False

    def use_clue_master():
        global player_data
        print("rest")

        if player_data["temp_power_ups"].get("CLUE_MASTER", 0) >= 1 and not player_data["clue_master_in_effect"]:
            player_data["temp_power_ups"]["CLUE_MASTER"] -= 1
            player_data["clue_master_in_effect"] = True
            return True
        
        return False   

    def random_question(is_hard_mode = False):
        
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

            attempt_count = 0
            # พยายามหาตำแหน่งที่ไม่มีปุ่มจองเอาไว้ ถ้าลอง MAX_ATTEMPTS ครั้งแล้วไม่พบก็ยอมแพ้ไป~
            while attempt_count < MAX_ATTEMPTS:
                attempt_count += 1

                rand_x = random.randint(int(min_x), int(max_x - BUTTON_SIZE))
                rand_y = random.randint(int(min_y), int(max_y - BUTTON_SIZE))

                new_rect = pygame.Rect(rand_x, rand_y, BUTTON_SIZE, BUTTON_SIZE)

                collision = False
                for existing_rect in existing_rects:
                    # inflate คือ ขยายขนาด rect ด้วยค่า X, Y
                    if new_rect.colliderect(existing_rect.inflate(PADDING, PADDING)):
                        collision = True
                        break
                
                # ถ้าสุ่มแล้วไม่ทับกับปุ่มอื่นก็เอาปุ่มเข้าไป~
                if not collision:
                    choices[i]["rect"] = new_rect
                    existing_rects.append(new_rect)
                    break

    def createQuiz(question_level):
        global questionLabel, player_data, time_start
        
        time_start = time.time()
    
        is_hard_mode = (question_level % 3 == 0) or (question_level == 20)
        choicesAmount = min((question_level // 5) + 4, 10)
    
        question, answer = random_question(is_hard_mode)

        questionLabel = QUESTION_FONT.render(question, 0, BLACK_FONT_COLOR)
    
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

        generateChoices(choicesAmount, str(answer), wrong_choices)

    createQuiz(level)

    def reset_game():
        global level, time_start, GAME_STATE, coin_mini_game_result, shop_coins_to_add
        level = 1
        time_start = time.time()
        GAME_STATE = "SHOP"
        playMusic("SHOP")
        coin_mini_game_result = None
        shop_coins_to_add = 0

        global player_data
        #player_data["temp_power_ups"] = {}
        player_data["player_hp"] = player_data["max_player_hp"]
        player_data["enemy_base_hp"] = 5
        player_data["enemy_hp"] = 5
        player_data["enemy_difficulty"] = 0
        player_data["enemy_max_hp"] = 5
        player_data["clue_master_in_effect"] = False

        createQuiz(level)

    def start_coin_minigame():
        global GAME_STATE, shop_coins_to_add, coin_mini_game_result, reward_box_index, coin_boxes
        GAME_STATE = "COIN_MINI_GAME"
        
        coin_mini_game_result = None

        if level <= 6:
           min_c, max_c = 5, 15
        elif level <= 11: 
            min_c, max_c = 10, 25
        elif level <= 16: 
            min_c, max_c = 15, 35
        else:
            min_c, max_c = 20, 45

        shop_coins_to_add = random.randint(min_c, max_c)
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

    def createButton(font, text, textColor, rect, backgroundColor, borderRadius=5):
 
        if rect.collidepoint(mouse_pos):
            btn_color = backgroundColor[1]
        else:
            btn_color = backgroundColor[0]

        pygame.draw.rect(screen, btn_color, rect, border_radius=borderRadius)
        label = font.render(text, True, textColor)
        screen.blit(label, label.get_rect(center=rect.center))

    def draw_hp_bar(screen, x, y, is_player=True):
        bg_color = (50, 50, 50)

        if is_player:
            hp_color   = (34, 139, 34) 
            current_hp = player_data["player_hp"]
            max_hp     = player_data["max_player_hp"]
        else:
            hp_color = (255, 0, 0)
            current_hp = player_data["enemy_hp"]
            max_hp     = player_data.get("enemy_max_hp", player_data["enemy_base_hp"])

        bg_rect_border = pygame.Rect(x-2.5, y-2.5, HP_BAR_WIDTH+5, HP_BAR_HEIGHT+5)
        bg_rect = pygame.Rect(x, y, HP_BAR_WIDTH, HP_BAR_HEIGHT)

        pygame.draw.rect(screen, (0, 0, 0), bg_rect_border, border_radius=5)
        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=5)
        current_hp = max(0, current_hp) 

        fill_width = (current_hp / max_hp) * HP_BAR_WIDTH
        fill_rect = pygame.Rect(x, y, fill_width, HP_BAR_HEIGHT)

        pygame.draw.rect(screen, hp_color, fill_rect, border_radius=5)

        text = f"{current_hp} / {max_hp}"

        healthLabel = HEALTH_FONT.render(text, True, WHITE_FONT_COLOR)
        healthLabelRect = healthLabel.get_rect()
        healthLabelRect.center = bg_rect.center

        screen.blit(healthLabel, healthLabelRect)

    def playerTakeDamage():
        
        global GAME_STATE, lastPlayerDamageTime

        player_data["player_hp"] -= player_data["enemy_damage"]
        
        if player_data["player_hp"] > 0:
            lastPlayerDamageTime = time.time()
            playRandomSound(ENEMY_ATTACK_SOUNDS)
            createQuiz(level)
               
            return
            
        # ถ้ามีพลัง Life saver จะรอดตุย HP กลับมาเป็น 1 ใน 3 
        if player_data["temp_power_ups"].get("LIFE_SAVER", 0) > 0:
            LIFE_SAVER_SOUND.play()
            player_data["temp_power_ups"]["LIFE_SAVER"] -= 1
            player_data["player_hp"] = math.ceil(player_data["max_player_hp"] / 3)
        else:
            GAME_OVER_SOUND.play()
            GAME_STATE = "GAME_OVER"
            playMusic("GAME_OVER")
             
    def mouseInput():
        global level, GAME_STATE, coin_mini_game_result, player_data, reward_box_index
        mouse_pos = pygame.mouse.get_pos()
        
        match GAME_STATE:
            case "GAME_OVER":
                if RESTART_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
                    reset_game()
                
            case "COIN_MINI_GAME":
                
                if coin_mini_game_result is None:
                    for i, box_rect in enumerate(coin_boxes):
                        if not box_rect.collidepoint(mouse_pos): 
                            continue

                        playerData.addCoins(shop_coins_to_add)
                        coin_mini_game_result = shop_coins_to_add
                        
                        reward_box_index = i

                        TREASURE_BOX_SOUND.play()

                else:
                    continue_button_rect = pygame.Rect(SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2, 600, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

                    if continue_button_rect.collidepoint(mouse_pos):
                        GAME_STATE = "SHOP"
                        playMusic("SHOP")
                        
            case "SHOP":
                for power_up in SHOP_POWER_UPS:
                    if power_up.get("rect") and power_up["rect"].collidepoint(mouse_pos):
                        if buy_power_up(power_up):
                            SHOP_UPGRADE_SOUND.play()
                            return                

                if CONTINUE_LEVEL_RECT.collidepoint(mouse_pos):
                    GAME_STATE = "PLAYING"
                    player_data["player_hp"] = player_data["max_player_hp"]
                    playMusic("NORMAL_BATTLE")
                    coin_mini_game_result = None
                    respawn_enemy()
                    createQuiz(level) 
                    return

            case "PLAYING":
                
                if USE_SKILL_RECT.collidepoint(mouse_pos):
                    if use_clue_master():
                        CLUE_MASTER_SOUND.play()
                        createQuiz(level)
                        return

                for choice in choices.values():
                    rect = choice["rect"]
                    
                    if not rect.collidepoint(mouse_pos):
                        continue
                    
                    player_data["clue_master_in_effect"] = False

                    if choice["answer"]:
                        damage = 1
                        playerData.addCoins(2)

                        if player_data["temp_power_ups"].get("DMG_MULTIPLIER"):
                            damage += player_data["temp_power_ups"]["DMG_MULTIPLIER"]

                        player_data["enemy_hp"] -= damage 

                        if player_data["enemy_hp"] <= 0: 
                            ENEMY_DEFEAT_SOUND.play()
                            level += 1
                            if level > TOTAL_ENEMIES:
                                GAME_STATE = "GAME_OVER"
                                playMusic("GAME_OVER")
                            elif level == 4 or level == 7 or level == 10 or level == 13 or level == 16 or level == 19: 
                                start_coin_minigame()
                            else:
                                playerData.addCoins(math.floor(5 * ((level / 5) + 1)))
                                respawn_enemy() 
                                createQuiz(level)
                        else:
                            global lastEnemyDamageTime
                            lastEnemyDamageTime = time.time()
                            playRandomSound(PLAYER_ATTACK_SOUNDS)
                            createQuiz(level) 
                    else:
                        playerTakeDamage()
                    return

    def getGameOverMessage():
        if level - 1 == TOTAL_ENEMIES:
            return "You are a Math Genius!"
        elif level - 1 >= TOTAL_ENEMIES * 0.75:
            return "Excellent work! Keep it up!"
        else:
            return "Try a little harder next time!"        

    while running:
        mouse_pos = pygame.mouse.get_pos()

        if GAME_STATE == "PLAYING" or GAME_STATE == "COIN_MINI_GAME":
            screen.blit(backgroundCombat, backgroundCombatRect)

        elif GAME_STATE == "SHOP" or GAME_STATE == "GAME_OVER":
            screen.blit(backgroundShop, backgroundShopRect)

        ShowHurt = False
        ShowPlayer = True 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseInput()

            ShowHurt = True
            ShowPlayer = False                    

        match GAME_STATE:
            case "PLAYING":
                time_boost = player_data["temp_power_ups"].get("TIME_BOOST", 0)
                max_time = TIME_PER_QUESTION + time_boost
                elapsed = time.time() - time_start
                remaining = max_time - elapsed

                if remaining <= 0:
                    playerTakeDamage()
                    remaining = 0

                draw_hp_bar(screen, PLAYER_HP_BAR_X, PLAYER_HP_BAR_Y, is_player=True)

                draw_hp_bar(screen, ENEMY_HP_BAR_X, ENEMY_HP_BAR_Y, is_player=False)


                playerCoins = playerData.coins

                info_text = INFO_FONT.render(f"Coins: {playerCoins} | Level: {level}/{TOTAL_ENEMIES}", True, (255, 0, 0))
                
                info_text_x = PLAYER_HP_BAR_X + (HP_BAR_WIDTH - info_text.get_width()) / 2 
                
                screen.blit(info_text, (info_text_x, 50))
                
                enemy = enemyCharacters[current_enemy]

                if time.time() - lastEnemyDamageTime < 0.2:
                    screen.blit(enemy["HurtImage"], enemy["HurtPosition"])
                else:
                    screen.blit(enemy["NormalImage"], enemy["Position"])

                if time.time() - lastPlayerDamageTime < 0.2:
                    screen.blit(playerCharacterHurt, (25, 380))
                else:
                    screen.blit(playerCharacter, (25, 430))


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
                
                timer_text = INFO_FONT.render(f"Time Left: {remaining:.1f}s", True, (255, 0, 0))

                screen.blit(timer_text, timer_text.get_rect(center=(q_center_x, q_center_y +55)))


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

                    label = BUTTON_FONT.render(choice["label"], True, CHOICE_FONT_COLOR) 
                    label_rect = label.get_rect(center=rect.center)

                    screen.blit(label, label_rect)

                clue_master_count = player_data["temp_power_ups"].get("CLUE_MASTER", 0)

                if clue_master_count > 0:
                    skill_text = f"Use clue master ({clue_master_count})"

                    createButton(INFO_FONT, skill_text, BLACK_FONT_COLOR, USE_SKILL_RECT, CLUE_BUTTON_COLOR)

            case "COIN_MINI_GAME":
                title_text = QUESTION_FONT.render("Choose a Treasure Box!", 0, WHITE_FONT_COLOR)
                screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, 150))
                box_color = (139, 69, 19)
                for i, rect in enumerate(coin_boxes):
                    current_box_color = (160, 82, 45) if rect.collidepoint(mouse_pos) and coin_mini_game_result is None else box_color
                    pygame.draw.rect(screen, current_box_color, rect, border_radius=10)
                    if coin_mini_game_result is None:
                        box_label = QUESTION_FONT.render("?", True, WHITE_FONT_COLOR)
                    else:
                        if i == reward_box_index:
                            box_label = QUESTION_FONT.render(f"+{coin_mini_game_result}", True, (255, 255, 0))
                        else:
                            box_label = QUESTION_FONT.render("?", True, WHITE_FONT_COLOR)

                    screen.blit(box_label, box_label.get_rect(center=rect.center))

                if coin_mini_game_result is not None:
                    continue_label_text = "Back to 7-11"

                    btn_x = SCREEN_WIDTH/2 - RESTART_BUTTON_WIDTH/2
                    btn_y = 600
                    continue_button_rect = pygame.Rect(btn_x, btn_y, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)
                    
                    createButton(RESTART_FONT, continue_label_text, WHITE_FONT_COLOR, continue_button_rect, CONTINUE_BUTTON_COLOR, 10)

            case "SHOP":
                shop_title = QUESTION_FONT.render("Welcome to 7-11!", 0, WHITE_FONT_COLOR)
                screen.blit(shop_title, (SCREEN_WIDTH/2 - shop_title.get_width()/2, 100))

                current_coins = INFO_FONT.render(f"Your Coins: {playerData.coins}", 0, (200, 0, 0))
                screen.blit(current_coins, (SCREEN_WIDTH/2 - current_coins.get_width()/2, 200))


                for i, power_up in enumerate(SHOP_POWER_UPS):
                    x = SHOP_PRODUCT_X + (SHOP_PRODUCT_WIDTH + SHOP_PRODUCT_PADDING) * i
                    
                    rect = pygame.Rect(x, SHOP_PRODUCT_Y, SHOP_PRODUCT_WIDTH, SHOP_PRODUCT_HEIGHT)
                    
                    power_up["rect"] = rect 

                    can_afford = (playerData.coins >= power_up["cost"])
                    base_color = power_up.get("color", (50, 200, 50))

                    if rect.collidepoint(mouse_pos) and can_afford:
                        box_color = (min(255, base_color[0] + 30), min(255, base_color[1] + 30), min(255, base_color[2] + 30))
                    elif not can_afford:
                        box_color = (base_color[0]//2, base_color[1]//2, base_color[2]//2) 
                    else:
                        box_color = base_color
                    
                    pygame.draw.rect(screen, box_color, rect, border_radius=10)

                    name_label = RESTART_FONT.render(power_up["name"], True, (255, 255, 255))
                    screen.blit(name_label, name_label.get_rect(center=(rect.centerx, rect.top + 30)))

                    desc_label = INFO_FONT.render(power_up["description"], True, (255, 255, 255))
                    screen.blit(desc_label, desc_label.get_rect(center=(rect.centerx, rect.top + 70)))

                    key = power_up["effect_key"]
                    count = player_data["temp_power_ups"].get(key, 0)
                    
                    count_label = INFO_FONT.render(f"+{count}", True, (255, 255, 0))
                    screen.blit(count_label, count_label.get_rect(center=(rect.centerx, rect.bottom - 70)))
                    
                    cost_label = RESTART_FONT.render(f"{power_up['cost']}", True, (255, 255, 0))
                    screen.blit(cost_label, cost_label.get_rect(center=(rect.centerx, rect.bottom - 30)))

                
                createButton(RESTART_FONT, "Destroy the office!", WHITE_FONT_COLOR, CONTINUE_LEVEL_RECT, CONTINUE_BUTTON_COLOR, 10)

            case "GAME_OVER":

                gameover_text = QUESTION_FONT.render("AJ.Nok gave you F! (again)", 0, (255, 0, 0))
                screen.blit(gameover_text, (SCREEN_WIDTH/2 - gameover_text.get_width()/2, 180))

                coins_text = QUESTION_FONT.render(f"Your Coins: {playerData.coins}", 0, (255, 255, 255))
                screen.blit(coins_text, (SCREEN_WIDTH/2 - coins_text.get_width()/2, 400))

                msg = getGameOverMessage()
                
                msg_text = COMPLIMENT_FONT.render(msg, 0, WHITE_FONT_COLOR)
                screen.blit(msg_text, (SCREEN_WIDTH/2 - msg_text.get_width()/2, 40)) 

                createButton(RESTART_FONT, "Back to 7-11", WHITE_FONT_COLOR, RESTART_BUTTON_RECT, RESTART_BUTTON_COLOR, 10)
        
                if ShowPlayer:
                    screen.blit(player, (playerX, playerY))
                if ShowHurt:
                    screen.blit(Hurt, (HurtX, HurtY))
        

        pygame.display.flip()

        clock.tick(60)
    
    pygame.quit()

