# Auto8Puzzle——A*算法的应用实例

pygame编写的8puzzle小游戏

按`s`键进入自动求解,(使用**A*算法**实现)

![demo.png](demo.png)

### 算法原理

已知棋盘状态之间的状态转移模型，我们只需要求解出从起始状态到终止状态的一条通路即可。
由于状态空间很大，而且我们无需保证结果的最优性，所以可以采用像A*之类的启发式搜索算法
