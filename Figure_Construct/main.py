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

ax1 = fig01.add_subplot(231)            # 기본적인 axes
ax2 = fig01.add_subplot(234)
ax3 = fig01.add_subplot(2, 3, (2, 6))   # 여러 인접한 axes를 묶어 하나로 표현
ax3.set_xlim(0, 2)
ax3.set_ylim(0, 2)
ax3.set_aspect('equal')

# Lennard-Jones Potential
dt = 0.02
esp = 35
sig = 0.02
e = sp.symbols('e')
s = sp.symbols('s')
r = sp.symbols('r')
f = 4 * e * (sp.Pow(s/r, 12) - sp.Pow(s/r, 6))
t = np.arange(0.01, 1.0, 0.001)
f_lambdified = sp.lambdify((e, s, r), f, modules='numpy')
y = f_lambdified(esp, sig, t)
l, = ax1.plot(t, y, lw=2)      # axes에 데이터를 플롯
ax1.set_ylim(-100, 150)

circle = patches.Circle((0.5, 0.5), 0.03, color='blue', alpha=0.5)
ax3.add_patch(circle)
# 원의 초기 위치와 속도
circle_position = np.array([0.5, 0.5])
circle_velocity = np.array([0.0, 0.0])  # x축 방향으로 이동


def update_circle():
    m = 300
    global circle_position, circle_velocity, f, esp, sig

    # 원의 위치 업데이트
    pot = f.subs([(e, esp), (s, sig)])
    force = -sp.diff(pot, r)
    circle_velocity[0] += force.subs(r, circle_position[0])*dt/m
    circle_position += circle_velocity*dt
    if circle_position[0] > 2.0 or circle_position[0] < 0.0:  # x축 경계 반사
        circle_velocity[0] *= -1
    if circle_position[1] > 2.0 or circle_position[1] < 0.0:  # y축 경계 반사
        circle_velocity[1] *= -1

    # 원의 새 위치 적용
    circle.center = circle_position
    fig01.canvas.draw_idle()  # 화면 업데이트

    # 50ms 후 다시 호출
    fig01.canvas.manager.window.after(50, update_circle)


class Index:

    def update_plot(self):
        global esp, sig
        ydata = f_lambdified(esp, sig, t)
        l.set_ydata(ydata)
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

    def close_fig(self, event):
        plt.close(fig01)
        plt.close(fig02)


callback = Index()

axclose = fig01.add_axes((0.81, 0.05, 0.1, 0.075))
axsigDown = fig02.add_axes((0.05, 0.05, 0.9, 0.075))
axsigUp = fig02.add_axes((0.05, 0.135, 0.9, 0.075))
axespDown = fig02.add_axes((0.05, 0.220, 0.9, 0.075))
axespUp = fig02.add_axes((0.05, 0.305, 0.9, 0.075))

bclose = Button(axclose, 'CLOSE')
bclose.on_clicked(callback.close_fig)
bsigUp = Button(axsigUp, 'sig ⬆')
bsigUp.on_clicked(callback.sigup)
bsigDown = Button(axsigDown, 'sig ⬇')
bsigDown.on_clicked(callback.sigdown)
bespUp = Button(axespUp, 'esp ⬆')
bespUp.on_clicked(callback.espup)
bespDown = Button(axespDown, 'esp ⬇')
bespDown.on_clicked(callback.espdown)

update_circle()
plt.show()      # 렌더링
