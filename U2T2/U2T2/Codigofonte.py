import numpy as np
import time
from scipy.stats import t
import matplotlib.pyplot as plt

# Classes e funções auxiliares para BST
class Node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

class BST:
    def __init__(self):
        self.root = None

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._add_recursive(self.root, value)

    def _add_recursive(self, current_node, value):
        if value <= current_node.value:
            if current_node.left_child is None:
                current_node.left_child = Node(value)
            else:
                self._add_recursive(current_node.left_child, value)
        else:
            if current_node.right_child is None:
                current_node.right_child = Node(value)
            else:
                self._add_recursive(current_node.right_child, value)

# Função solver_closest
def solver_closest(tree, target):
    def findClosestValueInBstHelper(node, target, closest):
        if node is None:
            return closest
        if abs(target - closest) > abs(target - node.value):
            closest = node.value
        if target < node.value:
            return findClosestValueInBstHelper(node.left_child, target, closest)
        elif target > node.value:
            return findClosestValueInBstHelper(node.right_child, target, closest)
        else:
            return closest

    return findClosestValueInBstHelper(tree.root, target, tree.root.value)

# Função solver_kth_largest
def solver_kth_largest(tree, k):
    sortedNodeValues = []

    def inOrderTraverse(node):
        if node is None:
            return
        inOrderTraverse(node.left_child)
        sortedNodeValues.append(node.value)
        inOrderTraverse(node.right_child)

    inOrderTraverse(tree.root)
    return sortedNodeValues[-k]

# Função para medir o tempo de execução
def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result

# Função para executar experimentos solver_closest
def run_experiments_closest(max_size=10**6, step=10**5, repetitions=15):
    np.random.seed(42)
    sizes = range(step, max_size + 1, step)
    results = {"sizes": [], "avg_time": [], "conf_interval": []}

    for size in sizes:
        times = []

        for _ in range(repetitions):
            arr = np.random.randint(0, 1000000, size=size)
            bst = BST()
            for value in arr:
                bst.add(value)

            target = np.random.randint(0, 1000000)
            time_taken, _ = measure_execution_time(solver_closest, bst, target)
            times.append(time_taken)

        mean_time = np.mean(times)
        conf_interval = t.interval(0.95, len(times) - 1, loc=mean_time, scale=np.std(times, ddof=1))

        results["sizes"].append(size)
        results["avg_time"].append(mean_time)
        results["conf_interval"].append((conf_interval[1] - mean_time))

    return results

# Função para executar experimentos solver_kth_largest
def run_experiments_kth_largest(max_size=10**6, step=10**5, repetitions=15):
    np.random.seed(42)
    sizes = range(step, max_size + 1, step)
    results = {"sizes": [], "avg_time": [], "conf_interval": []}

    for size in sizes:
        times = []

        for _ in range(repetitions):
            arr = np.random.randint(0, 1000000, size=size)
            bst = BST()
            for value in arr:
                bst.add(value)

            k = size // 2
            time_taken, _ = measure_execution_time(solver_kth_largest, bst, k)
            times.append(time_taken)

        mean_time = np.mean(times)
        conf_interval = t.interval(0.95, len(times) - 1, loc=mean_time, scale=np.std(times, ddof=1))

        results["sizes"].append(size)
        results["avg_time"].append(mean_time)
        results["conf_interval"].append((conf_interval[1] - mean_time))

    return results

# Função para gerar gráficos em segundos
def plot_results(results, title, xlabel="Tamanho do vetor", ylabel="Tempo médio de execução (s)"):
    plt.figure(figsize=(12, 6))
    plt.errorbar(results["sizes"], results["avg_time"], yerr=results["conf_interval"], fmt='o', capsize=5, label="Média com IC")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

# Função principal
def main():
    max_size = 10**6
    step = 10**5
    repetitions = 10

    print("Executando experimentos para Solver Closest...")
    results_closest = run_experiments_closest(max_size=max_size, step=step, repetitions=repetitions)
    plot_results(results_closest, title="Desempenho do Solver Closest")

    print("Executando experimentos para Solver Kth Largest...")
    results_kth_largest = run_experiments_kth_largest(max_size=max_size, step=step, repetitions=repetitions)
    plot_results(results_kth_largest, title="Desempenho do Solver Kth Largest")

if __name__ == "__main__":
    main()
