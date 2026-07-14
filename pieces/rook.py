#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:14:44 2026

@author: deivid
"""

from pieces.piece import Piece

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Rook estende a classe abstrata Piece de forma modular. Novas regras ou novas peças
# podem ser adicionadas criando novos arquivos sem precisar alterar o código base ou o motor do jogo.
class Rook(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'r' para pretas, 'R' para brancas
        symbol = 'r' if color == 'black' else 'R'
        
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # O construtor preserva exatamente a interface exigida pela superclasse Piece. 
        # Um objeto Rook pode substituir dinamicamente qualquer referência genérica a Piece sem quebrar o sistema.
        super().__init__(color, 'Rook', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # A assinatura do método e o tipo de retorno booleano seguem à risca o contrato estipulado 
        # pela classe mãe, garantindo o polimorfismo puro durante a varredura do tabuleiro.
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. A torre se move apenas em linha reta (vertical ou horizontal)
        is_straight = (curr_row == new_row) or (curr_col == new_col)
        if not is_straight:
            return False

        # 3. S (Responsabilidade Única): A Torre sabe apenas a "geometria" do seu movimento linear.
        # Ela delega ao Tabuleiro (board) a responsabilidade de varrer a matriz e checar obstruções,
        # mantendo um único motivo para mudar.
        if board.is_path_blocked(self.position, new_position):
            return False

        # 4. S & D (Inversão de Dependência): A peça não interage com o estado global do jogo de forma rígida;
        # ela depende da abstração injetada via parâmetro (board) para validar o destino e mantém sua 
        # única responsabilidade de testar regras locais.
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True