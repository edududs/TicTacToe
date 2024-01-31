from abc import ABC, abstractmethod
from typing import Optional

import pygame


class Game(ABC):
    def __init__(self, screen_size: Optional[tuple] = None) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            screen_size if screen_size else (640, 480)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def events(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class TicTacToe(Game):
    def __init__(self, screen_size: tuple | None = None) -> None:
        super().__init__(screen_size)
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None

    def run(self) -> None:
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                x, y = pygame.mouse.get_pos()
                if 0 <= y < 480 and 0 <= x < 480:
                    row, col = y // 160, x // 160
                    if self.board[row][col] == " ":
                        self.board[row][col] = self.current_player
                        self.current_player = "O" if self.current_player == "X" else "X"

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    pygame.Rect(col * 160, row * 160, 160, 160),
                    3,
                )
                font = pygame.font.Font(None, 120)
                text_surface = font.render(self.board[row][col], True, (0, 0, 0))
                text_rect = text_surface.get_rect(
                    center=(col * 160 + 80, row * 160 + 80)
                )
                self.screen.blit(text_surface, text_rect)

        if self.winner:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(f"Winner: {self.winner}", True, (255, 0, 0))
            text_rect = text_surface.get_rect(
                center=(
                    self.screen.get_width() // 2 + 240,
                    self.screen.get_height() // 2,
                )
            )
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def update(self) -> None:
        self.winner = self.check_winner()
        ticatactoe = self.check_tictactoe()
        if ticatactoe:
            self.running = False

    def check_winner(self):
        # Verificar linhas e colunas
        for i in range(3):
            # Verificar linhas
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]

            # Verificar colunas
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]

        # Verificar diagonais
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        # Se ninguém venceu
        return None

    def check_tictactoe(self) -> bool:
        # Verifica se todas as células do tabuleiro foram preenchidas
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False

        if not self.check_winner():
            return True

        return False


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
