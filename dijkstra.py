import heapq
from typing import List, Tuple


BoardState = Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]]


def neighbors(board_state: BoardState) -> List[Tuple[int, BoardState]]:
    zero_pos = find_zero(board_state)
    neighbors = []
    cost = 1
    for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_pos = (zero_pos[0] + d[0], zero_pos[1] + d[1])
        if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
            neighbors.append((cost, swap(board_state, zero_pos, new_pos)))
    return neighbors


def h(board_state: BoardState) -> int:
    goal = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    return sum(abs(i - gi) + abs(j - gj) for i, row in enumerate(board_state) for j, val in enumerate(row)
               for gi, grow in enumerate(goal) for gj, gval in enumerate(grow) if val == gval)


def board_to_tuple(board: List[List[int]]):
    return tuple(tuple(row) for row in board)


def tuple_to_board(board_state: BoardState) -> List[List[int]]:
    return [list(row) for row in board_state]


def find_zero(board_state: BoardState) -> Tuple[int, int]:
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == 0:
                return i, j


def swap(board_state: BoardState, pos1: Tuple[int, int], pos2: Tuple[int, int]):
    board = tuple_to_board(board_state)
    board[pos1[0]][pos1[1]], board[pos2[0]][pos2[1]] = board[pos2[0]][pos2[1]], board[pos1[0]][pos1[1]]
    return board_to_tuple(board)


def dijkstra(start, goal):
    queue = []
    heapq.heappush(queue, (0, start))  # 创建堆队列，保存(g_score, hashable_state)
    paths = {start: (None, None)}  # 记录经过的路径，保存hashable_state:()
    g_scores = {start: 0}

    while queue:
        g_score, state = heapq.heappop(queue)
        if state == goal:
            return get_path(paths, start, goal), g_score
        for cost, next_state in neighbors(state):
            new_g_score = g_scores[state] + cost
            if next_state not in g_scores or new_g_score < g_scores[next_state]:
                g_scores[next_state] = new_g_score
                f_score = new_g_score + h(next_state)
                heapq.heappush(queue, (f_score, next_state))
                paths[next_state] = (state, cost)
    return None, None


def get_path(paths, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current, _ = paths[current]
    path.append(start)
    path.reverse()
    return path


def path_to_actions(path):
    actions = []
    i0, j0 = 0, 0
    for state in path:
        i, j = find_zero(state)
        di, dj = i0 - i, j0 - j
        i0, j0 = i, j
        actions.append((di, dj))
    return actions[1:]


if __name__ == "__main__":
    start = ((3, 8, 5), (4, 0, 1), (2, 7, 6))
    goal = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    path, cost = dijkstra(start, goal)
    print(path_to_actions(path), cost)
