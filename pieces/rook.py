#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:14:44 2026

@author: deivid
"""

from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'r' para pretas, 'R' para brancas
        symbol = 'r' if color == 'black' else 'R'
        super().__init__(color, 'Rook', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Não pode se mover para a mesma casa em que já está
        if curr_row == new_row and curr_col == new_col:
            return False

        # 2. A torre se move apenas em linha reta (vertical ou horizontal)
        is_straight = (curr_row == new_row) or (curr_col == new_col)
        if not is_straight:
            return False

        # 3. SRP: Verifica se há peças bloqueando o caminho
        # Agora a torre NÃO vai mais conseguir saltar sobre o Peão!
        if board.is_path_blocked(self.position, new_position):
            return False

        # 4. Verifica se a casa de destino está ocupada por uma peça aliada
        destination_piece = board.get_piece_at(new_position)
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True