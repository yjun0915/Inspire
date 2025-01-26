from matplotlib.widgets import Button

def create_buttons(fig01, fig02, callback):
    """버튼 생성 및 콜백 연결"""
    axclose = fig01.add_axes((0.81, 0.05, 0.1, 0.075))
    axreset = fig01.add_axes((0.7, 0.05, 0.1, 0.075))
    axsigDown = fig02.add_axes((0.05, 0.05, 0.9, 0.075))
    axsigUp = fig02.add_axes((0.05, 0.135, 0.9, 0.075))
    axespDown = fig02.add_axes((0.05, 0.220, 0.9, 0.075))
    axespUp = fig02.add_axes((0.05, 0.305, 0.9, 0.075))

    Button(axclose, 'CLOSE').on_clicked(callback.close_fig)
    Button(axreset, 'RESET').on_clicked(callback.reset)
    Button(axsigUp, 'sig ⬆').on_clicked(callback.sigup)
    Button(axsigDown, 'sig ⬇').on_clicked(callback.sigdown)
    Button(axespUp, 'esp ⬆').on_clicked(callback.espup)
    Button(axespDown, 'esp ⬇').on_clicked(callback.espdown)