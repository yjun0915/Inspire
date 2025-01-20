import matplotlib                               # 데이터베이스 변경을 위해 호출
import matplotlib.pyplot as plt                 # 사용할 라이브러리
from matplotlib.widgets import Button           # 버튼 라이브러리
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

freqs = np.arange(2, 20, 3)
t = np.arange(0.0, 1.0, 0.001)
s = np.sin(2*np.pi*freqs[0]*t)
l, = ax1.plot(t, s, lw=2)      # axes에 데이터를 플롯


class Index:
    ind = 0

    def next(self, event):
        self.ind += 1
        i = self.ind % len(freqs)
        ydata = np.sin(2*np.pi*freqs[i]*t)
        l.set_ydata(ydata)
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(freqs)
        ydata = np.sin(2*np.pi*freqs[i]*t)
        l.set_ydata(ydata)
        plt.draw()


callback = Index()
axprev = fig01.add_axes((0.7, 0.05, 0.1, 0.075))
axnext = fig01.add_axes((0.81, 0.05, 0.1, 0.075))
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()      # 렌더링
