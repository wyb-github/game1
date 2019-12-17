import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果没有达到限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_settings,screen,ship,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
                
        elif event.type == pygame.KEYUP:  
            check_keyup_events(event,ship)

def update_bullets(aliens,bullets):
    """更新子弹位置，删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #检查子弹与外星人是否相撞，如果是，同时删除子弹和外星人
    collisions = pygame.sprite.groupcollide(aliens,bullets,True,True)

    if len(aliens) == 0:
        #删除现有的所有子弹，并创建一群新的外星人
        bullets.empty()
        create_fleet(ai_setting,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                             (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):    
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,
                         row_number)

def check_fleet_edges(ai_settings,aliens):
    """判断外星人到达边缘后，采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)

def change_fleet_direction(ai_settings,aliens):
    """在靠近右边框时，逐个下移，并在下一行将其移动方向改为向左"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction = -1

def update_aliens(ai_settings,aliens):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
     
def update_screen(ai_settings,screen,ship,aliens,bullets):
    """更新屏幕上的图像，并切换到新图像"""
    #每次循环重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

     #让最近绘制的屏幕可见
    pygame.display.flip()
    
