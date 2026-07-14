from pieces.piece import Piece

class King(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'k' para pretas, 'K' para brancas
        symbol = 'k' if color == 'black' else 'K'
        # O Rei começa com moved=False para viabilizar a lógica de Roque (Castling)
        super().__init__(color, 'King', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Rei é geometricamente correto.
        O Rei move-se exatamente uma casa em qualquer direção (horizontal, vertical ou diagonal)
        ou duas casas lateralmente no caso de um Roque válido.
        """
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. Calcula a distância absoluta de movimento
        delta_row = abs(new_row - curr_row)
        delta_col = abs(new_col - curr_col)

        # 3. Caso especial: Movimento de Roque (Castling)
        # No roque, o rei se desloca exatamente duas casas para a esquerda ou direita na mesma fileira.
        if delta_row == 0 and delta_col == 2:
            return self._is_valid_castling(new_position, board)

        # 4. Movimento Padrão: No máximo uma casa em qualquer direção
        if delta_row <= 1 and delta_col <= 1:
            # Verifica se a casa de destino não está ocupada por um aliado
            destination_piece = board.get_piece_at(new_position)
            if destination_piece is not None and destination_piece.color == self.color:
                return False
            
            # SRP: Delega ao Tabuleiro a verificação se a casa de destino está sob ataque.
            # O Rei não pode se colocar em xeque de forma alguma.
            if board.is_square_under_attack(new_position, self.color):
                return False

            return True

        return False

    def _is_valid_castling(self, new_position: tuple, board) -> bool:
        """
        Método auxiliar para validar os requisitos específicos do Roque.
        """
        # Se o rei já se moveu, o roque é estritamente proibido
        if self.moved:
            return False

        # O rei não pode fazer roque se estiver atualmente em xeque
        if board.is_square_under_attack(self.position, self.color):
            return False

        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # Determina a direção (esquerda para o roque grande, direita para o roque pequeno)
        step = 1 if new_col > curr_col else -1
        rook_col = 7 if step == 1 else 0

        # Encontra a torre correspondente
        rook = board.get_piece_at((curr_row, rook_col))
        
        # A peça na ponta precisa existir, ser uma torre, ser da mesma cor e não ter se movido
        if rook is None or rook.name != 'Rook' or rook.color != self.color or rook.moved:
            return False

        # Verifica se o caminho entre o Rei e a Torre está completamente livre
        # E se nenhuma das casas pelas quais o Rei passará está sob ataque (regral do xadrez)
        col_check = curr_col + step
        while col_check != rook_col:
            square = (curr_row, col_check)
            
            # Caminho deve estar vazio
            if board.get_piece_at(square) is not None:
                return False
            
            # O rei não pode passar por nenhuma casa que esteja sob ataque do adversário
            # (Valida apenas as casas de trânsito do rei, ou seja, até a coluna de destino inclusive)
            if abs(col_check - curr_col) <= 2:
                if board.is_square_under_attack(square, self.color):
                    return False
                    
            col_check += step

        return True