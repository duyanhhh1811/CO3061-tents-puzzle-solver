import pygame
import copy

from testcase import testcase
from search import *

from UIsetting import *
from handle import *
from sprite import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        # For path point accessing
        self.idx = -1
        # For next_state_function
        self.state_idx = 0

    def handle_matrix(self, matrix: list, row: list, col: list):
        new_matrix = copy.deepcopy(matrix)
        cnt = 0
        for line in new_matrix:
            line.append(row[cnt])
            cnt += 1
        new_matrix.append(col)
        return new_matrix

    def create_next_state(self, flag = False):
        if flag == False: self.state_idx += 1
        if self.state_idx > 10: self.state_idx = 1
        
        # print(f"Now is tc {self.i}")
        for testcase_number, testcase_info in testcase[str(GAMESIZE)].items():
            if testcase_number == str(self.state_idx):
                row_ = testcase_info["row"]
                col_ = testcase_info["col"]
                matrix_ = self.handle_matrix(testcase_info["matrix"], row_, col_)
                if flag == False: return matrix_
                else: return row_, col_, copy.deepcopy(testcase_info["matrix"])

    def draw_title(self):
        self.title = []
        for row, x in enumerate(self.title_grid):
            self.title.append([])
            for col, title in enumerate(x):
                if row == len(self.title_grid) - 1 or col == len(x) - 1:
                    self.title[row].append(Title(self, col, row, title))
                else: self.title[row].append(Title(self, col, row, str(title)))
        
    def update_grid(self, path, index, flag):
        if index >= len(path):
            self.idx = -1
            self.text_list.append(UIElement(770, 550, "Execute Time: " + str(round(self.exe_time,4)) + " s"))
            self.text_list.append(UIElement(738, 600, "Total Generated States: " + str(self.total_states)))
            self.text_list.append(UIElement(716, 650, "Total Allocated Memory: " + str(self.total_mem) + " KiB"))
            self.text_list.append(UIElement(700, 700, "Click this Quit below Button to exit"))
            quit_button = Button(675, 750, 175, 50, "Quit", F3D0D4, F2A7AC)
            cont_button = Button(875, 750, 175, 50, "Continue", F3D0D4, F2A7AC)
            self.buttons_list.append(cont_button)
            self.buttons_list.append(quit_button)
            self.avoid_prev_state = True
        else:
            x = path[index][0]
            y = path[index][1]
            if flag == True: self.title_grid[x][y] = 2
            else: self.title_grid[x][y] = 0
    
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.title_grid = self.create_next_state()
        self.draw_title()
        self.buttons_list = []
        self.text_list = []
        
        self.text_list.append(UIElement(250, 650, "", F291A3))
        self.text_list.append(UIElement(250, 680, "", F291A3))
        
        self.text_list[0].set_text_for_testcase(self.state_idx)
        if self.state_idx >= 1 and self.state_idx <= 5:
            self.text_list[1].set_text_for_level("Easy")
        else: self.text_list[1].set_text_for_level("Hard")
        
        if GAMESIZE == 6:
            self.buttons_list.append(Button(725,100,300,60,"Next Testcase",F3D0D4,F2A7AC))
            self.buttons_list.append(Button(725,250,300,60,"AI Solver",F3D0D4,F2A7AC))
        elif GAMESIZE == 8:
            self.buttons_list.append(Button(700,100,300,60,"Next Testcase",F3D0D4,F2A7AC))
            self.buttons_list.append(Button(700,170,300,60,"AI Solver",F3D0D4,F2A7AC))

        self.avoid_prev_state = True
        
    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            # pygame.display.update()
    
    def update(self):
        self.all_sprites.update()
    
    def draw_grid(self):
        for row in range(-1, GAMESIZE * TITLESIZE, TITLESIZE):
            pygame.draw.line(self.screen, F3E9EA, (row, 0), (row, GAMESIZE * TITLESIZE), 4)
        for col in range(-1, GAMESIZE * TITLESIZE, TITLESIZE):
            pygame.draw.line(self.screen, F3E9EA, (0, col), (GAMESIZE * TITLESIZE, col), 4)
                
    def draw(self):
        self.screen.fill(F3E9EA)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        
        for text in self.text_list:
            text.draw(self.screen)
        
        pygame.display.flip()
    
    def events(self):
        for event in pygame.event.get():
            # event = pygame.event.wait()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Next Testcase":
                            self.title_grid = self.create_next_state()
                            self.draw_title()
                            
                            self.text_list[0].set_text_for_testcase(str(self.state_idx))
                            if self.state_idx >= 1 and self.state_idx <= 5:
                                self.text_list[1].set_text_for_level("Easy")
                            else: self.text_list[1].set_text_for_level("Hard")
                            
                        elif button.text == "AI Solver":
                            self.row, self.col, self.title_grid = self.create_next_state(True)
                            
                            BFS_button = Button(900, 350, 175, 50, "BFS", F3D0D4, F2A7AC)
                            A_Star_button = Button(650, 350, 175, 50, "A*", F3D0D4, F2A7AC)
                            self.buttons_list.append(BFS_button)
                            self.buttons_list.append(A_Star_button)
                            
                        elif button.text == "BFS":
                            s = Search(State(GAMESIZE, self.title_grid, self.row, self.col))
                            goal_state, self.exe_time, self.total_states, self.total_mem = s.BFS()
                            self.point_path = get_point_path(GAMESIZE, get_matrix_path(goal_state))
                            #print(f"BFS path: {self.point_path}")
                            next_state_button = Button(900, 450, 175, 50, "Next State", F3D0D4, F2A7AC)
                            prev_state_button = Button(650, 450, 175, 50, "Prev State", F3D0D4, F2A7AC)
                            self.buttons_list.append(next_state_button)
                            self.buttons_list.append(prev_state_button)
                            self.title_grid = self.handle_matrix(self.title_grid, self.row, self.col)
                        elif button.text == "A*":
                            s = Search(State(GAMESIZE, self.title_grid, self.row, self.col))
                            goal_state, self.exe_time, self.total_states, self.total_mem = s.A_Star()
                            self.point_path = get_point_path(GAMESIZE, get_matrix_path(goal_state))
                            #print(f"A* Path: {self.point_path}")
                            next_state_button = Button(900, 450, 175, 50, "Next State", F3D0D4, F2A7AC)
                            prev_state_button = Button(650, 450, 175, 50, "Prev State", F3D0D4, F2A7AC)
                            self.buttons_list.append(next_state_button)
                            self.buttons_list.append(prev_state_button)
                            self.title_grid = self.handle_matrix(self.title_grid, self.row, self.col)
                        elif button.text == "Next State":
                            self.avoid_prev_state = False
                            if self.idx < len(self.point_path):
                                self.idx += 1
                                #print(f"Put tent successfully at {self.idx}: {self.point_path[self.idx]}")
                                self.update_grid(self.point_path, self.idx, True)
                                self.draw_title()
                            # else: 
                                # self.idx = -1
                                # self.update_grid(self.point_path, self.idx, True)
                                # self.draw_title()
                        elif button.text == "Prev State":
                            if self.avoid_prev_state == False:
                                if self.idx >= 0:
                                # print(f"Delete tent at {self.idx}: {self.point_path[self.idx]}")
                                    self.update_grid(self.point_path, self.idx, False)
                                    self.draw_title()
                                    self.idx -= 1
                                    #print(f"After delete tent, index = {self.idx}")
                        elif button.text == "Quit":
                            pygame.quit
                            quit(0)
                        elif button.text == "Continue":
                            self.new()

def main():
    game = Game()
    while True:
        game.new()
        game.run()
    
if __name__ == "__main__": main()







