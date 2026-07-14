#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:34:27 2026

@author: deivid
"""

from pieces.piece import Piece

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Pawn estende a classe abstrata Piece. As regras complexas e únicas do Peão (direção por cor, 
# primeiro movimento duplo, En Passant) são encapsuladas aqui sem alterar a estrutura das outras peças.
class Pawn(Piece):
    def __init__(self, color: str, position: tuple):
        # Define o símbolo: 'p' para pretas, 'P' para brancas
        symbol = 'p' if color == 'black' else 'P'
        
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # Garante a conformidade com a superclasse Piece ao invocar o construtor padrão.
        # Qualquer componente do sistema trata o Peão de forma polimórfica como uma peça comum.
        super().__init__(color, 'Pawn', symbol, position, False)

    def is_valid_move(self, new_position: tuple, board) -> bool:
        """
        Valida se o movimento do Peão é geometricamente correto de acordo com as regras do xadrez.
        """
        # L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        # Mantém estritamente a mesma assinatura de método e tipo de retorno esperado pela classe abstrata.
        curr_row, curr_col = self.position
        new_row, new_col = new_position

        # 1. Determina a direção do movimento baseada na cor do peão
        direction = -1 if self.color == 'white' else 1

        delta_row = new_row - curr_row
        delta_col = abs(new_col - curr_col)

        # ==========================================
        # CASO A: MOVIMENTO SIMPLES (Apenas para a frente)
        # ==========================================
        if delta_col == 0:
            # Avanço de 1 casa
            if delta_row == direction:
                # S (Responsabilidade Única): O Peão calcula a direção lógica do avanço,
                # mas consulta o tabuleiro (board) para saber o estado de ocupação da casa.
                return board.get_piece_at(new_position) is None

            # Avanço duplo de 2 casas (apenas no primeiro movimento)
            elif delta_row == 2 * direction and not self.moved:
                # S: A peça conhece seu estado interno (self.moved), mas delega ao tabuleiro 
                # a responsabilidade de inspecionar fisicamente o caminho intermediário na matriz.
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
            # S (Responsabilidade Única) & D (Inversão de Dependência): O Peão sabe que a diagonal vazia 
            # pode significar um En Passant, mas ele NÃO rastreia o histórico de turnos do jogo. 
            # Ele delega essa validação complexa à abstração do tabuleiro (`board.can_en_passant`), 
            # mantendo uma única responsabilidade e evitando acoplamento rígido.
            if board.can_en_passant(self.position, new_position):
                return True

        return False