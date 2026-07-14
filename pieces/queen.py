from pieces.piece import Piece

class Queen(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'q' para pretas, 'Q' para brancas
        symbol = 'q' if color == 'black' else 'Q'
        super().__init__(color, 'Queen', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento da Rainha é geometricamente correto.
        A Rainha combina os movimentos da Torre (retas) e do Bispo (diagonais).
        """
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. Calcula as variações de linha e coluna
        delta_row = abs(new_row - curr_row)
        delta_col = abs(new_col - curr_col)

        # 3. Verifica se o movimento é válido (reto OU diagonal)
        is_straight = (curr_row == new_row) or (curr_col == new_col)
        is_diagonal = (delta_row == delta_col)

        if not (is_straight or is_diagonal):
            return False

        # 4. SRP (Responsabilidade Única): A Rainha sabe a "matemática" do seu movimento, 
        # mas ela delega ao Tabuleiro (board) a verificação de bloqueios no caminho,
        # pois a Rainha não pode "pular" outras peças.
        if board.is_path_blocked(self.position, new_position):
            return False

        # 5. Verifica se a casa de destino está ocupada por uma peça aliada
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True