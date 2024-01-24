from tkinter import *
import customtkinter as ctk
import tkinter.filedialog as fd

from tkinter.scrolledtext import ScrolledText
import random
import tkinter.messagebox as msg

from threading import Thread
import sys

try:
    import gpt_parser as gp
except:
    msg.showerror("GPT api key error", "OpenAI api key is not available or not in appropriate place. Make sure that " +
                                       "api key is in the same folder of this file, and saved as 'gpt-api-key.txt'.")
    sys.exit()

try:
    import audio_manipulator as au
except:
    msg.showerror("Audio error", "Audio device has some error. Please check about it.")
    sys.exit()

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
                try:
                    topic = gp.get_topic()
                except:
                    msg.showerror("ChatGPT Error", "ChatGPT could not generate topic. Please check your condition.")
                    return
            else:
                try:
                    with open(link_value.get()) as f:
                        topic_list = f.read().split("\n")
                        print(topic_list)
                        topic = random.choice(topic_list)
                except:
                    msg.showerror("File Opening Error", "The file has not properly opened. Please check the format of the file.")
                    return

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

    def instruction(self):
        try:
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

            self.controller.frames[ReviewPage].review(self.topic)
        except:
            msg.showerror("Resource error", "Please check the consistency of resources.")
            sys.exit()
        return

    def test(self, topic):
        self.topic = topic
        self.variable_setting()

        self.controller.show_frame(ProblemPage)
        th1 = Thread(target=self.instruction, daemon=True)
        th1.start()


class ReviewPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        def pause():
            au.pause_speech()
            button_play.configure(command=unpause)

        def unpause():
            au.unpause_speech()

        def start():
            au.start_speech()
            button_pause.configure(command=pause)

        def stop():
            au.stop_speech()
            button_play.configure(command=start)
            button_pause.configure(command=pause)

        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.topic = "NULL TEXT"
        self.response = "NULL RESPONSE"
        self.suggestion = "NULL SUGGESTION"

        left_frame = ctk.CTkFrame(self, border_width=1)
        right_frame = ctk.CTkFrame(self, border_width=1)
        top_frame = ctk.CTkFrame(self, height=100)

        top_frame.pack(side="top", fill="x", expand=False)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame.pack(side="right", fill="both", expand=True)

        # left frame part
        label1 = Label(left_frame, text="Your Response", font=('Arial', 25))
        button_play = ctk.CTkButton(left_frame, text="Play", font=MIDFONT, command=start)
        button_pause = ctk.CTkButton(left_frame, text="Pause", font=MIDFONT)
        button_stop = ctk.CTkButton(left_frame, text="Stop", font=MIDFONT, command=stop)

        self.response_text = ScrolledText(left_frame, height=32, font=('Arial', 11))

        label1.grid(row=0, column=0, columnspan=3, sticky="we")
        button_play.grid(row=1, column=0, sticky="we")
        button_pause.grid(row=1, column=1, sticky="we")
        button_stop.grid(row=1, column=2, sticky="we")
        self.response_text.grid(row=2, column=0, columnspan=3, sticky="swe")

        # right frame part
        self.topic_text = ScrolledText(right_frame, width=66, height=10, font=('Arial', 13))
        label2 = Label(right_frame, text="GPT Suggestion", font=('Arial', 25))
        self.suggestion_text = ScrolledText(right_frame, width=66, height=23.3, font=('Arial', 13))

        self.topic_text.grid(row=0, column=0, sticky="w")
        label2.grid(row=1, column=0, sticky="we")
        self.suggestion_text.grid(row=2, column=0, sticky="nws")

        # top frame part
        self.home_button = ctk.CTkButton(top_frame, text="Home", font=LARGEFONT)

        self.home_button.pack(side="left", padx=20, pady=20)

        self.text_set()


    def text_set(self):
        self.response_text.config(state="normal")
        self.response_text.delete('1.0', END)
        self.response_text.insert(END, self.response)
        self.response_text.config(state="disabled")

        self.topic_text.config(state="normal")
        self.topic_text.delete('1.0', END)
        self.topic_text.insert(END, self.topic)
        self.topic_text.config(state="disabled")

        self.suggestion_text.config(state="normal")
        self.suggestion_text.delete('1.0', END)
        self.suggestion_text.insert(END, self.suggestion)
        self.suggestion_text.config(state="disabled")

    def get_response(self):
        self.response = au.speaking_to_text()
        self.text_set()
        return

    def get_suggestion(self):
        self.suggestion = gp.get_sample_response(self.topic)
        self.text_set()
        return

    def review(self, topic):
        self.topic = topic
        self.response = "Processing..."
        self.suggestion = "Processing..."
        self.text_set()

        def to_home():
            th_response.join()
            th_suggestion.join()
            au.stop_speech()
            self.controller.show_frame(StartPage)

        self.home_button.configure(command=to_home)

        self.controller.show_frame(ReviewPage)

        th_response = Thread(target=self.get_response, daemon=True)
        th_suggestion = Thread(target=self.get_suggestion, daemon=True)

        th_response.start()
        th_suggestion.start()

if __name__=="__main__":
    app = TkinterApp()
    app.geometry("1280x720")
    app.resizable(width=False, height=False)
    app.title("TOEFL Seaking Independent task Practicer")
    app.mainloop()