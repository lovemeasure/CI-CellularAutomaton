import numpy as np
import matplotlib.pyplot as plt

class CellularAutomaton:
    def __init__(self, size=100, rule=30, steps=50, initial_condition=None):
        self.size = size
        self.rule = self._rule_to_binary(rule)
        self.grid = np.zeros(size, dtype=int)
        if initial_condition:
            self._set_initial_condition(initial_condition)
        else:
            self.grid[size // 2] = 1  # デフォルトの初期状態: 中央のセルのみ1
        self.steps = steps
        self.history = []

    def _rule_to_binary(self, rule):
        """ルール番号を2進数形式のリストに変換"""
        return np.array([int(x) for x in f'{rule:08b}'])

    def _set_initial_condition(self, initial_condition):
        """ユーザーからの初期条件をセット"""
        for i, val in enumerate(initial_condition):
            if i < self.size:
                self.grid[i] = int(val)

    def step(self):
        """1ステップ分の更新を実行"""
        new_grid = np.zeros_like(self.grid)
        for i in range(self.size):
            left = self.grid[(i - 1) % self.size]  # 左隣
            center = self.grid[i]                  # 中心
            right = self.grid[(i + 1) % self.size] # 右隣
            pattern = (left << 2) | (center << 1) | right
            new_grid[i] = self.rule[7 - pattern]   # パターンに基づいて新しい値を決定
        self.grid = new_grid
        self.history.append(self.grid.copy())

    def run(self):
        """セルオートマトンを指定したステップ数だけ実行"""
        self.history = [self.grid.copy()]
        for _ in range(self.steps):
            self.step()

    def plot(self):
        """実行結果をプロット（グリッド付き）"""
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(self.history, cmap='binary', interpolation='nearest')

        # 方眼用紙のようにグリッド線を追加
        ax.set_xticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.steps, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)

        ax.set_title(f'Cellular Automaton with Rule {int("".join(map(str, self.rule)), 2)}')
        plt.show()

if __name__ == "__main__":
    # セルサイズとルール、実行ステップ数を設定
    size = int(input("セルのサイズを入力してください: "))
    rule = int(input("ルール番号（0〜255）を入力してください: "))
    steps = int(input("実行時間（ステップ数）を入力してください: "))

    # 初期条件を入力するか、スキップするかを選択
    use_initial_condition = input("初期条件を入力しますか？ (y/n): ").lower()

    if use_initial_condition == 'y':
        initial_condition = input(f"初期条件を01で入力してください（長さ{size}まで）: ")
    else:
        initial_condition = None

    ca = CellularAutomaton(size=size, rule=rule, steps=steps, initial_condition=initial_condition)
    ca.run()
    ca.plot()
