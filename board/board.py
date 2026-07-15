#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:38:29 2026

@author: deivid
"""

from pieces import Pawn, Rook, Knight, Bishop, Queen, King

# O - Open/Closed Principle (Princípio Aberto/Fechado):
# A classe Board está totalmente fechada para modificações de comportamento das peças individuais.
# Se novas peças com mecânicas exóticas forem adicionadas, o algoritmo de varredura ou impressão do 
# tabuleiro não sofrerá nenhuma alteração, pois ele trata todas as peças de forma genérica.
class Board:
    def __init__(self):
        # Inicializa um tabuleiro vazio (matriz 8x8 preenchida com None)
        self._grid = [[None for _ in range(8)] for _ in range(8)]
        # Registo para a lógica de En Passant (guarda a coordenada do Roo` que deu o salto duplo)
        self.en_passant_target = None
        # Configura as peças nas suas posições iniciais
        self.initial_setup()

    def get_piece_at(self, position: tuple):
        """Retorna a peça na coordenada dada ou None se estiver vazia."""
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self._grid[row][col]
        return None

    def set_piece_at(self, position: tuple, piece):
        """Coloca uma peça numa coordenada específica e atualiza a posição interna da peça."""
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            self._grid[row][col] = piece
            if piece is not None:
                piece.position = position

    # Métodos para permitir a indexação direta: tabuleiro[linha, coluna]
    def __getitem__(self, index):
        row, col = index
        return self.get_piece_at((row, col))

    def __setitem__(self, index, piece):
        row, col = index
        self.set_piece_at((row, col), piece)

    def initial_setup(self):
        """Configura o tabuleiro com a disposição oficial de peças do Xadrez."""
        # --- PEÇAS PRETAS (Linhas 0 e 1) ---
        for i in range(8):
            self[1, i] = Pawn('black', (1, i))

        self[0, 0] = Rook('black', (0, 0))
        self[0, 7] = Rook('black', (0, 7))
        self[0, 1] = Knight('black', (0, 1))
        self[0, 6] = Knight('black', (0, 6))
        self[0, 2] = Bishop('black', (0, 2))
        self[0, 5] = Bishop('black', (0, 5))
        self[0, 3] = Queen('black', (0, 3))
        self[0, 4] = King('black', (0, 4))

        # --- PEÇAS BRANCAS (Linhas 6 e 7) ---
        for i in range(8):
            self[6, i] = Pawn('white', (6, i))

        self[7, 0] = Rook('white', (7, 0))
        self[7, 7] = Rook('white', (7, 7))
        self[7, 1] = Knight('white', (7, 1))
        self[7, 6] = Knight('white', (7, 6))
        self[7, 2] = Bishop('white', (7, 2))
        self[7, 5] = Bishop('white', (7, 5))
        self[7, 3] = Queen('white', (7, 3))
        self[7, 4] = King('white', (7, 4))

    def is_path_blocked(self, start: tuple, end: tuple) -> bool:
        """
        SRP (Responsabilidade Única): O tabuleiro detém a única e exclusiva responsabilidade de
        conhecer a matriz e calcular colisões de trajeto físico, liberando as peças dessa carga de dados.
        """
        start_row, start_col = start
        end_row, end_col = end

        # Calcula a direção do passo (-1, 0 ou 1)
        step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)

        curr_row = start_row + step_row
        curr_col = start_col + step_col

        # Percorre o caminho até chegar antes da casa final
        while (curr_row, curr_col) != (end_row, end_col):
            if self.get_piece_at((curr_row, curr_col)) is not None:
                return True  # Caminho obstruído!
            curr_row += step_row
            curr_col += step_col

        return False

    def is_square_under_attack(self, position: tuple, defensive_color: str) -> bool:
        """
        L - Liskov Substitution Principle (Princípio da Substituição de Liskov):
        O tabuleiro interage de forma polimórfica com a lista de peças ao disparar `piece.is_valid_move`.
        Ele não precisa checar sub-tipos estritos; qualquer subclasse derivada responde ao mesmo método perfeitamente.
        """
        target_row, target_col = position
        for r in range(8):
            for c in range(8):
                piece = self.get_piece_at((r, c))
                if piece is not None and piece.color != defensive_color:
                    if piece.name == 'King':
                        king_row, king_col = piece.position
                        if abs(king_row - target_row) <= 1 and abs(king_col - target_col) <= 1:
                            return True
                    else:
                        if piece.is_valid_move(position, self):
                            return True
        return False

    def can_en_passant(self, pawn_position: tuple, target_position: tuple) -> bool:
        """
        Valida se o movimento de captura En Passant é permitido.
        """
        if self.en_passant_target is None:
            return False
        return target_position == self.en_passant_target

    # =========================================================================
    # LÓGICA DE XEQUE, XEQUE-MATE E EMPATE
    # =========================================================================

    def find_king(self, color: str) -> tuple:
        """Encontra a coordenada atual do Rei da cor especificada."""
        for r in range(8):
            for c in range(8):
                piece = self.get_piece_at((r, c))
                # Ajustado para 'Rei' em conformidade com a nomenclatura em português das suas peças
                if piece is not None and piece.name == 'King' and piece.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color: str) -> bool:
        """Verifica se o Rei da cor especificada está atualmente sob ataque."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        return self.is_square_under_attack(king_pos, color)

    def has_any_valid_moves(self, color: str) -> bool:
        """
        SRP (Responsabilidade Única): Centraliza a complexidade algorítmica de predição e simulação de estados.
        As peças se limitam a validar vetores geométricos simples, enquanto o Tabuleiro gerencia a simulação
        hipotética de jogadas para calcular a evasão de xeques.
        """
        for r in range(8):
            for c in range(8):
                piece = self.get_piece_at((r, c))
                if piece is None or piece.color != color:
                    continue

                # Varre todo o tabuleiro buscando uma casa de destino elegível
                for target_r in range(8):
                    for target_c in range(8):
                        target_pos = (target_r, target_c)

                        if piece.is_valid_move(target_pos, self):
                            # Simulação temporária do movimento
                            original_piece = self.get_piece_at(target_pos)
                            original_pos = piece.position

                            self._grid[r][c] = None
                            self._grid[target_r][target_c] = piece
                            piece.position = target_pos

                            # O movimento simulado livrou o Rei do xeque?
                            still_in_check = self.is_in_check(color)

                            # Desfaz o movimento hipotético
                            self._grid[r][c] = piece
                            self._grid[target_r][target_c] = original_piece
                            piece.position = original_pos

                            # Se o movimento é seguro e livra do xeque, o jogador tem uma jogada válida!
                            if not still_in_check:
                                return True
        return False

    def is_checkmate(self, color: str) -> bool:
        """O jogador está em xeque e não possui nenhum movimento de defesa legal."""
        return self.is_in_check(color) and not self.has_any_valid_moves(color)

    def is_stalemate(self, color: str) -> bool:
        """O jogador não está em xeque, mas não possui nenhuma jogada legal restante (Afogamento)."""
        return not self.is_in_check(color) and not self.has_any_valid_moves(color)

    def print_board(self):
        """Imprime o tabuleiro de forma elegante, estruturada e perfeitamente alinhada."""
        print("\n      0   1   2   3   4   5   6   7")
        print("    ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        
        for r in range(8):
            print(f"  {r} │", end="")
            for c in range(8):
                piece = self.get_piece_at((r, c))
                if piece is None:
                    print(" · ", end="│")
                else:
                    print(f" {piece} ", end="│")
            print(f" {r}")
            
            if r < 7:
                print("    ├───┼───┼───┼───┼───┼───┼───┼───┤")
        
        print("    └───┴───┴───┴───┴───┴───┴───┴───┘")
        print("      0   1   2   3   4   5   6   7\n")
