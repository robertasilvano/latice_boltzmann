import numpy as np
from matplotlib import pyplot

plot_rate = 50


class Simulation:
    @classmethod
    def calc_density(cls, velocity_array):
        return np.sum(velocity_array, 2)

    @classmethod
    def calc_momentum(cls, velocity_array, vel_x, vel_y, rho):
        momentum_x = np.sum(velocity_array*vel_x, 2)/rho
        momentum_y = np.sum(velocity_array*vel_y, 2)/rho

        return momentum_x, momentum_y

    @classmethod
    def calculate_colision(cls, velocity_array, vel_x, vel_y, weights, num_lattices, rho,
                           momentum_x, momentun_y, tau):
        # Estado de quilibrio do vetor de velocidades
        velocity_array_eq = np.zeros(velocity_array.shape)
        for i, vx, vy, weight in zip(range(num_lattices), vel_x, vel_y, weights):
            velocity_array_eq[:, :, i] = rho * weight * (1 + 3 * (vx*momentum_x + vy*momentun_y) + 9 * (vx*momentum_x + vy*momentun_y)**2/2 - 3 * (momentum_x**2 + momentun_y**2)/2)
        new_velocity_array = velocity_array + -(1/tau) * (velocity_array - velocity_array_eq)

        return new_velocity_array

    @classmethod
    def plot_simulation(cls, iteration, momentum_x, momentum_y):
        if iteration % plot_rate == 0:
            pyplot.imshow(np.sqrt(momentum_x**2 + momentum_y**2))
            pyplot.pause(0.01)
            pyplot.cla()

    @classmethod
    def simulate(cls, iterations, vel_lattice_x, vel_lattice_y, velocity_array, qtd_direcoes, weights, tau, solid_body):
        # Printando iteração atual
        for iteration in range(iterations):
            print(f'Iteration {iteration} out of {iterations}')

            # Alterando o valor de velocidade de cada célula dos n Lattices, shiftando os valores de velocidade
            for direcao, vx, vy in zip(range(qtd_direcoes), vel_lattice_x, vel_lattice_y):
                velocity_array[:, :, direcao] = np.roll(velocity_array[:, :, direcao], vx, axis=1)
                velocity_array[:, :, direcao] = np.roll(velocity_array[:, :, direcao], vy, axis=0)

            # Checando pontos de colisão com o corpo sólido para alterar a direção da velocidade
            sd_boundry = velocity_array[solid_body, :]
            sd_boundry = sd_boundry[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]  # números das células opostas

            # Calculando variáveis do fluido (densidade e momento)
            rho = cls.calc_density(velocity_array)
            momentum_x, momentum_y = cls.calc_momentum(velocity_array, vel_lattice_x, vel_lattice_y, rho)

            # Zerando velocidade do fluido no interior do corpo sólido
            velocity_array[solid_body, :] = sd_boundry
            momentum_x[solid_body] = 0
            momentum_y[solid_body] = 0

            velocity_array = cls.calculate_colision(velocity_array, vel_lattice_x, vel_lattice_y, weights, qtd_direcoes,
                                                    rho, momentum_x, momentum_y, tau)

            cls.plot_simulation(iteration, momentum_x, momentum_y)
