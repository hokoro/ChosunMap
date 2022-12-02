import numpy as np
from numpy.random import choice as np_choice


class AntColony(object):
    def __init__(self, start, goal, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
        """
        self.distances = distances  # a장소에서 b장소까지의 거리를 2차원 행렬로 표현
        self.pheromone = np.ones(self.distances.shape) / len(distances)  # 거리 저장한 행렬과 같은 모양의 1로 가득찬 배열 생성
        self.all_inds = range(len(distances))
        self.n_ants = n_ants  # 개미 수
        self.n_best = n_best  # 최적의 경로의 수
        self.n_iterations = n_iterations  # 반복 횟수
        self.decay = decay  # 1회 반복당 페로몬 증발률
        self.alpha = alpha  # 페로몬에 가중치를 더하는 변수
        self.beta = beta  # 만족도? 에 가중치를 더하는 변수
        self.start = start
        self.goal = goal

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)  # 제일 짧은 경로
        for i in range(self.n_iterations):
            all_paths, visited = self.gen_all_paths()  # 개미들이 지나온 경로와 거리 저장하는 변수
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)  # 페로몬 뿌리는 함수 호출
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:  # 이번 회차의 최단 거리가 전체 최단거리보다 짧으면 갱신
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay  # 페로몬 증발
        return visited

    # 페로몬 뿌리는 함수
    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])  # 거리 기준으로 오름차순 정렬
        for path, dist in sorted_paths[:n_best]:  # n_best 만큼의 최적의 경로를 뽑아서 반복
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]  # 지나온 경로에 페로몬 +1

    # 지나온 경로의 거리를 return하는 함수
    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    # 지나온 경로와 거리 return하는 함수
    def gen_all_paths(self):
        all_paths = []  # 경로와 거리 저장하는 리스트
        for i in range(self.n_ants):  # 개미 수 만큼 반복
            # print('ant:', i)
            path, visited = self.gen_path(self.start)  # 지나온 경로. 시작노드 설정
            all_paths.append((path, self.gen_path_dist(path)))  # 지나온 경로와 거리 저장
        return all_paths, visited

    # 지나온 경로를 return하는 함수
    def gen_path(self, start):
        path = []  # 경로 저장할 리스트
        visited = list()  # 방문한 노드 저장하는 집합
        visited.append(start)  # 시작노드 설정
        realvisited = list()  # 막다른길 에러 해결용 리스트
        realvisited.append(start)
        prev = start
        falsecount = 0
        for i in range(len(self.distances)-1):  # 거리 저장한 배열의 크기만큼 반복
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)  # 다음으로 갈 노드 선택
            if not move:
                realvisited.remove(prev)
                prev = realvisited[len(realvisited) - 1]
                path.pop()
                # print('현재노드:', prev)
                # print('falsecount:', falsecount)

            else:
                falsecount = 0
                path.append((prev, move))  # 경로에 지금 있는 노드와 다음 노드 저장
                prev = move  # 다음 노드를 현재 노드로 변경, 즉 다음경로로 이동
                visited.append(move)  # 이동한 노드를 방문한 노드에 추가
                realvisited.append(move)
                if prev == self.goal:
                    break
        return path, realvisited

    # 다음경로 계산하고 선택하는 함수
    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)  # 페로몬 배열 복사
        pheromone[list(visited)] = 0  # 지나온 경로의 페로몬을 0으로 설정: 뒤로 돌아가지 않기 위해

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)  # 페로몬을 이용해 계산한, 다음경로를 선택할 확률
        # print(row.sum())
        if row.sum() == 0:
            return False
        else:
            norm_row = row / row.sum()
            # 현재 노드에서 연결된 모든 노드중 다음으로 이동할 노드 선택 (위에서 구한 확률 이용)
            move = np_choice(self.all_inds, 1, p=norm_row)[0]
            return move

