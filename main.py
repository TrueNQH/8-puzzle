from puzzle import Puzzle
import pygame
import pygame_gui
import time
import colors

# Đặt kích thước màn hình là 1280x720 pixel
SCREEN_SIZE = (1280, 720)

# Khởi tạo Pygame
pygame.init()

# Đặt font chữ cơ bản cho game
BASICFONT = pygame.font.Font('FiraCode-Retina.ttf', 50)

# Thiết lập cửa sổ Pygame
pygame.display.set_caption('8 Puzzle')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(colors.BABY_BLUE))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')

# Đặt biểu tượng cho chương trình
programIcon = pygame.image.load('logo.png')
pygame.display.set_icon(programIcon)

# Đặt tiêu đề của cửa sổ
pygame_gui.core.IWindowInterface.set_display_title(self=window_surface, new_title="8-Puzzle")

# Hàm để hiển thị các phần tử trên cửa sổ
def display_elements():
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8-Puzzle Game",
                                        relative_rect=pygame.Rect((540, 10), (300, 70)),
                                        object_id="#title_box"
                                        )

# Gọi hàm display_elements
display_elements()

# Tạo nút để giải puzzle
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 640), (250, 45)),
                                             text='Solve Puzzle',
                                             manager=manager,
                                             object_id="#solve_btn")

# Tạo dropdown menu để chọn thuật toán
dropdown_layout_rect = pygame.Rect((970, 600), (280, 35))
algorithmOptions = ["A*", "Best-First"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

# Nhãn cho dropdown menu
pygame_gui.elements.ui_label.UILabel(parent_element=algorithmDropDown,
                                     manager=manager,
                                     text="Search:",
                                     relative_rect=pygame.Rect((800, 600), (170, 30)))

# Tạo nút để trộn các khối của puzzle
button_layout_rect = pygame.Rect((1000, 290), (250, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                               text='Shuffle',
                                               manager=manager)

# Nhãn để hiển thị cảnh báo hoặc thông báo
alert_label = pygame_gui.elements.ui_label.UILabel(
                                     manager=manager,
                                     text="",
                                     relative_rect=pygame.Rect((920, 320), (250, 30)),
                                     object_id="#accept_label")

# Hàm để vẽ các khối của puzzle lên cửa sổ
def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, colors.BLUE_GROTTO, block['rect'])
            textSurf = BASICFONT.render(str(block['block']), True, colors.NAVY_BLUE)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left + 50, block['rect'].top + 50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, colors.ROYAL_BLUE, block['rect'])


def printMatrix(matrix):
    for row in matrix:
        print(row)
    print("\n")
# Hàm để thực hiện hiệu ứng giải puzzle
def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matrix.searchBlock(0)
        if mv == "right":
            puzzle.matrix.moveright(zero)
        elif mv == "left":
            puzzle.matrix.moveleft(zero)  
        elif mv == "up":
            puzzle.matrix.moveup(zero)
        elif mv == "down":
            puzzle.matrix.movedown(zero)

         
        # In ra ma trận sau mỗi bước
        printMatrix(puzzle.matrix.getMatrix())
        puzzle.setBlocksMatrix()
        draw_blocks(puzzle.blocks)
        pygame.display.update()
        time.sleep(0.2)

# Đặt hình nền cho cửa sổ Pygame
window_surface.blit(background, (0, 0))
pygame.display.update()

# Khởi tạo đồng hồ để đo thời gian
clock = pygame.time.Clock()

# Tạo puzzle mới và khởi tạo
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.initialize()

# Đặt thuật toán mặc định
algorithm = "Best-First"
fstate = "1,2,3,4,5,6,7,8,0"
is_running = True

# Vòng lặp chính của game
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        # Kiểm tra các sự kiện người dùng
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    # Trộn các khối của puzzle
                    puzzle.randomBlocks()
                elif event.ui_element == solve_button:
                    # Giải puzzle dựa trên thuật toán đã chọn
                    if algorithm == "Best-First":
                        # Thuật toán Best-First
                        moves = puzzle.bestFirst()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        # Hiển thị báo cáo về việc giải puzzle
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                       
                        # Tạo hộp thoại xác nhận để hiển thị báo cáo
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        # Thực hiện hiệu ứng giải puzzle
                        solveAnimation(moves)
                        
                    elif algorithm == "A*":
                        # Thuật toán A*
                        moves = puzzle.a_star()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        # Hiển thị báo cáo về việc giải puzzle
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                       
                        # Tạo hộp thoại xác nhận để hiển thị báo cáo
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        # Thực hiện hiệu ứng giải puzzle
                        solveAnimation(moves)
                        
            # Kiểm tra sự kiện thay đổi dropdown menu
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
            # Kiểm tra sự kiện thay đổi ô nhập
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                print("")
        # Xử lý các sự kiện trong game
        manager.process_events(event)
    
    # Cập nhật giao diện người dùng
    manager.update(time_delta)
    
    # Vẽ lại cửa sổ với hình nền
    window_surface.blit(background, (0, 0))
    
    # Vẽ giao diện người dùng lên cửa sổ
    manager.draw_ui(window_surface)
    
    # Vẽ các khối của puzzle lên cửa sổ
    draw_blocks(puzzle.blocks)
    
    # Cập nhật cửa sổ Pygame
    pygame.display.update()
