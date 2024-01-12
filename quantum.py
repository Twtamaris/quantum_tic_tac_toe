from termcolor import colored, cprint
import json
from qiskit import *
import qiskit
from qiskit.tools.monitor import job_monitor

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 5
GRID_SIZE = 3

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3x3 Grid")

def draw_grid():
    # Draw vertical lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)
    
    # Draw horizontal lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)

def board_coordinates():
    return [[0,0,0] for i in range(3)]


def quanutum_game(circuit,recent_moves):
    """This will return the circuit and draw the circuit diagram"""
    first_move = recent_moves[0]
    second_move = recent_moves[1]
    # hamard gate
    circuit.h(first_move[0]*3 + first_move[1])

    # x gate
    circuit.x(second_move[0]*3 + second_move[1])

    # cnot gate
    circuit.cx(first_move[0]*3 + first_move[1], second_move[0]*3 + second_move[1])


    print(circuit.draw())
    recent_moves.clear()

    return circuit, recent_moves

    # initialize the hadamard gate hehahah
    # circuit.h()
    # ...

def collapse(circuit, is_collapse, quantum_moves, x_turn, recent_moves):
    is_collapse = True
    quantum_moves = False
    if recent_moves:
        circuit.x(recent_moves[0][0]*3 + recent_moves[0][1])
    x_turn = False
    recent_moves.clear()
    circuit.measure([0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8])
    print(circuit.draw())
    simulator = qiskit.Aer.get_backend('qasm_simulator')
    job = qiskit.execute(circuit, simulator, shots=1)
    result = job.result()
    out = json.dumps(result.get_counts())
    string = out[2:11] 

    # reverse the string
    string = string[::-1]
    print(string)

    # reset the circuit
    for i in range(9):  
        circuit.reset(i)

    for i,val in enumerate(string):
        if val == '0':
            print("This is i", i)
            board_coordinate[i//3][i%3] = 0

    

    return is_collapse, quantum_moves, x_turn


def draw_x_or_y(board_coordinates, is_collapse):
    font = pygame.font.Font('freesansbold.ttf', 60)
    colors_x = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    colors_y = [(255, 0, 255), (255, 255, 0),(0, 255, 255)]
    count_x = 0
    count_o = 0
    dict_x = {}
    for row in range(3):
        for col in range(3):
            if board_coordinates[row][col] == 1:
                if is_collapse:
                    text = font.render("X", True, (255,0,0))


                else:
                    # Most hard logic, 4 ghanta lagyo.😂😂
                    color_index = count_x // 2 % len(colors_x)
                    dict_x[color_index] = [row, col]
                    text = font.render("X", True, colors_x[color_index])
                    count_x += 1
                    
                text_rect = text.get_rect(center=(col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2))
                screen.blit(text, text_rect)
                
                
            elif board_coordinates[row][col] == -1:
                if is_collapse:
                    text = font.render("O", True, (0,0,255))
                else:
                    color_index = count_o // 2 % len(colors_y)
                    text = font.render("O", True, colors_y[color_index])
                    count_o += 1
                text_rect = text.get_rect(center=(col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2))
                screen.blit(text, text_rect)




def check_winner(board_coordinates):
    # Check rows
    for row in range(3):
        if board_coordinates[row][0] == board_coordinates[row][1] == board_coordinates[row][2] != 0:
            return board_coordinates[row][0]

    # Check columns
    for col in range(3):
        if board_coordinates[0][col] == board_coordinates[1][col] == board_coordinates[2][col] != 0:
            return board_coordinates[0][col]

    # Check diagonals
    if board_coordinates[0][0] == board_coordinates[1][1] == board_coordinates[2][2] != 0:
        return board_coordinates[0][0]
    if board_coordinates[0][2] == board_coordinates[1][1] == board_coordinates[2][0] != 0:
        return board_coordinates[0][2]

    return 0

def before_collapse(board_coordinates, rows, cols, quantum_moves, x_turn, count):
    """It will decide x_turn for the quantum moves or the normal moves"""
    count += 1
    print(count)
    if x_turn:
        board_coordinates[rows][cols] = 1
        if quantum_moves and count == 2:
            x_turn = False
            count = 0
        elif not quantum_moves:
            x_turn = False
        
        
    else:       
        board_coordinates[rows][cols] = -1
        if quantum_moves and count == 2:
            x_turn = True
            count = 0
        elif not quantum_moves:
            x_turn = True

    return x_turn, count, board_coordinates


def check_complete_fill(board_coordinates):
    print("This is board_coordinates", board_coordinates)
    for row in range(3):
        for col in range(3):
            if board_coordinates[row][col] == 0:
                return False
    return True



board_coordinate = board_coordinates()

circuit = qiskit.QuantumCircuit(9,9)

recent_moves = []

# Main loop
running = True
x_turn = True
count = 0
is_collapse = False
quantum_moves = True

while running:
    for event in pygame.event.get():

        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cols = mouse_x // (WIDTH // GRID_SIZE)
            rows = mouse_y // (HEIGHT // GRID_SIZE)
            recent_moves.append([rows, cols])
            
            


            if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
            #     if x_turn:
            #         board_coordinates[rows][cols] = 1
            #         x_turn = False
            #     else:
            #         board_coordinates[rows][cols] = -1
            #         x_turn = True

                        # if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                x_turn, count,board_coordinate = before_collapse(board_coordinate, rows, cols, quantum_moves, x_turn, count)

                if len(recent_moves) == 2:
                    circuit, recent_moves = quanutum_game(circuit, recent_moves)


            
                if check_complete_fill(board_coordinate):
                    if not is_collapse:
                        is_collapse, quantum_moves, x_turn= collapse(circuit, is_collapse, quantum_moves, x_turn, recent_moves)

                    


                if is_collapse:
                    print("This is is_collapse", is_collapse)
                    winner=check_winner(board_coordinate)
                    if winner == 1:
                        print("X wins!")
                        cprint("X wins!", 'red')
                        # running = False
                    elif winner == -1:
                        print("O wins!")
                        cprint("O wins!", 'blue')
                    
                    elif  check_complete_fill(board_coordinate):
                        print("This is a Draw!")

                print("BOARD COORDINATES", board_coordinate)
                
                # for i, instruction in enumerate(circuit.data):
                #     if hasattr(instruction, 'operation') and hasattr(instruction.operation, 'name') and instruction.operation.name == 'cx':
                #         qubits_connected = instruction.qubits
                #         control_index = qubits_connected[0].index
                #         target_index = qubits_connected[1].index
                        


    # Clear the screen
    screen.fill((0, 0, 0))
    draw_grid()


        # running = False

    # for i, instruction in enumerate(circuit.data):
    #     if hasattr(instruction, 'operation') and hasattr(instruction.operation, 'name') and instruction.operation.name == 'cx':
    #         qubits_connected = instruction.qubits
    #         control_index = qubits_connected[0].index
    #         target_index = qubits_connected[1].index
    #         print(f"CNOT {control_index} -> {target_index}")
            
    
    # quanutum_game(board_coordinates, circuit, x_turn)
    draw_x_or_y(board_coordinate, is_collapse)

        




    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
