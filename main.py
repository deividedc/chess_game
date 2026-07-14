import sys
from board.board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'  # O jogo sempre começa com as brancas

    def switch_turn(self):
        """Alterna o turno entre 'white' e 'black'."""
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def parse_coordinate(self, command: str) -> tuple:
        """
        Converte uma entrada do terminal como '7,4' ou '7 4' em uma tupla (7, 4).
        Retorna None se o formato for inválido.
        """
        try:
            # Substitui espaços por vírgulas e divide
            parts = command.replace(" ", ",").split(",")
            if len(parts) != 2:
                return None
            row = int(parts[0].strip())
            col = int(parts[1].strip())
            if 0 <= row < 8 and 0 <= col < 8:
                return (row, col)
        except ValueError:
            return None
        return None

    def play(self):
        """Loop principal que roda o jogo de xadrez."""
        print("=========================================")
        print("        BEM-VINDO AO CHESS GAME!        ")
        print("=========================================")
        print("Instruções de movimento:")
        print("Digite as coordenadas no formato: linha,coluna (Ex: 6,4)")
        print("Digite 'sair' a qualquer momento para encerrar.\n")

        while True:
            self.board.print_board()
            print(f"--- TURNO DAS: {self.current_turn.upper()} ---")

            # 1. Seleção da peça de origem
            orig_input = input("Escolha a coordenada da PEÇA que quer mover: ").strip().lower()
            if orig_input == 'sair':
                print("Jogo encerrado. Até a próxima!")
                sys.exit()

            origin = self.parse_coordinate(orig_input)
            if origin is None:
                print("[Erro] Formato inválido! Use o formato 'linha,coluna' (Ex: 6,4). Tente novamente.\n")
                continue

            piece = self.board.get_piece_at(origin)

            # Validações de origem
            if piece is None:
                print("[Erro] Não há nenhuma peça nesta casa! Tente novamente.\n")
                continue
            if piece.color != self.current_turn:
                print(f"[Erro] Essa peça é das {piece.color}s! É a vez das {self.current_turn}s. Tente novamente.\n")
                continue

            # 2. Seleção da casa de destino
            dest_input = input(f"Mover {piece.name} de {origin} para qual coordenada? ").strip().lower()
            if dest_input == 'sair':
                print("Jogo encerrado. Até a próxima!")
                sys.exit()

            destination = self.parse_coordinate(dest_input)
            if destination is None:
                print("[Erro] Formato inválido de destino! Movimento cancelado.\n")
                continue

            # 3. Validação das Regras do Movimento
            # Passamos o tabuleiro para a peça verificar as restrições físicas
            if not piece.is_valid_move(destination, self.board):
                print(f"[Erro] Movimento inválido para o {piece.name}! Tente novamente.\n")
                continue

            # 4. Execução do Movimento (caso seja válido)
            # Verifica se é um caso especial de En Passant
            if piece.name == 'Pawn' and self.board.can_en_passant(origin, destination):
                # Captura o peão adversário na casa En Passant (uma linha atrás do destino)
                direction = -1 if piece.color == 'white' else 1
                captured_pawn_pos = (destination[0] - direction, destination[1])
                self.board.set_piece_at(captured_pawn_pos, None)
                print(f"Captura En Passant realizada!")

            # Verifica se foi um movimento de Roque para mover também a Torre
            if piece.name == 'King' and abs(destination[1] - origin[1]) == 2:
                step = 1 if destination[1] > origin[1] else -1
                rook_origin_col = 7 if step == 1 else 0
                rook_dest_col = destination[1] - step
                
                rook = self.board.get_piece_at((origin[0], rook_origin_col))
                # Move a torre correspondente para o lado do rei
                self.board.set_piece_at((origin[0], rook_dest_col), rook)
                self.board.set_piece_at((origin[0], rook_origin_col), None)
                if rook:
                    rook.moved = True
                print("Roque realizado com sucesso!")

            # Configura o alvo En Passant se for um avanço duplo de peão nesta jogada
            if piece.name == 'Pawn' and abs(destination[0] - origin[0]) == 2:
                # O alvo de captura fica na casa intermediária onde o peão saltou
                direction = -1 if piece.color == 'white' else 1
                self.board.en_passant_target = (origin[0] + direction, origin[1])
            else:
                # Se qualquer outra jogada for feita, o En Passant expira
                self.board.en_passant_target = None

            # Efetua o movimento físico no tabuleiro
            self.board.set_piece_at(destination, piece)
            self.board.set_piece_at(origin, None)
            
            # Marca que a peça já se moveu pelo menos uma vez (essencial para Peão, Rei e Torre)
            piece.moved = True

            # 5. Turno concluído, passa para o próximo jogador
            self.switch_turn()
            print("\n-----------------------------------------")
            print("Movimento realizado com sucesso!")
            print("-----------------------------------------\n")


if __name__ == "__main__":
    game = ChessGame()
    game.play()