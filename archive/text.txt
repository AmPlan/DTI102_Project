import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Shooting Game")
background, obstacle, enemy, enemy_fire, enemy_die, rifle_left, rifle_right, rifle_direction

if(score = 0):
    game_time = 30 = [pygame.image.load(img) for img in [
      enemy_visible = False
      enemy_position = (x, y)
      enemy_action = enemy
      timer = 0

  เริ่มลูปหลักของเกม:
      ตรวจจับเหตุการณ์ (เช่น กดstart)
      อัปเดตเวลา

      ถ้า enemy ไม่โผล่:
          รอเวลาสุ่มแล้วให้ enemy_visible = True
          enemy_position = สุ่มตำแหน่งใหม่
           enemy_action = สุ่ม("enemy", "enemy_fire")

      ถ้า enemy โผล่ครบเวลาที่กำหนด:
          enemy_visible = False

      ถ้ามีการคลิกเมาส์:
          ตรวจสอบว่าคลิกโดน enemy, enemy_fire หรือไม่
          ถ้าโดน:
              เพิ่ม score
	      เพิ่ม  game_time = 5
	      เพิ่ม   enemy_die
              ซ่อน enemy_die

      ตรวจสอบตำแหน่งเมาส์:
          ถ้าเมาส์อยู่ทางซ้ายจอ → rifle_direction = "left"
          ถ้าเมาส์อยู่ทางขวาจอ → rifle_direction = "right"

      วาดพื้นหลัง
      วาดobstacleทั้งหมด

      ถ้า enemy_visible:
          ถ้า enemy_action == "enemy":
              วาด enemy ที่ enemy_position
          elif enemy_action == "enemy_fire":
              วาด enemy_fire ที่ enemy_position

      วาดrifleตามตำแหน่งเมาส์และ rifle_direction
      แสดงคะแนนและเวลา

      ถ้าgame_time == 0:
          แสดงหน้าจอ Game Over