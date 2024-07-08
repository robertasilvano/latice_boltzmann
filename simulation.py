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
    def calc_velocidade(cls, f_in, vel_x, vel_y, rho):
        '''
        Calcula a velocidade do fluido em cada direção
        '''
        velocity_x = np.sum(f_in * vel_x, 2) / rho
        velocity_y = np.sum(f_in * vel_y, 2) / rho

        return velocity_x, velocity_y

    @classmethod
    def calculate_colision(cls, f_in, vel_x, vel_y, weights, num_lattices, rho,
                           velocity_x, velocity_y, omega):
        '''
        Calcula a colisão, retornando a nova matriz de velocidade
        '''
        # Estado de equilibrio do vetor de velocidades
        f_in_eq = np.zeros(f_in.shape)
        for i, vx, vy, weight in zip(range(num_lattices), vel_x, vel_y, weights):
            f_in_eq[:, :, i] = rho * weight * (1 + 3 * (vx * velocity_x + vy * velocity_y) + 9 * (vx * velocity_x + vy * velocity_y) ** 2 / 2 - 3 * (velocity_x ** 2 + velocity_y ** 2) / 2)
        f_out = f_in + - omega * (f_in - f_in_eq)

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
    def simulate(cls, iterations, vel_lattice_x, vel_lattice_y, f_in, qtd_direcoes, weights, omega, solid_body):
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

            # Alterando o valor de velocidade de cada célula dos n Lattices, shiftando os valores de velocidade
            for direcao, vx, vy in zip(range(qtd_direcoes), vel_lattice_x, vel_lattice_y):
                f_in[:, :, direcao] = np.roll(f_in[:, :, direcao], vx, axis=1)
                f_in[:, :, direcao] = np.roll(f_in[:, :, direcao], vy, axis=0)

            # Checando pontos de colisão com o corpo sólido para alterar a direção da velocidade
            sd_boundry = f_in[solid_body, :]
            sd_boundry = sd_boundry[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]  # números das células opostas. invertendo direção das particulas que colidiram.

            # Calculando variáveis do fluido (densidade e velocidade)
            rho = cls.calc_density(f_in)
            velocity_x, velocity_y = cls.calc_velocidade(f_in, vel_lattice_x, vel_lattice_y, rho)

            # Zerando velocidade do fluido no interior do corpo sólido
            f_in[solid_body, :] = sd_boundry
            velocity_x[solid_body] = 0
            velocity_y[solid_body] = 0

            f_in = cls.calculate_colision(f_in, vel_lattice_x, vel_lattice_y, weights, qtd_direcoes,
                                          rho, velocity_x, velocity_y, omega)

            cls.plot_simulation(iteration, velocity_x, velocity_y)
