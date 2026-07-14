from pieces.piece import Piece

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Bishop estende a classe abstrata Piece de forma modular. Novas regras ou novas peças
# podem ser acopladas criando novos arquivos sem precisar alterar o código base ou o motor do jogo.
class Bishop(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'b' para pretas, 'B' para brancas
        symbol = 'b' if color == 'black' else 'B'
        
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # O construtor preserva exatamente a interface exigida pela superclasse Piece.
        # Um objeto Bishop pode substituir dinamicamente qualquer referência genérica a Piece sem quebrar o sistema.
        super().__init__(color, 'Bishop', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Bispo é geometricamente correto.
        O Bispo move-se qualquer quantidade de casas, exclusivamente nas diagonais.
        """
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # A assinatura do método e o tipo de retorno booleano seguem à risca o contrato estipulado 
        # pela classe mãe, garantindo o polimorfismo puro durante a varredura do tabuleiro.
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

        # 4. S (Responsabilidade Única): O Bispo sabe apenas a "geometria" do seu movimento diagonal.
        # Ele delega ao Tabuleiro (board) a responsabilidade de varrer a matriz e checar obstruções,
        # mantendo um único motivo para mudar.
        if board.is_path_blocked(self.position, new_position):
            return False

        # 5. S & D (Inversão de Dependência): A peça não interage com o estado global do jogo de forma rígida;
        # ela depende da abstração injetada via parâmetro (board) para validar o destino e mantém sua 
        # única responsabilidade de testar regras locais.
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True