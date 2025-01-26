import numpy as np
import matplotlib.patches as patches
from config import domain_size, dt

class CircleObject:
    def __init__(self, ax, x, y, radius=0.03, color='blue', velocity=(0.0, 0.0)):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = radius
        self.circle = patches.Circle((x, y), radius, color=color, alpha=0.5)
        ax.add_patch(self.circle)

    def calculate_force(self, other_circles, esp, sig, f_lambdified):
        """다른 원자들과의 상호작용으로 힘을 계산"""
        total_force = np.array([0.0, 0.0])

        for other in other_circles:
            if other is self:
                continue

            distance = np.linalg.norm(self.position - other.position)
            if distance < sig:
                distance = 1e-5

            force_magnitude = f_lambdified(esp, sig, distance)
            direction = (other.position - self.position) / distance
            total_force += force_magnitude * direction

        return total_force

    def update_position(self, force):
        """힘을 기반으로 속도와 위치를 업데이트"""
        self.velocity += force * dt
        self.position += self.velocity * dt

        # 경계 조건 처리 (벽 반사)
        if self.position[0] - self.radius < 0 or self.position[0] + self.radius > domain_size:
            self.velocity[0] *= -1
        if self.position[1] - self.radius < 0 or self.position[1] + self.radius > domain_size:
            self.velocity[1] *= -1

        # 원의 새 위치 적용
        self.circle.center = self.position