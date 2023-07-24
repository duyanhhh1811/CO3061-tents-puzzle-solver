from search import *

def get_input():
    folder = "input"
    size = input("Choose size: ")
    tc = input("Choose testcase: ")

    inp_file = size + "-" + tc + ".txt"
    file_list = os.listdir(folder)
    
    for file in file_list:
        if file == inp_file:
            file_path = os.path.join(folder, file)
            break 
    else:
        print("Không tìm thấy input, xin mời nhập lại!\n")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    inp_matrix = []
    for line in lines:
        value = line.strip().split(' ')
        inp_line = []
        for x in value:
            inp_line.append(int(x)) 
        inp_matrix.append(inp_line)
    return int(size), inp_matrix[:int(size)], inp_matrix[-2], inp_matrix[-1]

def get_matrix_path(state: State):
    matrix_path_list = []
    while state.prev:
        matrix_path_list.insert(0, getSubMatrix(state, state.prev))
        # matrix_path_list.insert(0, state.matrix)
        state = state.prev
    return matrix_path_list

def tent_finding(size: int, matrix: list):
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 2: return (i,j)

def get_point_path(size :int, matrix_path_list: list):
    res = []
    for each_matrix in matrix_path_list:
        res.append(tent_finding(size, each_matrix))
    return res

def main(size: int, matrix: list, row: list, col: list):
    
    choice = int(input())
    s = Search(State(size, matrix, row, col))
    if int(choice) == 1: 
        goal_state = s.BFS()
    elif int(choice) == 2:
        goal_state = s.A_Star()
        print(goal_state.matrix)
        
    point_path = get_point_path(size, get_matrix_path(goal_state))
    return point_path