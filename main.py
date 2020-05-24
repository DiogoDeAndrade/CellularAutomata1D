import pygame
import random

def ConvertDecimalToBase(base10_number, n_base, trailing_zeros):
    n = base10_number
    ret = []
    
    while (n > 0):
        ret.append(int(n % n_base))
        n //= n_base
    
    zeros_to_add = trailing_zeros - len(ret)
    
    for _ in range(zeros_to_add):
        ret.append(0)

    return ret[::-1]

def ConvertBaseToDecimal(baseN_number, n_base):
    ret = 0

    for v in baseN_number:
        ret = ret * n_base + v

    return ret

def BuildBaseRuleset(n_states, n_neighbours):
    e = (n_neighbours * 2 + 1)
    ret = dict()
    max_value = (n_states ** e)
    for i in range(max_value):
        ret[i] = 0

    return ret

def BuildRuleset(rule_number, n_states, n_neighbours):
    ret = BuildBaseRuleset(n_states, n_neighbours)

    rule_decomposed = ConvertDecimalToBase(rule_number, n_states, n_states ** (n_neighbours * 2 + 1))
    
    m = len(rule_decomposed)

    for i, val in enumerate(rule_decomposed):
        v = m - i - 1

        ret[v] = val

    return ret

def GetNextState(current_state, rules, n_states, n_neighbours):
    ret = current_state[:]

    n = len(current_state)

    for i in range(n):
        neighbourhood = []
        for dx in range(-n_neighbours, n_neighbours + 1):
            t = i + dx
            if (t < 0):
                neighbourhood.append(current_state[t])
            else:
                neighbourhood.append(current_state[t % n])

        v = ConvertBaseToDecimal(neighbourhood, n_states)

        ret[i] = rules[v]

    return ret

def CreateRandomState(n_states, n_cells):
    ret = []

    for _ in range(n_cells):
        ret.append(random.randrange(0, n_states))

    return ret

n_states = 2
n_cells = 31
n_neighbours = 1
n_iter = 15

max_rules = n_states ** (n_states ** (n_neighbours * 2 + 1))
rule = 30
#rule = random.randrange(0, max_rules)

ruleset = BuildRuleset(rule, n_states, n_neighbours)

initial_state = 1 << (n_cells // 2)
current_state = ConvertDecimalToBase(initial_state, n_states, n_cells)
#current_state = CreateRandomState(n_states, n_cells)

# Initialize pygame
res = (1280, 720)
margin = (20, 20)

pygame.init()

# Define the size/resolution of our window
# Create a window and a display surface
screen = pygame.display.set_mode(res)
screen.fill((0,0,20))

sx = (res[0] - margin[0] * 2) / n_cells
sy = (res[1] - margin[1] * 2) / (n_iter + 1)

if (n_states == 2):
    palette = [
        (25, 0, 0),
        (255, 255, 0)
    ]
else:
    palette = [
        (0, 0, 0),
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (128, 255, 0),
        (0, 255, 0),
        (0, 255, 128),
        (0, 255, 255),
        (0, 128, 255),
        (0, 0, 255),
        (128, 0, 255),
        (255, 0, 255),
        (255, 0, 128),
        (255, 128, 128),
        (128, 128, 128),
        (255, 255, 255)
    ]

for i in range(n_iter + 1):
    #print(current_state)

    # Create cells
    for j, v in enumerate(current_state):
        color = palette[v]
        rect = (margin[0] + j * sx + 1, margin[0] + i * sy + 1, sx - 2, sy - 2)
        pygame.draw.rect(screen, color, rect)

    current_state = GetNextState(current_state, ruleset, n_states, n_neighbours)

pygame.display.flip()

while (True):
    # Process OS events
    for event in pygame.event.get():
        # Checks if the user closed the window
        if (event.type == pygame.QUIT):
            # Exits the application immediately
            exit()
        elif (event.type == pygame.KEYDOWN):
            # Exits the application immediately
            exit()
