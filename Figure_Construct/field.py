import numpy as np
from config import domain_size

def calculate_field_map(circles, esp, sig, f_lambdified, grid_size=50):
    """격자 상의 장 세기 계산"""
    x = np.linspace(0, domain_size, grid_size)
    y = np.linspace(0, domain_size, grid_size)
    xv, yv = np.meshgrid(x, y)

    field_strength = np.zeros_like(xv)
    for circle in circles:
        for i in range(grid_size):
            for j in range(grid_size):
                distance = np.sqrt((xv[i, j] - circle.position[0])**2 + (yv[i, j] - circle.position[1])**2)
                if distance < sig:
                    distance = 1e-5

                field_strength[i, j] += np.abs(f_lambdified(esp, sig, distance))

    return xv, yv, field_strength