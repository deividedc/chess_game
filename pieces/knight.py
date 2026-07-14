#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:37:07 2026

@author: deivid
"""

from pieces.piece import Piece

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Knight estende a classe abstrata Piece de forma isolada e modular. O motor do jogo 
# está fechado para modificações no seu núcleo, mas aberto para extensões como esta peça e suas regras de movimento.
class Knight(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'n' para pretas, 'N' para brancas
        symbol = 'n' if color == 'black' else 'N'
        
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # O construtor invoca super().__init__ respeitando rigorosamente a interface da classe base.
        # Qualquer parte do sistema que espere um objeto "Piece" pode operar com "Knight" sem falhas.
        super().__init__(color, 'Knight', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Cavalo é geometricamente correto.
        O Cavalo move-se em formato de "L" (2 casas em uma direção e 1 na perpendicular).
        É a única peça que pode saltar sobre outras peças.
        """
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # A assinatura do método e o tipo de retorno (bool) atendem perfeitamente ao contrato polimórfico
        # estabelecido pela superclasse Piece.
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. Calcula as variações absolutas de linha e coluna
        delta_row = abs(new_row - curr_row)
        delta_col = abs(new_col - curr_col)

        # 3. Regra matemática do movimento em "L":
        # Deve andar (2 em linha e 1 em coluna) OU (1 em linha e 2 em coluna)
        is_l_move = (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)
        
        if not is_l_move:
            return False

        # 4. S (Responsabilidade Única) & D (Inversão de Dependência): 
        # O Cavalo possui a responsabilidade única de validar sua regra matemática de salto em L.
        # Ao ignorar a verificação de caminhos bloqueados (já que ele pula peças) e consultar apenas
        # a ocupação da casa final através da abstração injetada `board`, ele cumpre sua função de forma desacoplada.
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True