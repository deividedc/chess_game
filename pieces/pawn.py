#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:34:27 2026

@author: deivid
"""

from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'p' para pretas, 'P' para brancas
        symbol = 'p' if color == 'black' else 'P'
        super().__init__(color, 'Pawn', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Peão é geometricamente correto de acordo com as regras do xadrez.
        """
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Determina a direção do movimento baseada na cor do peão
        # Brancas sobem o tabuleiro (diminuem o índice da linha)
        # Pretas descem o tabuleiro (aumentam o índice da linha)
        direction = -1 if self.color == 'white' else 1

        delta_row = new_row - curr_row
        delta_col = abs(new_col - curr_col)

        # ==========================================
        # CASO A: MOVIMENTO SIMPLES (Apenas para a frente)
        # ==========================================
        if delta_col == 0:
            # Avanço de 1 casa
            if delta_row == direction:
                # A casa da frente deve estar completamente vazia
                return board.get_piece_at(new_position) is None

            # Avanço duplo de 2 casas (apenas no primeiro movimento)
            elif delta_row == 2 * direction and not self.moved:
                # Ambas as casas (a intermediária e a de destino) devem estar vazias
                intermediate_square = (curr_row + direction, curr_col)
                return (board.get_piece_at(intermediate_square) is None and 
                        board.get_piece_at(new_position) is None)

        # ==========================================
        # CASO B: CAPTURA PADRÃO (Diagonal para a frente)
        # ==========================================
        elif delta_col == 1 and delta_row == direction:
            destination_piece = board.get_piece_at(new_position)
            
            # Se houver uma peça na diagonal e ela for inimiga, a captura é válida
            if destination_piece is not None:
                return destination_piece.color != self.color
            
            # ==========================================
            # CASO C: CAPTURA EN PASSANT
            # ==========================================
            # Se a casa de destino está vazia, o peão pode estar tentando capturar "En Passant".
            # Quem valida as regras de En Passant é o Tabuleiro, pois precisamos saber se o
            # peão adversário adjacente acabou de se mover 2 casas na última jogada da partida.
            if board.can_en_passant(self.position, new_position):
                return True

        return False