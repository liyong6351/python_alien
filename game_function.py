import sys
import pygame
from bullet import Bullet
from alien import Alien
from button import Button
from time import sleep

# 检测按钮按下事件
def check_keydown_events(event,ai_settings, screen, ship, bullets):
    # 如果是q则退出
    if event.key == pygame.K_q:
        sys.exit()
    # 响应向右移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        ship.rect.centerx += 1
    # 响应向左
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        ship.rect.centerx -= 1
    # 响应空格键
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

# 检测按钮放开事件
def check_keyup_events(event, ship):
    # 放开向右的按钮
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 放开向右的按钮
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

# 检测按键和鼠标事件
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # 响应按键和鼠标事件
    for event in pygame.event.get():
        # 响应退出按钮
        if event.type == pygame.QUIT:
            sys.exit()
        # 响应按钮按下动作
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        # 响应按键放开动作
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        # 响应鼠标按键
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

# 点击Play按钮开始新的游戏
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # 重置游戏设置
            ai_settings.initialized_dynamic_settings()
            # 隐藏光标
            pygame.mouse.set_visible(False)
            # 重置游戏统计信息
            stats.reset_stats()
            stats.game_active = True

            # 清空外星人列表和子弹列表
            aliens.empty()
            bullets.empty()

            # 重置记分牌图像
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # 创建一群外星人，并让飞船居中
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

# 更新屏幕
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    
    aliens.draw(screen)
    ship.blitme()

    # 显示得分
    sb.show_score()
    # 如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

# 更新子弹
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 更新子弹的位置
    bullets.update()

    # 并删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

# 处理子弹和外星人碰撞同时删除发生的子弹和外星人，同时检测是否需要重新绘制外星人
def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人，如果是，则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()
    check_high_score(stats, sb)

    if len(aliens) ==0:
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


# 发射子弹
def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一个子弹放入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

# 创建外星人群
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

# 计算每行可容纳多少个外星人
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

# 计算列数
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

# 创建外星人
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其加入到当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

# 更新外星人数组中的所有外星人位置
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    check_alien_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

# 响应外星人撞到飞船
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):

    if stats.ships_left > 0:
        # 将ships_left的数值减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群外星人，并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        # 将飞船居中
        ship.center_ship()
        
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# 有外星人到达边缘时采取相应的措施
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

# 整体下移并修改外星人的位置
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

# 检查是否由外星人达到了屏幕底端
def check_alien_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

# 检查是否诞生了最高分
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()