import matplotlib                               # 데이터베이스 변경을 위해 호출
import matplotlib.pyplot as plt                 # 사용할 라이브러리
from matplotlib.widgets import Button           # 버튼 라이브러리
import matplotlib.patches as patches
import sympy as sp
import numpy as np                              # 임시 데이터 생성 및 수학 라이브러리

matplotlib.use('TkAgg')     # 기본 백엔드인 macosx는 fig.canvas.manager.window.geometry()를 지원하지 않아 TkAgg로 변경

fig01 = plt.figure(1, (12., 8.), 100)   # figure를 넘버링하여 지정(중복❎)
fig01.suptitle("matplotlib")                             # figure 별로 제목 지정 가능
fig01.canvas.manager.window.geometry("+100+100")         # 화면 상에서의 윈도우의 위치 지정
fig01.subplots_adjust(bottom=0.2)                        # 버튼을 위한 자리 마련

fig02 = plt.figure(2, (3., 8.), 100)   # figsize는 리스트([])가 아닌 튜플(())로 지정하여 warning 방지
fig02.suptitle("Sub Fig")
fig02.canvas.manager.window.geometry("+1300+100")        # 문자열 형식만 지원하는 듯

domain_size = 6

ax1 = fig01.add_subplot(231)            # 기본적인 axes
ax2 = fig01.add_subplot(234)
ax3 = fig01.add_subplot(2, 3, (2, 6))   # 여러 인접한 axes를 묶어 하나로 표현
ax3.set_xlim(0, domain_size)
ax3.set_ylim(0, domain_size)
ax3.set_aspect('equal')

# Lennard-Jones Potential
dt = 0.002
objectNum = 10
esp = 350
sig = 0.13
e = sp.symbols('e')
s = sp.symbols('s')
r = sp.symbols('r')
f = 4 * e * (sp.Pow(s/r, 12) - sp.Pow(s/r, 6))
t1 = np.arange(0.01, 1.0, 0.001)
t2 = np.arange(-1.0, -  0.01, 0.001)
f_lambdified = sp.lambdify((e, s, r), f, modules='numpy')
y = f_lambdified(esp, sig, t1)
l1, = ax1.plot(t1, y, lw=2)      # axes에 데이터를 플롯
l2, = ax2.plot(t2, y, lw=2)

ax1.set_ylim(-100, 150)
ax2.set_ylim(-100, 150)

circle = patches.Circle((0.5, 0.5), 0.03, color='blue', alpha=0.5)
ax3.add_patch(circle)
# 원의 초기 위치와 속도
circle_position = np.array([0.5, 0.5])
circle_velocity = np.array([0.0, 0.0])  # x축 방향으로 이동


class CircleObject:
    def __init__(self, ax, x, y, radius=0.03, color='blue', velocity=(0.0, 0.0)):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = radius
        self.circle = patches.Circle((x, y), radius, color=color, alpha=0.5)
        ax.add_patch(self.circle)

    def update(self, other_circles, esp, sig):
        """Lennard-Jones 퍼텐셜을 기반으로 위치 및 속도를 업데이트"""
        global f
        x, y = sp.symbols('x y')
        total_force = np.array([0.0, 0.0])

        for other in other_circles:
            if other is self:
                continue

            # 두 원 사이 거리 및 퍼텐셜 계산
            distance = np.linalg.norm(self.position - other.position)
            if distance < 1e-5:
                distance = 1e-5  # 너무 가까워지는 것을 방지

            r_sym = sp.sqrt((x - other.position[0])**2 + (y - other.position[1])**2)
            pot = f.subs([(e, esp), (s, sig), (r, r_sym)])
            force_x = -sp.diff(pot, x)
            force_y = -sp.diff(pot, y)

            fx_val = float(force_x.subs({x: self.position[0], y: self.position[1]}))
            fy_val = float(force_y.subs({x: self.position[0], y: self.position[1]}))

            total_force += np.array([fx_val, fy_val])

        # 속도와 위치 업데이트
        self.velocity += total_force * dt
        self.position += self.velocity * dt

        # 경계 조건 처리 (벽 반사)
        if self.position[0] - self.radius < 0 or self.position[0] + self.radius > 2:
            self.velocity[0] *= -1
        if self.position[1] - self.radius < 0 or self.position[1] + self.radius > 2:
            self.velocity[1] *= -1

        # 원의 새 위치 적용
        self.circle.center = self.position


# 다중 원 생성
circles = [
    CircleObject(ax3, np.random.uniform(0.2, domain_size-0.2), np.random.uniform(0.2, domain_size-0.2), color=np.random.choice(['blue', 'red', 'green']))
    for _ in range(objectNum)
]


class Index:
    def __init__(self):
        self.after_id = None  # after 이벤트의 ID를 저장

    def update_plot(self):
        global esp, sig
        ydata = f_lambdified(esp, sig, t1)
        l1.set_ydata(ydata)
        ax1.relim()  # 축 범위를 업데이트
        ax1.autoscale_view()
        ax1.legend([f"esp={esp}, sig={sig}"])
        plt.draw()

    def espup(self, event):
        global esp
        esp *= 1.1
        self.update_plot()

    def espdown(self, event):
        global esp
        esp *= 0.9
        self.update_plot()

    def sigup(self, event):
        global sig
        sig += 0.005
        self.update_plot()

    def sigdown(self, event):
        global sig
        sig -= 0.005
        self.update_plot()

    def reset(self, event):
        global circles, ax3

        # 기존 after 이벤트 취소
        if self.after_id is not None:
            fig01.canvas.manager.window.after_cancel(self.after_id)
            self.after_id = None

        # 기존 패치 삭제
        for patch in ax3.patches[:]:
            patch.remove()

        # 원 리스트 초기화
        circles = [
            CircleObject(ax3, np.random.uniform(0.2, domain_size-0.2), np.random.uniform(0.2, domain_size-0.2),
                         color=np.random.choice(['blue', 'red', 'green']))
            for _ in range(objectNum)
        ]

        # 업데이트 재시작
        self.after_id = fig01.canvas.manager.window.after(50, update_all)

    def close_fig(self, event):
        plt.close(fig01)
        plt.close(fig02)


callback = Index()


def update_all():
    """모든 원 업데이트"""
    for circle in circles:
        circle.update(circles, esp, sig)
    fig01.canvas.draw_idle()
    callback.after_id = fig01.canvas.manager.window.after(50, update_all)  # 이벤트 ID 저장


axclose = fig01.add_axes((0.81, 0.05, 0.1, 0.075))
axreset = fig01.add_axes((0.7, 0.05, 0.1, 0.075))
axsigDown = fig02.add_axes((0.05, 0.05, 0.9, 0.075))
axsigUp = fig02.add_axes((0.05, 0.135, 0.9, 0.075))
axespDown = fig02.add_axes((0.05, 0.220, 0.9, 0.075))
axespUp = fig02.add_axes((0.05, 0.305, 0.9, 0.075))

bclose = Button(axclose, 'CLOSE')
bclose.on_clicked(callback.close_fig)
breset = Button(axreset, "RESET")
breset.on_clicked(callback.reset)
bsigUp = Button(axsigUp, 'sig ⬆')
bsigUp.on_clicked(callback.sigup)
bsigDown = Button(axsigDown, 'sig ⬇')
bsigDown.on_clicked(callback.sigdown)
bespUp = Button(axespUp, 'esp ⬆')
bespUp.on_clicked(callback.espup)
bespDown = Button(axespDown, 'esp ⬇')
bespDown.on_clicked(callback.espdown)

update_all()
plt.show()      # 렌더링
