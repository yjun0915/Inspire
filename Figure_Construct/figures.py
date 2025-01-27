import matplotlib
import matplotlib.pyplot as plt

# 백엔드를 TkAgg로 변경
matplotlib.use("TkAgg")

def initialize_figures():
    """fig01과 fig02를 초기화하고 반환"""
    fig01 = plt.figure(1, (12., 8.), 100)
    fig01.suptitle("matplotlib")
    fig01.canvas.manager.window.geometry("+100+100")  # 위치 설정 가능

    fig02 = plt.figure(2, (3., 8.), 100)
    fig02.suptitle("Sub Fig")
    fig02.canvas.manager.window.geometry("+1300+100")  # 위치 설정 가능

    return fig01, fig02