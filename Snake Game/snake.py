import pygame
import random
import heapq
import enum
import sys
from typing import List, Tuple, Set, Optional

class GameState(enum.Enum):
    RUNNING = 0
    GAME_OVER = 1
    PAUSED = 2

class Settings:
    """ Game configuration and constants """
    # Screen Dimensions
    WIDTH = 800
    HEIGHT = 600
    GRID_SIZE = 20
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (100, 100, 100)

    # Game Settings
    FPS = 10
    DIFFICULTY_LEVELS = {
        'Easy': 5,
        'Medium': 10,
        'Hard': 15
    }

class Node:
    """A* Pathfinding Node representation"""
    def __init__(self, position: Tuple[int, int], g: int = 0, h: int = 0):
        self.position = position
        self.g = g  # Cost from start node
        self.h = h  # Heuristic (estimated cost to goal)
        self.f = g + h  # Total cost
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

class PathfindingStrategy:
    """Flexible Pathfinding Strategy"""
    @staticmethod
    def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def get_neighbors(current: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]

class AStar:
    """A* Pathfinding Algorithm"""
    @staticmethod
    def find_path(
        start: Tuple[int, int], 
        goal: Tuple[int, int], 
        snake_body: List[Tuple[int, int]], 
        obstacles: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        open_list = []
        closed_set = set()
        
        start_node = Node(start, h=PathfindingStrategy.manhattan_distance(start, goal))
        heapq.heappush(open_list, start_node)

        max_iterations = Settings.GRID_WIDTH * Settings.GRID_HEIGHT
        iterations = 0

        while open_list and iterations < max_iterations:
            iterations += 1
            current_node = heapq.heappop(open_list)

            if current_node.position == goal:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1][1:]

            closed_set.add(current_node.position)

            for neighbor_pos in PathfindingStrategy.get_neighbors(current_node.position):
                # Skip if neighbor is an obstacle or out of bounds
                if (neighbor_pos in obstacles or 
                    neighbor_pos[0] < 0 or neighbor_pos[0] >= Settings.GRID_WIDTH or 
                    neighbor_pos[1] < 0 or neighbor_pos[1] >= Settings.GRID_HEIGHT):
                    continue

                neighbor = Node(
                    neighbor_pos, 
                    g=current_node.g + 1, 
                    h=PathfindingStrategy.manhattan_distance(neighbor_pos, goal)
                )
                neighbor.parent = current_node

                if neighbor.position in closed_set:
                    continue

                # Check if neighbor is already in open list with a lower cost
                existing_node = next((n for n in open_list if n.position == neighbor.position), None)
                if existing_node and existing_node.f <= neighbor.f:
                    continue

                heapq.heappush(open_list, neighbor)

        return []  # No path found

class Snake:
    """Snake game entity"""
    def __init__(self):
        self.body: List[Tuple[int, int]] = [(Settings.GRID_WIDTH // 2, Settings.GRID_HEIGHT // 2)]
        self.direction: Tuple[int, int] = (1, 0)
        self.length: int = 1

    def move(self, path: Optional[List[Tuple[int, int]]] = None):
        if path:
            next_pos = path.pop(0)
            self.body.insert(0, next_pos)
            
            if len(self.body) > self.length:
                self.body.pop()

    def grow(self):
        self.length += 1

class Food:
    """Food generation and management"""
    def __init__(self, snake_body: List[Tuple[int, int]]):
        self.position = self.randomize_position(snake_body)

    def randomize_position(self, snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        while True:
            pos = (
                random.randint(0, Settings.GRID_WIDTH - 1), 
                random.randint(0, Settings.GRID_HEIGHT - 1)
            )
            if pos not in snake_body:
                return pos

class Renderer:
    """Game rendering and display management"""
    @staticmethod
    def draw(screen, game):
        screen.fill(Settings.BLACK)

        # Draw Snake
        for segment in game.snake.body:
            pygame.draw.rect(screen, Settings.GREEN, 
                             (segment[0] * Settings.GRID_SIZE, 
                              segment[1] * Settings.GRID_SIZE, 
                              Settings.GRID_SIZE, Settings.GRID_SIZE))

        # Draw Food
        pygame.draw.rect(screen, Settings.RED, 
                         (game.food.position[0] * Settings.GRID_SIZE, 
                          game.food.position[1] * Settings.GRID_SIZE, 
                          Settings.GRID_SIZE, Settings.GRID_SIZE))

        # Draw Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {game.score}", True, Settings.WHITE)
        screen.blit(score_text, (10, 10))

        # Draw Game Over or Pause
        if game.state == GameState.GAME_OVER:
            game_over_text = font.render("Game Over!", True, Settings.RED)
            screen.blit(game_over_text, (Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2))

        # Draw Exit Instructions
        if game.state in [GameState.GAME_OVER, GameState.RUNNING]:
            exit_text = font.render("Press ESC to Exit", True, Settings.WHITE)
            screen.blit(exit_text, (Settings.WIDTH // 2 - 100, Settings.HEIGHT - 50))

        pygame.display.flip()

class Game:
    """Main game logic and management"""
    def __init__(self, difficulty: str = 'Medium'):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        pygame.display.set_caption("Advanced Snake Game with A* Pathfinding")
        
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.state = GameState.RUNNING
        self.fps = Settings.DIFFICULTY_LEVELS.get(difficulty, 10)

    def handle_events(self):
        """Centralized event handling method"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
                
                # Restart game when in game over state
                if event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.__init__()

    def exit_game(self):
        """Properly exit the game"""
        pygame.quit()
        sys.exit()

    def check_collision(self):
        head = self.snake.body[0]

        # Wall collision
        if (head[0] < 0 or head[0] >= Settings.GRID_WIDTH or 
            head[1] < 0 or head[1] >= Settings.GRID_HEIGHT):
            self.state = GameState.GAME_OVER

        # Self collision
        if head in self.snake.body[1:]:
            self.state = GameState.GAME_OVER

        # Food collision
        if head == self.food.position:
            self.snake.grow()
            self.food = Food(self.snake.body)
            self.score += 1

    def run(self):
        running = True
        while running:
            self.handle_events()

            if self.state == GameState.RUNNING:
                # Find path to food using A*
                obstacles = set(self.snake.body[1:])
                path = AStar.find_path(
                    self.snake.body[0], 
                    self.food.position, 
                    self.snake.body, 
                    obstacles
                )

                if path:
                    self.snake.move(path)

                self.check_collision()

            Renderer.draw(self.screen, self)
            
            self.clock.tick(self.fps)

def main():
    game = Game(difficulty='Hard')
    game.run()

if __name__ == "__main__":
    main()