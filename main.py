import pygame as pg
import random

pg.init()
screen_width, screen_height = 800, 600
FPS = 24  # frame per second
clock = pg.time.Clock()
# изображения
bg_img = pg.image.load('src/background.png')
icon_img = pg.image.load('src/ufo.png')
display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическое вторжение')
sys_font = pg.font.SysFont('arial', 34)
font = pg.font.Font('src/04B_19.TTF', 48)
# display.fill('blue', (0, 0, screen_width, screen_height))
display.blit(bg_img, (0, 0))  # image.tr
text_img = sys_font.render('Score 123', True, 'white')
# display.blit(text_img, (100, 50))
game_over_text = font.render('Game Over', True, 'red')
w, h = game_over_text.get_size()
# display.blit(game_over_text, (screen_width/2 - w/2, screen_height / 2 - h/2))
# игрок
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()
player_gap = 10
player_velocity = 10
player_dx = 0
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height - player_gap
# пуля
bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -5
bullet_x = player_x + player_width // 2 - bullet_width // 2  # микро дз - пускать из середины
bullet_y = player_y - bullet_height
bullet_alive = False  # есть пуля?
bullet_velocity = 5
# прoтивник

enemy_img = pg.image.load('src/enemy.png')
enemy_width, enemy_height = enemy_img.get_size()
enemy_dx = 0
enemy_dy = 1
enemy_x = 0  # микро дз - пускать из середины
enemy_y = 0
counter_enemy = 0
score = 0
missed_shots = 0


def enemy_create():
    global enemy_x, enemy_y
    enemy_x = random.randint(0, screen_width - enemy_width)  # screen_width/2-enemy_width/2
    enemy_y = 0
    print(f'CREATE: {enemy_x}')


def model_update():
    palayer_model()
    bullet_model()
    enemy_model()


def palayer_model():
    global player_x
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width


def bullet_model():
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    # пуля улетела за верх экрана
    if bullet_y < 0:
        bullet_alive = False


def bullet_create():
    global bullet_x, bullet_y, bullet_alive
    bullet_alive = True
    bullet_x = player_x + player_width / 2 - bullet_width / 2  # Здесь мы изменяем x-координату пули так, чтобы она вылетала из середины игрока.
    bullet_y = player_y - bullet_height

# Функция bullet_update, которая обновляет положение пули.
def bullet_update():
    global bullet_x, bullet_y, bullet_alive, player_x, player_width, bullet_width
    if bullet_alive:  # Если пуля активна
        bullet_x = player_x + player_width // 2 - bullet_width // 2 # Обновляем x-координату пули, чтобы соответствовать x-координате игрока.
        bullet_y -= bullet_velocity  # Пуля продолжает движение вверх.
        if bullet_y < 0:  # Если пуля достигает верхней части экрана
            bullet_y = player_y - bullet_height  # Сбрасываем положение пули
            bullet_alive = False  # Пуля становится неактивной


def game_over_screen():
    display.blit(game_over_text, (screen_width / 2 - w / 2, screen_height / 2 - h / 2))
    pg.display.update()
    pg.time.wait(2000)  # Ожидание 2 секунды перед закрытием


def victory_screen():
    victory_text = font.render('You Win!', True, 'green')
    w, h = victory_text.get_size()
    display.blit(victory_text, (screen_width / 2 - w / 2, screen_height / 2 - h / 2))
    pg.display.update()
    pg.time.wait(2000)  # Ожидание 2 секунды перед закрытием


def defeat_screen():
    defeat_text = font.render('defeat', True, 'Red')
    w, h = defeat_text.get_size()
    display.blit(defeat_text, (screen_width / 2 - w / 2, screen_height / 2 - h / 2))
    pg.display.update()
    pg.time.wait(2000)  # Ожидание 2 секунды перед закрытием


def enemy_model():
    global enemy_x, enemy_y, bullet_alive, counter_enemy, missed_shots, score
    global enemy_dx, enemy_dy, screen_width, enemy_width
    enemy_x += enemy_dx
    enemy_y += enemy_dy

    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        if is_crossed:
            bullet_alive = False
            score += 1
            counter_enemy += 1
            print("BANG!")
            enemy_create()
            if counter_enemy >= 5:
                victory_screen()
                return False
        # промах
        elif enemy_y + enemy_height > screen_height:
            missed_shots += 1
            print("Missed!")
            enemy_create()
            if missed_shots >= 1:
                defeat_screen()
                return False
    return True


def display_redraw():
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    display.blit(enemy_img, (enemy_x, enemy_y))
    text = font.render(f"Score: {counter_enemy}", True, 'white')  # добавляем счетчик в левый верхний угол
    display.blit(text, (10, 10))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    pg.display.update()


def event_processing():
    global player_x, player_dx
    running = True
    for event in pg.event.get():
        # нажали крестик на окне
        if event.type == pg.QUIT:
            running = False
        # тут нажимаем на клавиши
        if event.type == pg.KEYDOWN:
            # нажали на q - quit
            if event.key == pg.K_q:
                running = False
            if event.type == pg.KEYDOWN:
                # нажали на q - quit
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_SPACE:  # Стрельба по пробелу
                    if not bullet_alive:
                        bullet_create()  # Здесь исправление

        # Движение игрока с помощью мыши
        if event.type == pg.MOUSEMOTION:
            player_x, _ = pg.mouse.get_pos()
            player_x -= player_width / 2  # Центровка корабля относительно курсора мыши

        # Ограничение движения игрока в пределах экрана
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_width:
            player_x = screen_width - player_width

        if counter_enemy >= 10:
            running = False

    clock.tick(FPS)
    return running


# random.seed(77)
missed_shots = 0
enemy_create()
running = True
while running:
    bullet_update()
    model_update()
    display_redraw()
    running = event_processing()
    if not running:
        break
    running = enemy_model()
pg.quit()
