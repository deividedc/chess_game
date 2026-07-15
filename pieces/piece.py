from abc import ABC, abstractmethod

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Piece foi criada usando a classe abstrata (ABC), definindo uma estrutura genérica rígida.
# O núcleo do jogo está fechado para modificações, mas totalmente aberto para expansões: 
# qualquer nova peça criada só precisa herdar de Piece.
class Piece(ABC):
    # Dicionário de mapeamento de classe para renderizar os ícones reais
    _UNICODE_SYMBOLS = {
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',  # Peças Brancas
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙'   # Peças Pretas
    }

    def __init__(self, color: str, name: str, symbol: str, position: tuple, moved: bool = False):
        self._color = color
        self._name = name
        self._symbol = symbol     # Continua guardando 'P', 'p', 'N', etc.
        self._position = position
        self._moved = moved

    def __repr__(self) -> str:
        # Quando o tabuleiro tentar imprimir a peça, ela se auto-traduz para o ícone Unicode correspondente.
        # Se por algum motivo o símbolo não estiver no dicionário, ela mostra o caractere original.
        return self._UNICODE_SYMBOLS.get(self._symbol, self._symbol)

    # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
    # O uso do decorador @abstractmethod força todas as subclasses derivadas (Rei, Rainha, etc.)
    # a implementarem obrigatoriamente este método seguindo a mesma assinatura. Isso garante que o motor
    # do jogo possa chamar `is_valid_move` em qualquer peça de forma polimórfica e segura, sem quebras.
    @abstractmethod
    def is_valid_move(self, new_position: tuple, board) -> bool:
        pass

    # =========================================================================
    # ENCAPSULAMENTO (Getters e Setters)
    # =========================================================================

    # S (Responsabilidade Única): A classe Piece detém a única responsabilidade de encapsular 
    # as propriedades fundamentais do estado de uma peça genérica (cor, nome, posição, se moveu).
    # Ela não interfere na matriz do tabuleiro e não decide mecânicas externas do jogo.
    @property
    def color(self) -> str:
        return self._color

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, new_position: tuple):
        if isinstance(new_position, tuple) and len(new_position) == 2:
            self._position = new_position
        else:
            raise ValueError("A posição deve ser uma tupla com duas coordenadas.")

    @property
    def moved(self) -> bool:
        return self._moved

    @moved.setter
    def moved(self, status: bool):
        if isinstance(status, bool):
            self._moved = status
        else:
            raise ValueError("O estado 'moved' deve ser um valor booleano.")