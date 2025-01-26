import matplotlib.pyplot as plt

def initialize_figures():
    """fig01과 fig02를 초기화하고 반환"""
    fig01 = plt.figure(1, (12., 8.), 100)
    fig01.suptitle("matplotlib")
    fig01.canvas.manager.window.geometry("+100+100")
    fig01.subplots_adjust(bottom=0.2)

    fig02 = plt.figure(2, (3., 8.), 100)
    fig02.suptitle("Sub Fig")
    fig02.canvas.manager.window.geometry("+1300+100")

    return fig01, fig02