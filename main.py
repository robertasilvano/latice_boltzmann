"""
    Método de Simulação de Escoamento
    de Fluidos Lattice Boltzmann
"""

from lattice import Lattice
from solid_bodies import SolidBody
from simulation import Simulation

ITERATIONS = 10000
RADIUS = 13
SOLID_X_POS = 50
SOLID_Y_POS = 50
SOLID_BODY = 'P'


def main(iterations):
    # Instancia o Lattice
    lattice = Lattice()

    # Define o array de velocidades iniciais
    lattice.seta_velocidades_iniciais()

    # Perfil do Sólido
    solid_body = SolidBody().monta_solid_body(num_lattice_x=lattice.num_lattice_x, num_lattice_y=lattice.num_lattice_y,
                                              radius=RADIUS, solid_x_pos=SOLID_X_POS, solid_y_pos=SOLID_Y_POS,
                                              SOLID_BODY=SOLID_BODY)

    # Simulação
    Simulation().simulate(iterations=iterations,
                          dir_lattice_x=lattice.dir_lattice_x, dir_lattice_y=lattice.dir_lattice_y,
                          f_in=lattice.f_in, qtd_direcoes=lattice.qtd_direcoes,
                          weights=lattice.weights, omega=lattice.omega, solid_body=solid_body,
                          initial_vel=lattice.initial_vel)


if __name__ == '__main__':
    main(iterations=ITERATIONS)

