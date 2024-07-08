import numpy as np
from matplotlib import pyplot

plot_rate = 50


class Simulation:
    @classmethod
    def calc_density(cls, f_in):
        '''
        Calcula a densidade do fluido em cada célula da grade, somando as componentes de velocidade ao longo da direção 2
        '''
        return np.sum(f_in, 2)

    @classmethod
    def calc_velocidade(cls, f_in, dir_x, dir_y, rho):
        '''
        Calcula a velocidade do fluido em cada direção
        '''
        velocity_x = np.sum(f_in * dir_x, 2) / rho
        velocity_y = np.sum(f_in * dir_y, 2) / rho

        return velocity_x, velocity_y

    @classmethod
    def calculate_eq(cls, f_in, dir_x, dir_y, weights, qtd_direcoes, rho, velocity_x, velocity_y):
        '''
        Define a função de distribuição de equilibrio, por expansão de série de taylor
        '''
        f_in_eq = np.zeros(f_in.shape)
        for direcao, dir_x, dir_y, weight in zip(range(qtd_direcoes), dir_x, dir_y, weights):
            c = (dir_x * velocity_x + dir_y * velocity_y)
            f_in_eq[:, :, direcao] = rho * weight * (1 + 3 * c + 9 * c ** 2 / 2 - 3 * (velocity_x ** 2 + velocity_y ** 2) / 2)
        return f_in_eq

    @classmethod
    def calculate_colision(cls, f_in, f_in_eq, omega):
        '''
        Calcula a colisão, retornando a nova matriz de velocidade
        '''
        f_out = f_in - omega * (f_in - f_in_eq)

        return f_out

    @classmethod
    def plot_simulation(cls, iteration, velocity_x, velocity_y):
        '''
        Plota a simulação
        Se o número da iteração for multiplo de plot_rate, mostra a imagem da magnitude do vetor de velocidade
        '''
        if iteration % plot_rate == 0:
            pyplot.imshow(np.sqrt(velocity_x ** 2 + velocity_y ** 2))
            pyplot.pause(0.01)
            pyplot.cla()

    @classmethod
    def simulate(cls, iterations, dir_lattice_x, dir_lattice_y, f_in, qtd_direcoes, weights, omega, solid_body, initial_vel):
        '''
        Executa a simulação pelo método de lattice boltzmann.
        Para cada iteração executa os seguintes passos:
            - desloca os valores de velocidade em cada direção do lattice
            - ajusta as células que estão na borda do corpo solido
            - calcula a densidade e velocidade do fluido
            - zera a velocidade e velocidade dentro do corpo sólido
            - calcula a colisão
            - plota
        '''

        # Printando iteração atual
        for iteration in range(iterations):
            print(f'Iteration {iteration} out of {iterations}')

            # Ajustando parede da direita
            f_in[:, -1, [6, 7, 8]] = f_in[:, -2, [6, 7, 8]]  # linha (y), coluna (x), direção

            # Calculando variáveis do fluido (densidade e velocidade)
            rho = cls.calc_density(f_in)
            velocity_x, velocity_y = cls.calc_velocidade(f_in, dir_lattice_x, dir_lattice_y, rho)

            # # Ajustando parede da esquerda
            velocity_x[:, 0] = 0
            velocity_y[:, 0] = 0
            # rho[:, 0] = np.sum(f_in[:, 0, [1, 0, 5]], 1) + 2*np.sum(f_in[:, 0, [8, 7, 6]], 1)/(1-velocity_x[:, 0])

            # Calcula a função de equilibrio
            f_in_eq = cls.calculate_eq(f_in, dir_lattice_x, dir_lattice_y, weights, qtd_direcoes, rho, velocity_x, velocity_y, )
            f_in[:, 0, [2, 3, 4]] = f_in_eq[:, 0, [2, 3, 4]] + f_in[:, 0, [6, 7, 8]] - f_in_eq[:, 0, [6, 7, 8]]

            # Calcula o passo de colisão
            f_in = cls.calculate_colision(f_in, f_in_eq, omega)

            # Checando pontos de colisão com o corpo sólido para alterar a direção da velocidade
            sd_boundry = f_in[solid_body, :]
            sd_boundry = sd_boundry[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]  # números das células opostas. invertendo direção das particulas que colidiram.

            # Zerando velocidade do fluido no interior do corpo sólido
            f_in[solid_body, :] = sd_boundry
            velocity_x[solid_body] = 0
            velocity_y[solid_body] = 0

            # Alterando o valor de velocidade de cada célula dos n Lattices, shiftando os valores de velocidade
            for direcao, dir_x, dir_y in zip(range(qtd_direcoes), dir_lattice_x, dir_lattice_y):
                f_in[:, :, direcao] = np.roll(f_in[:, :, direcao], dir_x, axis=1)
                f_in[:, :, direcao] = np.roll(f_in[:, :, direcao], dir_y, axis=0)

            cls.plot_simulation(iteration, velocity_x, velocity_y)
