#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:37:07 2026

@author: deivid
"""

from pieces.piece import Piece

class Knight(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'n' para pretas, 'N' para brancas
        symbol = 'n' if color == 'black' else 'N'
        super().__init__(color, 'Knight', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Cavalo é geometricamente correto.
        O Cavalo move-se em formato de "L" (2 casas em uma direção e 1 na perpendicular).
        É a única peça que pode saltar sobre outras peças.
        """
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

        # 4. Verificação da casa de destino:
        # Como o Cavalo "pula" peças, NÃO precisamos verificar se o caminho está bloqueado (board.is_path_blocked).
        # Apenas precisamos garantir que ele não tente capturar uma peça aliada na casa de destino.
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True