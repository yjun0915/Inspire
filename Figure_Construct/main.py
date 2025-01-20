import matplotlib                               # 데이터베이스 변경을 위해 호출
import matplotlib.pyplot as plt                 # 사용할 라이브러리

matplotlib.use('TkAgg')     # 기본 백엔드인 macosx는 fig.canvas.manager.window.geometry()를 지원하지 않아 TkAgg로 변경

fig01 = plt.figure(1, (12., 8.), 100)   # figure를 넘버링하여 지정(중복❎)
fig01.suptitle("matplotlib")                            # figure 별로 제목 지정 가능
fig01.canvas.manager.window.geometry("+100+100")        # 화면 상에서의 윈도우의 위치 지정

fig02 = plt.figure(2, (3., 4.), 100)   # figsize는 리스트([])가 아닌 튜플(())로 지정하여 warning 방지
fig02.suptitle("Sub Fig")
fig02.canvas.manager.window.geometry("+1300+400")        # 문자열 형식만 지원하는 듯

ax1 = fig01.add_subplot(231)        # 기본적인 axes
ax2 = fig01.add_subplot(234)
ax3 = fig01.add_subplot(2, 3, (2, 6))   # 여러 인접한 axes를 묶어 하나로 표현

ax1.plot([1, 2, 3, 4])      # axes에 데이터를 플롯

plt.show()      # 렌더링
