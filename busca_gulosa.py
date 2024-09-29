from collections import deque
import time
import copy
import tracemalloc
import numpy as np

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def is_board_valid(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0
                if not is_valid(board, row, col, num):
                    return False
                board[row][col] = num
    return True

def find_empty(board):
    zeros = 28
    linha = 0
    coluna = 0
    for i in range(9):
        for j in range(9):
            zeros_value = 28
            if board[i][j] == 0:
                zeros_value = 0
                for k in range(9):
                    if board[k][j] == 0:
                        zeros_value += 1
                for k in range(9):
                    if board[i][k] == 0:
                        zeros_value += 1
                start_row, start_col = 3 * (i // 3), 3 * (j // 3)
                for k in range(3):
                    for l in range(3):
                        if board[start_row + k][start_col + l] == 0:
                            zeros_value += 1
            if zeros_value < zeros:
                zeros = zeros_value
                linha = i
                coluna = j
    if zeros < 28:
        return linha, coluna
    return None

def greedy_sudoku_solver(board):
    queue = deque([board])
    while queue:
        current_board = queue.popleft()

        empty_pos = find_empty(current_board)
        if not empty_pos:
            return current_board

        row, col = empty_pos
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = copy.deepcopy(current_board)
                new_board[row][col] = num
                queue.append(new_board)

    return None

def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(num) if num != 0 else "."
            row_str += " "
        print(row_str)

# Lista de 50 tabuleiros de Sudoku (simplificada para exemplo, todos iguais)
sudoku_boards = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
] * 50

times = []
memories = []

for sudoku_board in sudoku_boards:
    tracemalloc.start()
    start_time = time.time()

    if is_board_valid(sudoku_board):
        solution = greedy_sudoku_solver(sudoku_board)

    end_time = time.time()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    times.append(execution_time)
    memories.append(peak_memory / 1024)  # Convertendo para KB

# Calculando estatísticas
mean_time = np.mean(times)
std_time = np.std(times)
mean_memory = np.mean(memories)
std_memory = np.std(memories)

print(f"Média de tempo: {mean_time:.4f} segundos")
print(f"Desvio padrão do tempo: {std_time:.4f} segundos")
print(f"Média de memória: {mean_memory:.2f} KB")
print(f"Desvio padrão da memória: {std_memory:.2f} KB")
