# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19a_2wy2-wYBK4nLQTmaujsPOy6vkFy08
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# Define the Ant class
class Ant:
    def __init__(self, n_cities):
        self.n_cities = n_cities
        self.tour = []
        self.visited = [False] * n_cities
        self.total_distance = 0.0

    def is_visited(self, city):
        return self.visited[city]

    def reset(self):
        self.tour = []
        self.visited = [False] * self.n_cities
        self.total_distance = 0.0

    def visit_city(self, city):
        self.tour.append(city)
        self.visited[city] = True

# Define the Ant Colony Optimization class
class ACO:
    def __init__(self, num_ants, num_iterations, alpha, beta, rho, q):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.pheromone_matrix = None


    def initialize_pheromone_matrix(self, n_cities):
        self.pheromone_matrix = np.ones((n_cities, n_cities))


    def run(self, distance_matrix):
        best_tour = []
        best_distance = float('inf')
        n_cities = len(distance_matrix)
        self.initialize_pheromone_matrix(n_cities)

        for iteration in range(self.num_iterations):
            ants = [Ant(n_cities) for i in range(self.num_ants)]

            for ant in ants:
              ant.reset()
              ant.visit_city(random.randint(0, n_cities - 1))

            for _ in range(n_cities - 1):
                for ant in ants:
                    current_city = ant.tour[-1] if ant.tour else random.randint(0, n_cities - 1)
                    next_city = self.select_next_city(ant,distance_matrix)
                    ant.visit_city(next_city)
                    ant.total_distance += distance_matrix[current_city][next_city]

            self.update_pheromone_matrix(ants, distance_matrix)

            # Update the best tour and distance
            if ants[0].total_distance < best_distance:
                best_distance = ants[0].total_distance
                best_tour = ants[0].tour.copy()

        return best_tour, best_distance



    def select_next_city(self, ant, distance_matrix):
        current_city = ant.tour[-1]
        unvisited_cities = [city for city in range(len(ant.visited)) if not ant.is_visited(city)]
        probabilities = []

        for city in unvisited_cities:
            pheromone = self.pheromone_matrix[current_city][city]
            attractiveness = 1.0 / distance_matrix[current_city][city] if distance_matrix[current_city][city] != 0 else 1e-10  # Avoid division by zero
            probability = pheromone ** self.alpha * attractiveness ** self.beta
            probabilities.append(probability)

        probabilities = np.array(probabilities)
        probabilities /= np.sum(probabilities)
        next_city = np.random.choice(unvisited_cities, p=probabilities)

        return next_city

    def update_pheromone_matrix(self, ants, distance_matrix):

      # get the evaporation Multiply it with pheromones valuse in all pheromone matrix
      evaporation = 1 - self.rho #1-p
      for i in range (len(self.pheromone_matrix)):
        for j in range (len(self.pheromone_matrix)):
          self.pheromone_matrix[i][j] *= evaporation


      # calculating delta t = Q(self initalize) / L_K = total distance taken by ant
      # then adding them to phpheromone matrix
      for ant in ants:
        for i in range(1,len(ant.tour)-1):
          from_city = ant.tour[i]
          to_city = ant.tour[i+1]
          distance = ant.total_distance
          self.pheromone_matrix[from_city][to_city] += self.q / distance
          self.pheromone_matrix[to_city][from_city] += self.q / distance


    # def update_pheromone_matrix(self, ants, distance_matrix):
    #     num_cities = len(distance_matrix)
    #     delta_pheromone = np.ones((num_cities, num_cities))

    #     for ant in ants:
    #         for i in range(num_cities - 1):
    #             city1, city2 = ant.tour[i], ant.tour[i + 1]
    #             delta_pheromone[city1][city2] += self.q / ant.total_distance

    #     self.pheromone_matrix *= (1 - self.rho)
    #     self.pheromone_matrix += delta_pheromone


    def print_pheromone_map(self, pheromone_matrix, num_cities):
      print("Pheromone Matrix:")
      for i in range(num_cities):
          for j in range(num_cities):
              if i != j:
                  print(f"Pheromone ({i}, {j}): {pheromone_matrix[i][j]:.3f}")




    def visualize_pheromone_map(self, pheromone_matrix, num_cities):
        # Create an empty graph
        G = nx.Graph()
        edge_labels = {}

        # Add edges with pheromone levels as weights
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                pheromone_value = pheromone_matrix[i][j]
                if pheromone_value > 0:
                    G.add_edge(i, j, weight=pheromone_value)
                    edge_labels[(i, j)] = f"{pheromone_value:.3f}"

        # Position the nodes in a circular layout
        pos = nx.circular_layout(G)
        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_color='purple', node_size=500)
        nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_size=12, font_color='white' , font_weight='bold')
        # Draw edge labels to show pheromone values
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        # Display the graph
        plt.title("Pheromone Map Visualization")
        plt.show()

# Function to generate a random distance matrix
def generate_distance_matrix(n_cities):
    distance_matrix = np.zeros((n_cities, n_cities))

    for i in range(n_cities):
        for j in range(i+1, n_cities):
            distance = random.uniform(3, 50)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    return distance_matrix

# Main code
num_cities = 10
num_ants_list = [1, 5, 10, 20]
num_iterations = 50
alpha = 1.0
beta = 2.0
rho = 0.5
q = 100.0

for num_ants in num_ants_list:
    distance_matrix = generate_distance_matrix(num_cities)
    aco = ACO(num_ants, num_iterations, alpha, beta, rho, q)
    best_tour, best_distance = aco.run(distance_matrix)

    if num_iterations >= 10:
        for iteration in range(10, num_iterations + 1, 10):
            aco.visualize_pheromone_map(aco.pheromone_matrix, num_cities)
            print(f"Iteration {iteration}:")
            aco.print_pheromone_map(aco.pheromone_matrix, num_cities)
            print(f"Optimal Path: {best_tour}")
            print()

print(f"Number of cites: 10")
for num_ants in num_ants_list:
    distance_matrix = generate_distance_matrix(num_cities)
    aco = ACO(num_ants, num_iterations, alpha, beta, rho, q)
    best_tour, best_distance = aco.run(distance_matrix)

    print(f"Number of ants: {num_ants}")
    print(f"Best tour: {best_tour}")
    print(f"Best distance: {best_distance}")
    print()

# Main code
num_cities = 20
num_ants_list = [1, 5, 10, 20]
num_iterations = 50
alpha = 1.0
beta = 2.0
rho = 0.5
q = 100.0

for num_ants in num_ants_list:
    distance_matrix = generate_distance_matrix(num_cities)
    aco = ACO(num_ants, num_iterations, alpha, beta, rho, q)
    best_tour, best_distance = aco.run(distance_matrix)



    if num_iterations >= 10:
        for iteration in range(10, num_iterations + 1, 10):
            aco.visualize_pheromone_map(aco.pheromone_matrix, num_cities)
            print(f"Iteration {iteration}:")
            aco.print_pheromone_map(aco.pheromone_matrix, num_cities)
            print(f"Optimal Path: {best_tour}")
            print()

print(f"Number of cites: 20")
for num_ants in num_ants_list:
    distance_matrix = generate_distance_matrix(num_cities)
    aco = ACO(num_ants, num_iterations, alpha, beta, rho, q)
    best_tour, best_distance = aco.run(distance_matrix)

    print(f"Number of ants: {num_ants}")
    print(f"Best tour: {best_tour}")
    print(f"Best distance: {best_distance}")
    print()