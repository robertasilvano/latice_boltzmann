"""
    Classe Lattice
"""
import numpy as np


class Lattice:
    def __init__(self):
        # Característica do Lattice
        self.initial_vel = 2.9  # Velocidade inicial direita
        self.num_lattice_x = 400  # Número de lattices em x
        self.num_lattice_y = 100  # Número de lattices em y
        self.tau = 0.56  # Taxa de Colisão
        self.qtd_direcoes = 9  # Quantidade de direções
        self.vel_lattice_x = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
        self.vel_lattice_y = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
        self.weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])  # Distribuição das probabilidades de ir para um lado ou pro outro
        self.velocity_array = None

    def seta_velocidades_iniciais(self):
        """
        Gera um vetor de velocidades, e atribui a velocidade inicial para a terceira célula de cada Lattice.
        A terceira celula representa uma velocidade no sentido positivo de X.
        """

        lattice_ones = np.ones((self.num_lattice_y, self.num_lattice_x, self.qtd_direcoes))  # monta o lattice 100x400x9, e preenche todas as células com 1
        lattice_randoms = np.random.rand(self.num_lattice_y, self.num_lattice_x, self.qtd_direcoes)  # monta o lattice 100x400x9, e preenche todas as células com valores aleatórios
        velocity_array = lattice_ones + 0.1 * lattice_randoms  # monta o vetor de velocidades 100x400x9
        velocity_array[:, :, 3] = self.initial_vel  # seta o valor da velocidade inicial na célula 3, que representa uma velocidade no sentido positivo de x

        self.velocity_array = velocity_array
