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
        self.tau = 0.56  # Taxa de Colisão (relaxation time)
        self.omega = 1/self.tau  # Parametro de relaxamento
        self.qtd_direcoes = 9  # Quantidade de direções
        self.dir_lattice_x = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])  # ficar no lugar, pra cima, e em sentido horário
        self.dir_lattice_y = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
        self.weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])  # Distribuição das probabilidades de ir para um lado ou pro outro, onde a probabilidade é menor pra onde é mais fácil se mover. 0.44, 0.11, 0.027, 0.11, 0.027, 0.11, 0.027, 0.11, 0.027
        self.f_in = None

    def seta_velocidades_iniciais(self):
        """
        Gera um vetor de velocidades, e atribui a velocidade inicial para a terceira célula de cada Lattice.
        A terceira celula representa uma velocidade no sentido positivo de X.
        """

        lattice_ones = np.ones((self.num_lattice_y, self.num_lattice_x, self.qtd_direcoes))  # monta o lattice 100x400x9, e preenche todas as células com 1
        lattice_randoms = np.random.rand(self.num_lattice_y, self.num_lattice_x, self.qtd_direcoes)  # monta o lattice 100x400x9, e preenche todas as células com valores aleatórios
        f_in = lattice_ones + 0.1 * lattice_randoms  # monta o vetor de velocidades 100x400x9
        f_in[:, :, 3] = self.initial_vel  # seta o valor da velocidade inicial na célula 3, que representa uma velocidade no sentido positivo de x

        self.f_in = f_in
