import os
import pgzrun
import time
from random import choice
import pygame

# 게임 창을 화면 중앙에 배치
os.environ['SDL_VIDEO_CENTERED'] = '1'

# 게임 화면 크기
WIDTH = 800
HEIGHT = 600

# 게임 상태
current_screen = 'menu'
selected_mode = None

# 버튼 설정
button_width = 250
button_height = 70
button_margin = 20
home_button_width = 150
home_button_height = 40

# 맵 크기 설정 (Creative 모드)
MAP_WIDTH = 1500
MAP_HEIGHT = 1500
TILE_SIZE = 30

# 지표면 레벨 정의
GROUND_LEVEL_Y = (MAP_HEIGHT // TILE_SIZE) - 7  # 지표면의 y 좌표 인덱스

# 중력 및 캐릭터 이동 관련 변수
GRAVITY = 0.4
JUMP_STRENGTH = -6
MOVE_SPEED = 4
steve_vy = 0  # steve의 수직 속도
on_ground_status = False  # 캐릭터가 땅에 있는지 확인하는 플래그

# 카메라 오프셋
camera_offset_x = 0
camera_offset_y = 0

# 마우스 클릭 상태 변수
last_click_time = 0  # 마지막 클릭 시간을 저장
double_click_interval = 0.5  # 더블 클릭 감지 간격 (초)
clicked_block = None  # 클릭된 블록
last_clicked_block = None  # 마지막으로 클릭한 블록

# 캐릭터
# 초기 이미지를 steve_right_1로 설정 (인벤토리 1)
steve = Actor("steve_right_1", midbottom=(WIDTH // 2, TILE_SIZE * 20))  
steve.pos = WIDTH / 2, 0

# 블록 이미지 정의 (Creative 모드)
grass = Actor("grass")
dirt = Actor("dirt")
bedrock = Actor("bedrock")  # 배드락 블록 추가
bricks = Actor("bricks")
oak_planks = Actor("oak_planks")
cobblestone = Actor("cobblestone")
glass = Actor("glass")
white_wool = Actor("white_wool")
black_concrete = Actor("black_concrete")
red_concrete = Actor("red_concrete")
blue_concrete = Actor("blue_concrete")
yellow_concrete = Actor("yellow_concrete")

# 인벤토리 설정
# 인벤토리에 맞는 블록 타입을 정의
block_types = [
    "bricks",
    "oak_planks",
    "cobblestone",
    "glass",
    "white_wool",
    "black_concrete",
    "red_concrete",
    "blue_concrete",
    "yellow_concrete"
]

# 인벤토리 이미지 파일 이름
inventory_images = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
selected_inventory_index = 0  # 초기 설정은 첫 번째 이미지

# Creative 모드 맵 생성
map_data = []

for y in range(MAP_HEIGHT // TILE_SIZE):
    row = []
    for x in range(MAP_WIDTH // TILE_SIZE):
        # 맨 아래 2칸을 배드락으로 채움
        if y >= (MAP_HEIGHT // TILE_SIZE) - 2:
            row.append(Actor("bedrock", (x * TILE_SIZE, y * TILE_SIZE)))
        # 그 위 4칸을 흙으로 채움
        elif y >= (MAP_HEIGHT // TILE_SIZE) - 6:
            row.append(Actor("dirt", (x * TILE_SIZE, y * TILE_SIZE)))
        # 그 위에 1칸을 잔디로 채움
        elif y == (MAP_HEIGHT // TILE_SIZE) - 7:
            row.append(Actor("grass", (x * TILE_SIZE, y * TILE_SIZE)))
        else:
            row.append(None)  # 그 위는 빈 공간
    map_data.append(row)

def on_start():
    pygame.display.set_caption("2D Minecraft")  # 창 타이틀 설정
    # 배경 음악 재생 (무한 반복)
    music.play('bgm.wav')

# 화면 그리기
def draw():
    global current_screen

    if current_screen == 'menu':
        draw_menu()
    elif current_screen == 'game':
        if selected_mode == 'Creative':
            draw_creative_game()
        else:
            draw_survival_game()

# 메뉴 화면 그리기
def draw_menu():
    screen.fill((50, 50, 50))  # 메뉴 배경색

    # 메뉴 제목을 그립니다
    screen.draw.text("2D Minecraft", center=(WIDTH // 2, HEIGHT // 2 - 200), fontsize=80, color="grey", owidth=0.1, ocolor="red")

    # 버튼을 그립니다
    draw_button("Survival", WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - button_margin, 'Survival')
    draw_button("Creative", WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + button_height + button_margin, 'Creative')

# 버튼 그리기
def draw_button(text, x, y, mode):
    # 버튼 배경
    screen.draw.filled_rect(Rect((x, y), (button_width, button_height)), (150, 150, 150))
    # 버튼 텍스트
    screen.draw.text(text, center=(x + button_width // 2, y + button_height // 2), fontsize=50, color="white")

# 홈 버튼 그리기
def draw_home_button():
    # 'Home' 버튼 배경
    screen.draw.filled_rect(Rect((WIDTH - home_button_width - 10, 10), (home_button_width, home_button_height)), (150, 0, 0))
    # 버튼 텍스트
    screen.draw.text("Home", center=(WIDTH - home_button_width // 2 - 10, 10 + home_button_height // 2), fontsize=25, color="white")

# Survival 모드 게임 화면 그리기
def draw_survival_game():
    screen.fill((0, 0, 0))  # 서바이벌 모드 배경색
    screen.draw.text("Survival Mode Coming Soon", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
    # 'Home' 버튼을 그립니다
    draw_home_button()

# Creative 모드 게임 화면 그리기
def draw_creative_game():
    screen.clear()
    screen.fill((110, 177, 255))

    # 카메라 오프셋을 적용하여 맵 그리기
    for row in map_data:
        for block in row:
            if block:
                block.x -= camera_offset_x
                block.y -= camera_offset_y
                block.draw()
                block.x += camera_offset_x
                block.y += camera_offset_y

    # 캐릭터 그리기 (카메라 오프셋 적용)
    steve.x -= camera_offset_x
    steve.y -= camera_offset_y
    steve.draw()
    steve.x += camera_offset_x
    steve.y += camera_offset_y

    # 인벤토리 그리기 (중앙 바닥에 이미지 표시)
    inventory_image = Actor(inventory_images[selected_inventory_index], midbottom=(WIDTH // 2, HEIGHT))
    inventory_image.draw()

    # 'Home' 버튼을 그립니다
    draw_home_button()

# Helper function to set steve's image based on direction and inventory
def set_steve_image():
    inventory_num = selected_inventory_index + 1
    if steve.image.startswith("steve_right"):
        steve.image = f"steve_right_{inventory_num}"
    elif steve.image.startswith("steve_left"):
        steve.image = f"steve_left_{inventory_num}"
    else:
        # 기본 이미지 설정 (처음 시작 시)
        steve.image = f"steve_right_{inventory_num}"

# 블록 파괴 및 설치를 위한 마우스 클릭 처리
def on_mouse_down(pos, button):
    global current_screen, selected_mode, mouse_pressed, clicked_block, last_click_time, last_clicked_block, selected_inventory_index
    current_time = time.time()

    if current_screen == 'menu':
        # 'Survival' 버튼 클릭 확인
        if (WIDTH // 2 - button_width // 2 <= pos[0] <= WIDTH // 2 + button_width // 2 and
            HEIGHT // 2 - button_height // 2 - button_margin <= pos[1] <= HEIGHT // 2 - button_height // 2 - button_margin + button_height):
            selected_mode = 'Survival'
            current_screen = 'game'
        # 'Creative' 버튼 클릭 확인
        elif (WIDTH // 2 - button_width // 2 <= pos[0] <= WIDTH // 2 + button_width // 2 and
              HEIGHT // 2 - button_height // 2 + button_height + button_margin <= pos[1] <= HEIGHT // 2 - button_height // 2 + button_height + button_margin + button_height):
            selected_mode = 'Creative'
            current_screen = 'game'

    elif current_screen == 'game':
        # 'Home' 버튼 클릭 확인
        if (WIDTH - home_button_width - 10 <= pos[0] <= WIDTH - 10 and
            10 <= pos[1] <= 10 + home_button_height):
            current_screen = 'menu'
        else:
            if selected_mode == 'Creative':
                adjusted_x = pos[0] + camera_offset_x
                adjusted_y = pos[1] + camera_offset_y

                # 블록 파괴: 마우스 왼쪽 클릭
                if button == mouse.LEFT:
                    for row in map_data:
                        for block in row:
                            if block and block.collidepoint((adjusted_x, adjusted_y)):
                                clicked_block = block

                                # 블록이 배드락인지 확인
                                if block.image == "bedrock":
                                    # 배드락은 절대로 파괴할 수 없음
                                    return

                                # 캐릭터와 블록의 맵 좌표 계산
                                steve_x = int(steve.x // TILE_SIZE)
                                steve_y = int(steve.y // TILE_SIZE)
                                block_x = int(block.x // TILE_SIZE)
                                block_y = int(block.y // TILE_SIZE)

                                # 거리 계산 (맨해튼 거리)
                                distance = abs(steve_x - block_x) + abs(steve_y - block_y)

                                # 거리 제한: 5칸 이내만 블록 파괴 가능
                                if distance <= 5:
                                    # 캐릭터와 블록 사이에 다른 블록이 있는지 확인 (라인 오브 사이트)
                                    if clear_line_of_sight(steve_x, steve_y, block_x, block_y):
                                        # 블록의 캐릭터 반대 방향에 블록이 있는지 확인
                                        if not has_block_in_opposite_direction(steve_x, steve_y, block_x, block_y):
                                            # 캐릭터의 위치에서 해당 블록이 있는 방향인지 확인
                                            if is_in_character_direction(steve_x, steve_y, block_x, block_y):
                                                # 더블 클릭 감지 (블록 파괴)
                                                if clicked_block == last_clicked_block and current_time - last_click_time <= double_click_interval:
                                                    # 블록 파괴
                                                    map_data[block_y][block_x] = None
                                                    last_clicked_block = None  # 초기화
                                                    sounds.remove.play()
                                                else:
                                                    # 마지막 클릭 기록 업데이트
                                                    last_click_time = current_time
                                                    last_clicked_block = clicked_block
                                            else:
                                                # 캐릭터가 해당 방향에 없음
                                                last_click_time = 0
                                                last_clicked_block = None
                                        else:
                                            # 블록의 반대편에 다른 블록이 있어서 파괴 불가
                                            last_click_time = 0
                                            last_clicked_block = None
                                    else:
                                        # 사이에 다른 블록이 있어서 파괴 불가
                                        last_click_time = 0
                                        last_clicked_block = None
                                else:
                                    # 거리 제한으로 인해 파괴 불가능
                                    last_click_time = 0
                                    last_clicked_block = None

                                return

                # 블록 설치: 마우스 오른쪽 클릭
                elif button == mouse.RIGHT:
                    install_block_x = int(adjusted_x // TILE_SIZE)
                    install_block_y = int(adjusted_y // TILE_SIZE)

                    # 캐릭터와 설치할 블록 사이의 맨해튼 거리 계산
                    steve_x = int(steve.x // TILE_SIZE)
                    steve_y = int(steve.y // TILE_SIZE)
                    distance = abs(steve_x - install_block_x) + abs(steve_y - install_block_y)

                    if distance <= 5:
                        # 설치할 위치에 블록이 없는지 확인
                        if 0 <= install_block_x < len(map_data[0]) and 0 <= install_block_y < len(map_data):
                            if map_data[install_block_y][install_block_x] is None:
                                # 캐릭터와 설치할 블록 사이에 다른 블록이 있는지 확인
                                if clear_line_of_sight(steve_x, steve_y, install_block_x, install_block_y):
                                    # 캐릭터의 방향과 일치하는지 확인
                                    if is_in_character_direction(steve_x, steve_y, install_block_x, install_block_y):
                                        # 설치할 블록의 반대 방향에 블록이 없어야 함
                                        if not has_block_in_opposite_direction(steve_x, steve_y, install_block_x, install_block_y):
                                            # 현재 선택된 인벤토리에 따른 블록 타입 선택
                                            block_type = block_types[selected_inventory_index]
                                            # 블록 생성 및 맵에 추가
                                            new_block = Actor(block_type, (install_block_x * TILE_SIZE, install_block_y * TILE_SIZE))
                                            map_data[install_block_y][install_block_x] = new_block
                                            sounds.place.play()

# 브레젠험의 선 알고리즘을 사용하여 라인 오브 사이트 확인
def clear_line_of_sight(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    n = 1 + dx + dy
    x_inc = 1 if x1 > x0 else -1 if x1 < x0 else 0
    y_inc = 1 if y1 > y0 else -1 if y1 < y0 else 0
    error = dx - dy
    dx *= 2
    dy *= 2

    for _ in range(n):
        if (x, y) != (x0, y0) and (x, y) != (x1, y1):
            if map_data[y][x] is not None:
                return False  # 사이에 블록이 있음
        if error > 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
    return True  # 사이에 블록이 없음

# 캐릭터의 반대 방향에 블록이 있는지 확인
def has_block_in_opposite_direction(steve_x, steve_y, block_x, block_y):
    dx = block_x - steve_x
    dy = block_y - steve_y

    # 캐릭터와 블록이 같은 위치인 경우
    if dx == 0 and dy == 0:
        return False

    # 반대 방향 좌표 계산
    opposite_x = block_x - dx
    opposite_y = block_y - dy

    # 맵 범위 확인
    if 0 <= opposite_x < len(map_data[0]) and 0 <= opposite_y < len(map_data):
        if map_data[opposite_y][opposite_x] is not None:
            return True  # 반대편에 블록이 있음

    return False  # 반대편에 블록이 없음

# 캐릭터가 블록의 방향에 있는지 확인
def is_in_character_direction(steve_x, steve_y, block_x, block_y):
    dx = block_x - steve_x
    dy = block_y - steve_y

    if abs(dx) > abs(dy):
        # 수평 방향
        if dx > 0 and steve.image.startswith("steve_right"):
            return True
        elif dx < 0 and steve.image.startswith("steve_left"):
            return True
        else:
            return False
    else:
        # 수직 방향
        if dy > 0:
            return True  # 캐릭터 아래쪽 블록
        else:
            return True  # 캐릭터 위쪽 블록

# 캐릭터가 땅에 닿았는지 확인
def on_ground():
    for row in map_data:
        for block in row:
            if block and steve.colliderect(block) and steve.bottom <= block.bottom:
                return True
    return False

# 좌우 충돌 확인
def horizontal_collision():
    for row in map_data:
        for block in row:
            if block and steve.colliderect(block):
                return True
    return False

# 캐릭터 움직임 및 중력 적용
def update():
    global steve_vy, on_ground_status, camera_offset_x, camera_offset_y, mouse_pressed, clicked_block, selected_inventory_index

    if current_screen == 'game' and selected_mode == 'Creative':
        # 중력 적용
        if not on_ground_status:
            steve_vy += GRAVITY

        # 이동 전에 이전 위치 저장
        old_y = steve.y
        steve.y += steve_vy

        # 땅에 닿으면 수직 속도를 0으로 설정하고 캐릭터의 위치 조정
        if on_ground():
            if steve_vy > 0:
                steve_vy = 0
                # 충돌 위치에서 멈추도록 조정
                steve.y = old_y
            on_ground_status = True
            # 점프
            if keyboard.w:
                steve_vy = JUMP_STRENGTH
                on_ground_status = False
        else:
            on_ground_status = False

        # 캐릭터 좌우 이동 및 이미지 전환
        old_x = steve.x
        moved = False
        direction = None
        if keyboard.a:
            steve.x -= MOVE_SPEED
            moved = True
            direction = "left"
        if keyboard.d:
            steve.x += MOVE_SPEED
            moved = True
            direction = "right"

        # 좌우 이동 충돌 감지
        if horizontal_collision():
            steve.x = old_x
        else:
            if moved:
                # Update steve's image based on movement direction and inventory
                inventory_num = selected_inventory_index + 1
                steve.image = f"steve_{direction}_{inventory_num}"

        # 화면 경계 넘어가지 않게 제한
        steve.x = max(0, min(MAP_WIDTH - TILE_SIZE, steve.x))
        steve.y = min(MAP_HEIGHT - TILE_SIZE, steve.y)

        # 카메라 오프셋 계산
        camera_offset_x = steve.x - WIDTH // 2
        camera_offset_y = steve.y - HEIGHT // 2

        # 카메라가 맵 바깥으로 나가지 않도록 제한
        camera_offset_x = max(0, min(camera_offset_x, MAP_WIDTH - WIDTH))
        camera_offset_y = max(0, min(camera_offset_y, MAP_HEIGHT - HEIGHT))

        # 인벤토리 변경 (1~9 숫자 키를 누를 때)
        if keyboard.k_1:
            selected_inventory_index = 0
            set_steve_image()
        elif keyboard.k_2:
            selected_inventory_index = 1
            set_steve_image()
        elif keyboard.k_3:
            selected_inventory_index = 2
            set_steve_image()
        elif keyboard.k_4:
            selected_inventory_index = 3
            set_steve_image()
        elif keyboard.k_5:
            selected_inventory_index = 4
            set_steve_image()
        elif keyboard.k_6:
            selected_inventory_index = 5
            set_steve_image()
        elif keyboard.k_7:
            selected_inventory_index = 6
            set_steve_image()
        elif keyboard.k_8:
            selected_inventory_index = 7
            set_steve_image()
        elif keyboard.k_9:
            selected_inventory_index = 8
            set_steve_image()


on_start()
pgzrun.go()