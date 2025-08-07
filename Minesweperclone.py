import random

# Config
GRID_SIZE = 8     # 8x8 board
NUM_MINES = 10

# Directions for neighbor check
DIRS = [(-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),         ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)]

# Create grid
def create_board():
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return board

# Place mines randomly
def place_mines(board):
    mine_locations = set()
    while len(mine_locations) < NUM_MINES:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if (row, col) not in mine_locations:
            mine_locations.add((row, col))
            board[row][col] = 'M'
    return mine_locations

# Count neighboring mines
def count_adjacent_mines(board, row, col):
    count = 0
    for dr, dc in DIRS:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if board[r][c] == 'M':
                count += 1
    return count

# Reveal cells recursively
def reveal(board, visible, row, col):
    if visible[row][col] != ' ':
        return
    if board[row][col] == 'M':
        visible[row][col] = 'M'
        return

    count = count_adjacent_mines(board, row, col)
    visible[row][col] = str(count) if count > 0 else ' '

    if count == 0:
        for dr, dc in DIRS:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                reveal(board, visible, r, c)

# Print the visible board
def print_board(board):
    print("\n    " + " ".join(str(i) for i in range(GRID_SIZE)))
    print("   " + "---" * GRID_SIZE)
    for i in range(GRID_SIZE):
        row = " ".join(board[i])
        print(f"{i} | {row}")
    print()

# Main game loop
def play_minesweeper():
    hidden_board = create_board()
    visible_board = create_board()
    mines = place_mines(hidden_board)
    safe_cells = GRID_SIZE * GRID_SIZE - NUM_MINES

    revealed = 0

    while True:
        print_board(visible_board)
        try:
            row = int(input("Enter row (0-7): "))
            col = int(input("Enter col (0-7): "))
        except ValueError:
            print("❗ Invalid input. Use numbers.")
            continue

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            print("❗ Coordinates out of range.")
            continue

        if visible_board[row][col] != ' ':
            print("⛔ Already revealed.")
            continue

        if hidden_board[row][col] == 'M':
            print_board(hidden_board)
            print("💥 You hit a mine! Game Over.")
            break

        reveal(hidden_board, visible_board, row, col)

        # Recalculate revealed count
        revealed = sum(row.count(' ') for row in visible_board)
        if revealed == 0:
            print_board(visible_board)
            print("🎉 Congratulations! You cleared the minefield!")
            break

if __name__ == "__main__":
    play_minesweeper()

