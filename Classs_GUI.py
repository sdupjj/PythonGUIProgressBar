import PySimpleGUI as sg
from time import sleep

sg.theme('LightBrown1')

class GUI_ProgressBar():
    def __init__(self):
        self.GUIWindowName = 'ProgressBar'
        self.layout =  [[sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress')]]
        self.window = sg.Window(self.GUIWindowName, self.layout)
    def run(self):
        while True:             # Event Loop
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, 'Exit'):
                break
            progress_bar.update_bar(G.downloaded)
        self.window.close()

class QuickMeter_PJJ(object):
    active_meters = {}
    exit_reasons = {}

    def __init__(self, title, current_value, max_value, key, *args, orientation='h', bar_color=(None, None), button_color=(None, None),
                 size=(50,50), border_width=None, grab_anywhere=False, no_titlebar=False, keep_on_top=None, no_button=False):
        """

        :param title:         text to display in element
        :type title:          (str)
        :param current_value: current value
        :type current_value:  (int)
        :param max_value:     max value of QuickMeter
        :type max_value:      (int)
        :param key:           Used with window.find_element and with return values to uniquely identify this element
        :type key:            str | int | tuple | object
        :param *args:         stuff to output
        :type *args:          (Any)
        :param orientation:   'horizontal' or 'vertical' ('h' or 'v' work) (Default value = 'vertical' / 'v')
        :type orientation:    (str)
        :param bar_color:     color of a bar line
        :type bar_color:      (str, str)
        :param button_color:  button color (foreground, background)
        :type button_color:   (str, str) or str
        :param size:          (w,h) w=characters-wide, h=rows-high (Default value = DEFAULT_PROGRESS_BAR_SIZE)
        :type size:           (int, int)
        :param border_width:  width of border around element
        :type border_width:   (int)
        :param grab_anywhere: If True: can grab anywhere to move the window (Default = False)
        :type grab_anywhere:  (bool)
        :param no_titlebar:   If True: window will be created without a titlebar
        :type no_titlebar:    (bool)
        :param keep_on_top:   If True the window will remain above all current windows
        :type keep_on_top:    (bool)
        :param no_button:     If True: window will be created without a cancel button
        :type no_button:      (bool)
        """
        self.key = key
        self.orientation = orientation
        self.bar_color = bar_color
        self.size = size
        self.grab_anywhere = grab_anywhere
        self.button_color = button_color
        self.border_width = border_width
        self.no_titlebar = no_titlebar
        self.title = title
        self.current_value = current_value
        self.max_value = max_value
        self.close_reason = None
        self.keep_on_top = keep_on_top
        self.no_button = no_button
        self.window = self.BuildWindow(*args)

    def BuildWindow(self, *args):
        layout = []
        col = []
        col += [[sg.T(''.join(map(lambda x: str(x) + '\n', args)),key='-OPTMSG-')]]  ### convert all *args into one string that can be updated
        col += [[sg.ProgressBar(max_value=self.max_value, orientation='h', key='-PROG-', size=self.size, bar_color=self.bar_color)]]
        #col += [[sg.Cancel(button_color=self.button_color)]]
        layout = [sg.Column(col,element_justification='c')]

        self.window = sg.Window(self.title, grab_anywhere=self.grab_anywhere, border_depth=self.border_width, no_titlebar=self.no_titlebar, disable_close=True, keep_on_top=self.keep_on_top)
        self.window.Layout([layout]).Finalize()

        return self.window

    def UpdateMeter(self, current_value, max_value, *args):  ### support for *args when updating
        METER_OK = True
        METER_STOPPED = False

        self.current_value = current_value
        self.max_value = max_value
        self.window.Element('-PROG-').UpdateBar(self.current_value, self.max_value)
        self.window.Element('-OPTMSG-').Update(value=''.join(map(lambda x: str(x) + '\n', args)))  ###  update the string with the args
        event, values = self.window.read(timeout=0)
        #print(event)
        #exit_reason 可能的结果 'finished'，'running'
        if current_value == max_value:
            exit_reason = 'finished'
            #print(f'exit_reason : {exit_reason}')
            #self.window.close()
            #del (QuickMeter_PJJ.active_meters[self.key])
            #QuickMeter_PJJ.exit_reasons[self.key] = exit_reason
        elif current_value > max_value:
            exit_reason = 'overloaded'
        else:
            exit_reason = 'running'
        QuickMeter_PJJ.exit_reasons[self.key] = exit_reason
        return exit_reason

def one_line_progress_meter_PJJ(title, current_value, max_value, *args, key='OK for 1 meter', orientation='h', bar_color=(None, None), button_color=None, size=(32,10), border_width=None, grab_anywhere=False, no_titlebar=False, keep_on_top=None, no_button=False):
    '''
    METER_REASON_CANCELLED = 'cancelled'
    METER_REASON_CLOSED = 'closed'
    METER_REASON_REACHED_MAX = 'finished'
    METER_OK = True
    METER_STOPPED = False
    '''

    """
    :param title:         text to display in eleemnt
    :type title:          (str)
    :param current_value: current value
    :type current_value:  (int)
    :param max_value:     max value of QuickMeter
    :type max_value:      (int)
    :param *args:         stuff to output
    :type *args:          (Any)
    :param key:           Used to differentiate between mutliple meters. Used to cancel meter early. Now optional as there is a default value for single meters
    :type key:            str | int | tuple | object
    :param orientation:   'horizontal' or 'vertical' ('h' or 'v' work) (Default value = 'vertical' / 'v')
    :type orientation:    (str)
    :param bar_color:     color of a bar line
    :type bar_color:      Tuple(str, str)
    :param button_color:  button color (foreground, background)
    :type button_color:   (str, str) or str
    :param size:          (w,h) w=characters-wide, h=rows-high (Default value = DEFAULT_PROGRESS_BAR_SIZE)
    :type size:           (int, int)
    :param border_width:  width of border around element
    :type border_width:   (int)
    :param grab_anywhere: If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:  (bool)
    :param no_titlebar:   If True: no titlebar will be shown on the window
    :type no_titlebar:    (bool)
    :param keep_on_top:   If True the window will remain above all current windows
    :type keep_on_top:    (bool)
    :param no_button:     If True: window will be created without a cancel button
    :type no_button:      (bool)
    :return:              True if updated successfully. False if user closed the meter with the X or Cancel button
    :rtype:               (bool)
    """
    if key not in QuickMeter_PJJ.active_meters:
        meter = QuickMeter_PJJ(title, current_value, max_value, key, *args, orientation=orientation, bar_color=bar_color, button_color=button_color, size=size, border_width=border_width, grab_anywhere=grab_anywhere, no_titlebar=no_titlebar, keep_on_top=keep_on_top, no_button=no_button)
        QuickMeter_PJJ.active_meters[key] = meter
        QuickMeter_PJJ.exit_reasons[key] = 'running'
    else:
        meter = QuickMeter_PJJ.active_meters[key]

    rc = meter.UpdateMeter(current_value, max_value, *args)  ### pass the *args to to UpdateMeter function
    # one_line_progress_meter_PJJ.exit_reasons = getattr(one_line_progress_meter_PJJ, 'exit_reasons', QuickMeter_PJJ.exit_reasons)
    # exit_reason = one_line_progress_meter_PJJ.exit_reasons.get(key)
    return rc

def one_line_progress_meter_cancel_pjj(key='OK for 1 meter'):
    """
    Cancels and closes a previously created One Line Progress Meter window

    :param key: Key used when meter was created
    :type key:  (Any)
    :return:    None
    :rtype:     None
    """
    try:
        meter = QuickMeter_PJJ.active_meters[key]
        meter.window.Close()
        del (QuickMeter_PJJ.active_meters[key])
        QuickMeter_PJJ.exit_reasons[key] = 'cancelled'
    except:  # meter is already deleted
        QuickMeter_PJJ.exit_reasons[key] = 'cancelled'
        return

if __name__ == '__main__':

    # Create the class
    #my_gui = GUI_ProgressBar()
    # run the event loop
    #for i in range(3):
    #    G.downloaded = G.downloaded + 1
    #    my_gui.run()
    #    sleep(3)
    '''
    for i in range(100):
        print(i)
        fb = one_line_progress_meter_PJJ('测试',i,100,'进度条',key='OK for 1 meter')
        print(f'fb : {fb}')
        if fb == False:
            break
        sleep(0.2)
    '''
    '''
    x = 0
    for i in range(10):
        print(i)
        a = one_line_progress_meter_PJJ('测试2',i,20,'进度条2',key='OKK')

        if i == 5:
            print('laile')
            one_line_progress_meter_cancel_pjj(key='OKK')
            x = 1
            #break
    sleep(3)
    '''
    
    for i in range(20):
        a = one_line_progress_meter_PJJ('测试2',i,10,f'{i}',key='OK2')
        sleep(0.1)
        if a == 'finished':
            one_line_progress_meter_cancel_pjj(key='OK2')
            sleep(1)
            break
    sleep(2)
