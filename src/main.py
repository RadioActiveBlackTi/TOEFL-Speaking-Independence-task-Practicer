from tkinter import *
import customtkinter as ctk
import tkinter.filedialog as fd
import gpt_parser as gp
import audio_manipulator as au

from threading import Thread

LARGEFONT =("Times", 30)
MIDFONT =("Times", 20)
class TkinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ProblemPage, ReviewPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        def start():
            if mode_value.get():
                topic = gp.get_topic()
            else:
                topic = "Would you prefer to work in a team or work alone on a project? Include details and explanation."

            controller.frames[ProblemPage].test(topic)


        def finder():
            if mode_value.get():
                return
            filename = fd.askopenfilename()
            link_value.set(filename)

        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text="TSIP: TOEFL Speaking Independent task Practicer", font=LARGEFONT, width=1280)

        mode_value = IntVar()
        mode_value.set(1)

        link_value = StringVar()
        link_value.set("")

        mode_button = ctk.CTkButton(self, text="Mode", font=LARGEFONT, width=300, height=100)
        radio1 = ctk.CTkRadioButton(self, text = 'GPT', variable = mode_value, value = 1, font=LARGEFONT, width=50, height=50)
        radio2 = ctk.CTkRadioButton(self, text='Pre-defined', variable = mode_value, value=0, font=LARGEFONT, width=50, height=50)

        import_button = ctk.CTkButton(self, text="Import Topic List", font=LARGEFONT, width=300, height=100,
                                      command = finder)
        link = ctk.CTkLabel(self, textvariable=link_value, font=LARGEFONT, height=50, wraplength=500)
        empty = ctk.CTkLabel(self, text="", width=1280, height=200)
        start_button = ctk.CTkButton(self, text="Start", font=LARGEFONT,
                                 command = start, width=640, height=70)

        label.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky ="nsew")
        mode_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        radio1.grid(row=1, column=1, padx=10, pady=10)
        radio2.grid(row=1, column=2, padx=10, pady=10)
        import_button.grid(row=2, column=0, padx=10, pady=10)
        link.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        empty.grid(row=3, column=0, padx=10, pady=10, columnspan=3)
        start_button.grid(row=4, column=0, padx=10, pady=10, columnspan=3)


class ProblemPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.topic = "NULL TEXT"

        self.pre_timer = IntVar()
        self.speak_timer = IntVar()
        self.topic_string = StringVar()

        self.variable_setting()

        empty_up = ctk.CTkLabel(self, text="", width=1280, height=50)
        dialogue = ctk.CTkLabel(self, textvariable=self.topic_string, font=MIDFONT, height=100, width=700,
                                wraplength=700, bg_color="light gray")
        empty_mid = ctk.CTkLabel(self, text="", width=1280, height=50)
        prt = ctk.CTkLabel(self, text="PREPARATION TIME", width=300, height=50, bg_color="gray", text_color="white")
        prti = ctk.CTkLabel(self, textvariable=self.pre_timer, width=500, height=50, font=LARGEFONT)
        empty_down = ctk.CTkLabel(self, text="", width=1280, height=50)
        spt = ctk.CTkLabel(self, text="RESPONSE TIME", width=300, height=50, bg_color="gray", text_color="white")
        spti = ctk.CTkLabel(self, textvariable=self.speak_timer, width=500, height=50, font=LARGEFONT)

        empty_up.grid(row=0, column=0)
        dialogue.grid(row=1, column=0)
        empty_mid.grid(row=2, column=0)
        prt.grid(row=3, column=0)
        prti.grid(row=4, column=0)
        empty_down.grid(row=5, column=0)
        spt.grid(row=6, column=0)
        spti.grid(row=7, column=0)


    def variable_setting(self):
        self.pre_timer.set(15)
        self.speak_timer.set(45)
        self.topic_string.set(self.topic)
        print(self.topic)

    def test(self, topic):
        self.topic = topic
        self.variable_setting()
        def audio():
            for work, args in [(au.topic_tts, self.topic), (au.delay, 2), (au.prepare_tts, None), (au.beep, None),
                               (au.delay, (15, self.pre_timer)), (au.speaknow_tts, None), (au.beep, None),
                               (au.record_start, None), (au.delay, (45, self.speak_timer)),
                               (au.record_stop, None), (au.delay, 1)]:
                if isinstance(args, type(str())) or isinstance(args, type(int())):
                    work(args)
                elif isinstance(args, type(tuple())):
                    work(args[0], args[1])
                else:
                    work()


        self.controller.show_frame(ProblemPage)
        th1 = Thread(target=audio)
        th1.start()


class ReviewPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

app = TkinterApp()
app.geometry("1280x720")
app.resizable(width=False, height=False)
app.title("TOEFL Seaking Independent task Practicer")
app.mainloop()