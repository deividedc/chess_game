from abc import ABC, abstractmethod

class Piece(ABC):
    # Dicionário de mapeamento de classe para renderizar os ícones reais
    _UNICODE_SYMBOLS = {
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',  # Peças Brancas (Preenchidas = Claras no console dark)
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙'   # Peças Pretas (Vazadas = Escuras no console dark)
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

    @abstractmethod
    def is_valid_move(self, new_position: tuple, board) -> bool:
        pass

    # =========================================================================
    # ENCAPSULAMENTO (Getters e Setters)
    # =========================================================================

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