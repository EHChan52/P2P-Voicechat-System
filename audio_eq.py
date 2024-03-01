import numpy as np
from scipy.io import wavfile
from scipy import signal
import PySimpleGUI as sg
from datetime import time, datetime, timedelta
from audio_to_waveform import Generate_waveform
import os

class Equalizer:
    time_constant = time(0, 0, 0)
    def __init__(self):
        button_size=(45,32)
        sg.theme("LightBlue")
        # Load audio file
        self.fs, self.data = wavfile.read('test.wav')
        frame_20hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-20hz-',enable_events=True)],[sg.Text("20-40Hz")]]
        frame_40hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-40hz-',enable_events=True)],[sg.Text("40-80Hz")]]
        frame_80hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-80hz-',enable_events=True)],[sg.Text("80-160Hz")]]
        frame_160hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-160hz-',enable_events=True)],[sg.Text("160-320Hz")]]
        frame_320hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-320hz-',enable_events=True)],[sg.Text("320-640Hz")]]
        frame_640hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-640hz-',enable_events=True)],[sg.Text("640-1280Hz")]]
        frame_1280hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-1280hz-',enable_events=True)],[sg.Text("1280-2560Hz")]]
        frame_2560hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-2560hz-',enable_events=True)],[sg.Text("2560-5120Hz")]]
        frame_5120hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-5120hz-',enable_events=True)],[sg.Text("5120-10240Hz")]]
        frame_10240hz=[[sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=50,key='-10240hz-',enable_events=True)],[sg.Text("10240-20480Hz")]]
        frame_preview=[[sg.Text("Original    Audio:"),sg.Button("▶", font=(40), key="Play"),sg.Button("⏸", font=(40), key="Pause"),sg.Button("◼", font=(40), key="Stop"),sg.Text('time_constant', key="-Eplased_Playtime-"),sg.Text("/"),sg.Text('time_constant', key="-Audio_Length-"),sg.Slider(range=(0, 100),key="-Play_Length-",size=(30, 10),orientation="h",enable_events=True,disable_number_display=True,)],
                       [sg.Text("Resultant Audio:"),sg.Button("▶", font=(40), key="Play"),sg.Button("⏸", font=(40), key="Pause"),sg.Button("◼", font=(40), key="Stop"),sg.Text('time_constant', key="-Eplased_Playtime-"),sg.Text("/"),sg.Text('time_constant', key="-Audio_Length-"),sg.Slider(range=(0, 100),key="-Play_Length-",size=(30, 10),orientation="h",enable_events=True,disable_number_display=True,)]
                       ]
        frame_preamp=[[sg.Slider(range=(-100, 20), orientation='v', size=(15, 20), default_value=0,key='-preamp-')],[sg.Text("Preamp")]]
        frame_width=[[sg.Slider(range=(0.0,5.0), orientation='v', size=(15, 20), default_value=0.0,key='-width-')],[sg.Text("Width")]]
        frame_freq_macro=[[sg.Image('default.png',size=button_size,enable_events=True,key='-default-'),sg.Image('up1.png',size=button_size,enable_events=True,key='-up1-'),sg.Image('up2.png',size=button_size,enable_events=True,key='-up2-'),sg.Image('up3.png',size=button_size,enable_events=True,key='-up3-'),sg.Image('up4.png',size=button_size,enable_events=True,key='-up4-')],
                          [sg.Image('reset.png',size=button_size,enable_events=True,key='-reset-'),sg.Image('down1.png',size=button_size,enable_events=True,key='-down1-'),sg.Image('down2.png',size=button_size,enable_events=True,key='-down2-'),sg.Image('down3.png',size=button_size,enable_events=True,key='-down3-'),sg.Image('down4.png',size=button_size,enable_events=True,key='-down4-')]]
        frame_buttons=[[sg.Button('Preview Changes')],[sg.Button('Save & Exit')],[sg.Button('Discard & Exit')]]
        # Create sliders for each frequency band
        layout = [[sg.Text("Selected Audio to Equalize:"),sg.Text("selected_song_name")],
                    [sg.Frame('',frame_20hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_40hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_80hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_160hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_320hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_640hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_1280hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_2560hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_5120hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_10240hz,element_justification='center',border_width=0),
                   sg.Frame('',frame_preamp,element_justification='center',border_width=0),
                   sg.Frame('',frame_width,element_justification='center',border_width=0),
                    ],
                    [sg.Frame('',frame_preview,element_justification='center',border_width=0),sg.Frame('',frame_freq_macro,element_justification='center',border_width=0)],
                  [sg.Frame('',frame_buttons,element_justification='center',border_width=0),sg.Graph(canvas_size=(400, 200),graph_bottom_left=(0, 0),graph_top_right=(400, 200),key="-GRAPH1-",enable_events=True,background_color="black"),sg.Graph(canvas_size=(400, 200),graph_bottom_left=(0, 0),graph_top_right=(400, 200),key="-GRAPH2-",enable_events=True,background_color="black")]
                  ]

        # Create the window
        self.window = sg.Window('Equalizer', layout)

    def changeValue(self, value, key):
    # Determine the frequency band from the slider key
        if 'hz' in key:
            band = int(key.strip('-hz-'))
            lowcut = band
            highcut = band * 2
            # Apply the filter to the audio data
            self.data = self.apply_filter(lowcut, highcut, value / 50)
        elif key == '-preamp-':
            self.data = self.data * (value / 50)
        elif key == '-width-':
            # Here you can add the functionality for the width slider
            self.width = value

    def apply_filter(self, lowcut, highcut, gain):
        nyquist = 0.5 * self.fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = signal.butter(1, [low, high], btype='band')
        return signal.lfilter(b, a, self.data) * gain

    def run(self):
        # Event Loop
        while True:
            event, values = self.window.read()
            self.window.finalize()
            print(event)
            if event == sg.WINDOW_CLOSED or event == 'Discard & Exit':
                break

            elif event == '-default-':
                default_value=50
                self.window["-20hz-"].update(default_value)
                self.window["-40hz-"].update(default_value)
                self.window["-80hz-"].update(default_value)
                self.window["-160hz-"].update(default_value)
                self.window["-320hz-"].update(default_value)
                self.window["-640hz-"].update(default_value)
                self.window["-1280hz-"].update(default_value)
                self.window["-2560hz-"].update(default_value)
                self.window["-5120hz-"].update(default_value)
                self.window["-10240hz-"].update(default_value)
                self.window["-preamp-"].update(default_value-default_value)
                self.window["-width-"].update(default_value-default_value)

            elif event == '-reset-':
                graph1 = self.window["-GRAPH1-"]
                graph2 = self.window["-GRAPH2-"]
                graph1.erase()
                graph2.erase()
                self.window["-GRAPH1-"].update("#000000")
                self.window["-GRAPH2-"].update("#000000")
                

            elif event == '-up1-':
                self.window["-20hz-"].update(values['-20hz-']+1)
                self.window["-40hz-"].update(values['-40hz-']+1)
                self.window["-80hz-"].update(values['-80hz-']+1)
                self.window["-160hz-"].update(values['-160hz-']+1)
                self.window["-320hz-"].update(values['-320hz-']+1)
                self.window["-640hz-"].update(values['-640hz-']+1)
                self.window["-1280hz-"].update(values['-1280hz-']+1)
                self.window["-2560hz-"].update(values['-2560hz-']+1)
                self.window["-5120hz-"].update(values['-5120hz-']+1)
                self.window["-10240hz-"].update(values['-10240hz-']+1)
            
            elif event == '-down1-':
                self.window["-20hz-"].update(values['-20hz-']-1)
                self.window["-40hz-"].update(values['-40hz-']-1)
                self.window["-80hz-"].update(values['-80hz-']-1)
                self.window["-160hz-"].update(values['-160hz-']-1)
                self.window["-320hz-"].update(values['-320hz-']-1)
                self.window["-640hz-"].update(values['-640hz-']-1)
                self.window["-1280hz-"].update(values['-1280hz-']-1)
                self.window["-2560hz-"].update(values['-2560hz-']-1)
                self.window["-5120hz-"].update(values['-5120hz-']-1)
                self.window["-10240hz-"].update(values['-10240hz-']-1)

            elif event == '-up2-':
                self.window["-20hz-"].update(10)
                self.window["-40hz-"].update(20)
                self.window["-80hz-"].update(30)
                self.window["-160hz-"].update(40)
                self.window["-320hz-"].update(50)
                self.window["-640hz-"].update(60)
                self.window["-1280hz-"].update(70)
                self.window["-2560hz-"].update(80)
                self.window["-5120hz-"].update(90)
                self.window["-10240hz-"].update(100)

            elif event == '-down2-':
                self.window["-10240hz-"].update(10)
                self.window["-5120hz-"].update(20)
                self.window["-2560hz-"].update(30)
                self.window["-1280hz-"].update(40)
                self.window["-640hz-"].update(50)
                self.window["-320hz-"].update(60)
                self.window["-160hz-"].update(70)
                self.window["-80hz-"].update(80)
                self.window["-40hz-"].update(90)
                self.window["-20hz-"].update(100)
            
            elif event == '-up3-':
                self.window["-20hz-"].update(100)
                self.window["-40hz-"].update(80)
                self.window["-80hz-"].update(60)
                self.window["-160hz-"].update(40)
                self.window["-320hz-"].update(20)
                self.window["-640hz-"].update(20)
                self.window["-1280hz-"].update(40)
                self.window["-2560hz-"].update(60)
                self.window["-5120hz-"].update(80)
                self.window["-10240hz-"].update(100)

            elif event == '-down3-':
                self.window["-20hz-"].update(20)
                self.window["-40hz-"].update(40)
                self.window["-80hz-"].update(60)
                self.window["-160hz-"].update(80)
                self.window["-320hz-"].update(100)
                self.window["-640hz-"].update(100)
                self.window["-1280hz-"].update(80)
                self.window["-2560hz-"].update(60)
                self.window["-5120hz-"].update(40)
                self.window["-10240hz-"].update(20)

            elif event == '-up4-':
                self.window["-10240hz-"].update(10-5)
                self.window["-5120hz-"].update(20-5)
                self.window["-2560hz-"].update(30-5)
                self.window["-1280hz-"].update(40-5)
                self.window["-640hz-"].update(50-5)
                self.window["-320hz-"].update(60-5)
                self.window["-160hz-"].update(70-5)
                self.window["-80hz-"].update(80-5)
                self.window["-40hz-"].update(90-5)
                self.window["-20hz-"].update(100-5)              

            elif event == '-down4-':
                self.window["-20hz-"].update(10-5)
                self.window["-40hz-"].update(20-5)
                self.window["-80hz-"].update(30-5)
                self.window["-160hz-"].update(40-5)
                self.window["-320hz-"].update(50-5)
                self.window["-640hz-"].update(60-5)
                self.window["-1280hz-"].update(70-5)
                self.window["-2560hz-"].update(80-5)
                self.window["-5120hz-"].update(90-5)
                self.window["-10240hz-"].update(100-5)          
            
            elif event == 'Preview Changes':
                wavfile.write('equalized.wav', self.fs, self.data.astype(np.int16))
                waveform_image1 = Generate_waveform("test.wav")
                waveform_image2 = Generate_waveform("equalized.wav")
                graph1 = self.window["-GRAPH1-"]
                graph2 = self.window["-GRAPH2-"]
                # Display the image on the graph
                graph1.draw_image(data=waveform_image1, location=(0, 200))
                graph2.draw_image(data=waveform_image2, location=(0, 200))

            elif event == 'Save & Exit':
                os.remove('temp_plot.png')
                break

            elif event == 'Discard & Exit':
                self.data = self.original_data.copy()


        self.window.close()

if __name__ == "__main__":
    equalizer = Equalizer()
    equalizer.run()
