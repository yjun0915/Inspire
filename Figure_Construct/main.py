import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from config import domain_size, esp, sig, objectNum
from figures import initialize_figures
from circle import CircleObject
from field import calculate_field_map
from buttons import create_buttons

# Lennard-Jones Potential 설정
e, s, r = sp.symbols('e s r')
f = 4 * e * (sp.Pow(s/r, 12) - sp.Pow(s/r, 6))
f_lambdified = sp.lambdify((e, s, r), f, modules='numpy')

# Figure 초기화
fig01, fig02 = initialize_figures()
ax1 = fig01.add_subplot(231)
ax2 = fig01.add_subplot(234)
ax3 = fig01.add_subplot(2, 3, (2, 6))
ax3.set_xlim(0, domain_size)
ax3.set_ylim(0, domain_size)
ax3.set_aspect('equal')

# 원 초기화
circles = [
    CircleObject(ax3, np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9), color=np.random.choice(['blue', 'red', 'green']))
    for _ in range(objectNum)
]

# 콜백 클래스 정의 및 버튼 생성
class Index:
    def reset(self, event):
        pass  # 실제 구현 추가
    def close_fig(self, event):
        plt.close(fig01)
        plt.close(fig02)

callback = Index()
create_buttons(fig01, fig02, callback)

# 프로그램 실행
plt.show()