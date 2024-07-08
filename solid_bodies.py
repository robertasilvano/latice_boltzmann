import numpy as np


class SolidBody:
    @classmethod
    def monta_solid_body(cls, num_lattice_x, num_lattice_y, radius, solid_x_pos, solid_y_pos, SOLID_BODY):
        '''
        Monta o array do solid body, neste caso um cilindro
        '''
        solid_body = np.full((num_lattice_y, num_lattice_x), False)  # monta o array 100x400, com todas as células preenchidas com False, ou seja, o corpo sólido ainda não está presente
        if SOLID_BODY == 'C':
            solid_body = cls.check_collision_cylinder(num_lattice_x, num_lattice_y, radius, solid_x_pos, solid_y_pos, solid_body)  # monta o corpo sólido do cilindro
        elif SOLID_BODY == 'P':
            solid_body = cls.check_collision_plate(num_lattice_x, num_lattice_y, solid_x_pos, solid_y_pos, solid_body)  # monta o corpo sólido da placa
        return solid_body

    @classmethod
    def check_collision_cylinder(cls, num_lattice_x, num_lattice_y, radius, solid_x_pos, solid_y_pos, solid_body):
        '''
        Calcula quais células pertencem ao sólido e devem ser marcadas como True
        Define a região com o formato do sólido, onde a colisão não será calculada, considera as colisões para fora do raio específicado.
        Pega o array montado anteriormente com todas as células preenchidas com False, e preenche com True, representando onde o sólido está.
        '''
        for celula_y in range(0, num_lattice_y):
            for celula_x in range(0, num_lattice_x):
                if cls.distance_btwn_two_points(solid_x_pos, solid_y_pos, celula_x, celula_y) < radius:  # Se a distância entre a célula atual até o centro do sólido for menor que o raio, faz parte do sólido
                    solid_body[celula_y][celula_x] = True

        return solid_body

    @classmethod
    def distance_btwn_two_points(cls, solid_x_pos, solid_y_pos, celula_x, celula_y):
        '''
        Calcula a distância euclediana entre a célula atual e o ponto central do sólido
        '''
        return np.sqrt((celula_x-solid_x_pos)**2 + (celula_y-solid_y_pos)**2)

    @classmethod
    def check_collision_plate(cls, num_lattice_x, num_lattice_y, solid_x_pos, solid_y_pos, solid_body):
        '''
        Calcula quais células pertencem ao sólido e devem ser marcadas como True
        Define a região com o formato do sólido, onde a colisão não será calculada, considera as colisões para fora do solido específicado.
        Pega o array montado anteriormente com todas as células preenchidas com False, e preenche com True, representando onde o sólido está.
        '''
        for celula_y in range(0, num_lattice_y):
            for celula_x in range(0, num_lattice_x):
                if celula_x == solid_x_pos:
                    if solid_y_pos - 5 <= celula_y <= solid_y_pos + 5:
                        solid_body[celula_y][celula_x] = True
        return solid_body