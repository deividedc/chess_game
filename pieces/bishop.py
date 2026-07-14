from pieces.piece import Piece

class Bishop(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'b' para pretas, 'B' para brancas
        symbol = 'b' if color == 'black' else 'B'
        super().__init__(color, 'Bishop', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Bispo é geometricamente correto.
        O Bispo move-se qualquer quantidade de casas, exclusivamente nas diagonais.
        """
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. Calcula o valor absoluto das variações (distâncias)
        delta_row = abs(new_row - curr_row)
        delta_col = abs(new_col - curr_col)

        # 3. Regra matemática da diagonal: a variação de linha deve ser igual à de coluna
        if delta_row != delta_col:
            return False

        # 4. SRP: Delega ao Tabuleiro a verificação de obstáculos no trajeto.
        # O Bispo não pode saltar sobre outras peças.
        if board.is_path_blocked(self.position, new_position):
            return False

        # 5. Verifica se a casa de destino está ocupada por uma peça da mesma cor
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True