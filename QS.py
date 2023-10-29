import numpy as np
import random
from queue import Queue
import matplotlib.pyplot as plt

class CityGrid:
    def __init__(self, rows, cols, obstacle_coverage=0.3):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

        # Генерация случайных препятствий
        self.generate_obstacles(obstacle_coverage)

    def generate_obstacles(self, obstacle_coverage):
        # Генерация случайных блокированных кварталов в сетке
        total_blocks = self.rows * self.cols
        num_obstacles = int(obstacle_coverage * total_blocks)

        obstacle_indices = random.sample(range(total_blocks), num_obstacles)

        for index in obstacle_indices:
            row = index // self.cols
            col = index % self.cols
            self.grid[row][col] = 1  # Обозначим препятствие как 1

    def place_tower(self, row, col, range_R):
        # Размещение башни и визуализация ее покрытия
        for i in range(max(0, row - range_R), min(self.rows, row + range_R + 1)):
            for j in range(max(0, col - range_R), min(self.cols, col + range_R + 1)):
                self.grid[i][j] = 2  # Обозначим зону покрытия башни как 2


    def optimize_towers(self, range_R):
        # Алгоритм оптимизации размещения башен
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 0:  # Проверка, что блок не заблокирован
                    # Размещаем башню, если незащищенный блок не покрыт ни одной башней
                    is_covered = False
                    for i in range(max(0, row - range_R), min(self.rows, row + range_R + 1)):
                        for j in range(max(0, col - range_R), min(self.cols, col + range_R + 1)):
                            if self.grid[i][j] == 2:
                                is_covered = True
                                break
                        if is_covered:
                            break

                    if not is_covered:
                        self.place_tower(row, col, range_R)

    def find_reliable_path(self, start_tower, end_tower):
        start_row, start_col = start_tower
        end_row, end_col = end_tower

        # Используем поиск в ширину (BFS) для нахождения пути с наименьшим числом переходов
        visited = set()
        queue = Queue()
        queue.put((start_row, start_col, 0))  # Тройка (строка, столбец, количество переходов)
        visited.add((start_row, start_col))

        while not queue.empty():
            current_row, current_col, num_transitions = queue.get()

            if current_row == end_row and current_col == end_col:
                return num_transitions  # Минимальное количество переходов до конечной башни

            # Перебираем соседние блоки (вверх, вниз, влево, вправо)
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_row, new_col = current_row + dr, current_col + dc

                if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.grid[new_row][new_col] != 1 and (new_row, new_col) not in visited:
                    queue.put((new_row, new_col, num_transitions + 1))
                    visited.add((new_row, new_col))

        return float('inf')  # Если путь не найден
    def visualize(self):
        plt.figure(figsize=(8, 8))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 0:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'go', markersize=20)  # Свободные блоки (зеленые)
                elif self.grid[row][col] == 1:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'ro', markersize=20)  # Блокированные блоки (красные)
                elif self.grid[row][col] == 2:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'bo', markersize=20)  # Башни (синие)

        plt.gca().invert_yaxis()
        plt.grid(True, linestyle='--', color='gray', linewidth=1, alpha=0.5)
        plt.show()

    def visualize_path(self, path):
        plt.figure(figsize=(8, 8))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 0:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'go', markersize=20)  # Свободные блоки (зеленые)
                elif self.grid[row][col] == 1:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'ro', markersize=20)  # Блокированные блоки (красные)
                elif self.grid[row][col] == 2:
                    plt.plot(col + 0.5, self.rows - row - 0.5, 'bo', markersize=20)  # Башни (синие)

        path_x, path_y = zip(*path)
        plt.plot(path_x, path_y, 'b-', linewidth=3, alpha=0.7)  # Путь передачи данных (синяя линия)

        plt.gca().invert_yaxis()
        plt.grid(True, linestyle='--', color='gray', linewidth=1, alpha=0.5)
        plt.show()
# Пример использования:
city = CityGrid(10, 10, obstacle_coverage=0.3)
city.optimize_towers(2)  # Оптимизировать размещение башен с диапазоном 2
city.visualize()

reliable_path = city.find_reliable_path((4, 4), (7, 7))
path = [(1, 1)]
for _ in range(reliable_path):
    path.append((7, 7))
city.visualize_path(path)