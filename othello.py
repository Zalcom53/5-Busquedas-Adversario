from juegos_simplificado import ModeloJuegoZT2

class Othello(ModeloJuegoZT2):
    def inicializa(self):
        board = [0] * 64
        board[27] = 1  # (3,3)
        board[36] = 1  # (4,4)
        board[28] = -1  # (3,4)
        board[35] = -1  # (4,3)
        return tuple(board), 1

    def jugadas_legales(self, s, j):
        board = list(s)
        placement_moves = []
        for i in range(64):
            if board[i] == 0 and self.is_legal_move(board, i, j):
                placement_moves.append(i)
        return placement_moves if placement_moves else [-1]

    def is_legal_move(self, board, i, j):
        if board[i] != 0:
            return False
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        return any(self.check_direction(board, i, j, dr, dc) for dr, dc in directions)

    def check_direction(self, board, i, j, dr, dc):
        row, col = divmod(i, 8)
        opponent = -j
        row += dr
        col += dc
        found_opponent = False
        while 0 <= row < 8 and 0 <= col < 8:
            pos = row * 8 + col
            if board[pos] == 0:
                break
            if board[pos] == j:
                return found_opponent
            if board[pos] == opponent:
                found_opponent = True
            row += dr
            col += dc
        return False

    def transicion(self, s, a, j):
        if a == -1:
            return s
        board = list(s)
        self.place_disk(board, a, j)
        return tuple(board)

    def place_disk(self, board, i, j):
        board[i] = j
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in directions:
            self.flip_direction(board, i, j, dr, dc)

    def flip_direction(self, board, i, j, dr, dc):
        row, col = divmod(i, 8)
        opponent = -j
        flips = []
        row += dr
        col += dc
        while 0 <= row < 8 and 0 <= col < 8 and board[row*8 + col] == opponent:
            flips.append((row, col))
            row += dr
            col += dc
        if 0 <= row < 8 and 0 <= col < 8 and board[row*8 + col] == j:
            for r, c in flips:
                board[r*8 + c] = j

    def terminal(self, s):
        has_moves1 = any(a != -1 for a in self.jugadas_legales(s, 1))
        has_moves2 = any(a != -1 for a in self.jugadas_legales(s, -1))
        return not (has_moves1 or has_moves2)

    def ganancia(self, s):
        return s.count(1) - s.count(-1)

def ordena_othello(jugadas, jugador, s):
    def clave(a):
        if a == -1:
            return 0
        tablero_temp = list(s)
        juego = Othello()
        juego.place_disk(tablero_temp, a, jugador)
        volteados = sum(1 for i, x in enumerate(tablero_temp) if x == jugador and s[i] != jugador)
        return volteados
    return sorted(jugadas, key=clave, reverse=True)

def make_ordena_othello(s):
    def ordena(jugadas, jugador):
        return ordena_othello(jugadas, jugador, s)
    return ordena

def evalua_othello(s):
    count1 = s.count(1)
    count2 = s.count(-1)
    juego = Othello()
    mobility1 = len([a for a in juego.jugadas_legales(s, 1) if a != -1])
    mobility2 = len([a for a in juego.jugadas_legales(s, -1) if a != -1])
    return (count1 - count2) + 0.1 * (mobility1 - mobility2)

if __name__ == "__main__":
    from juegos_simplificado import juega_dos_jugadores
    from minimax import minimax_iterativo

    def jugador_manual_othello(juego, s, j):
        moves = juego.jugadas_legales(s, j)
        if moves == [-1]:
            print("Sin movimientos, pasando")
            return -1
        print_board(s)
        print("Movimientos legales:", moves)
        while True:
            try:
                a = int(input("Elige un movimiento (índice 0-63): "))
                if a in moves:
                    return a
            except ValueError:
                pass
            print("Movimiento inválido")

    def print_board(s):
        for i in range(8):
            row = [s[i*8 + j] for j in range(8)]
            print([1 if x == 1 else -1 if x == -1 else '.' for x in row])

    juego = Othello()
    jugador_ia = lambda juego, s, j: minimax_iterativo(juego, s, j, tiempo=10, ordena=make_ordena_othello(s), evalua=evalua_othello)
    resultado, estado_final = juega_dos_jugadores(juego, jugador_manual_othello, jugador_ia)
    print("Resultado (ganancia para jugador 1):", resultado)
    print("Tablero final:")
    print_board(estado_final)