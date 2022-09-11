import Classs_GUI
from time import sleep

TotalV = 10

for i in range(20):
    a = Classs_GUI.one_line_progress_meter_PJJ('Demo', i, TotalV, f'{i} / {TotalV}',key='DemoShow')
    sleep(0.5)
    if a == 'finished':
        Classs_GUI.one_line_progress_meter_cancel_pjj(key='DemoShow')
        sleep(1)
        break