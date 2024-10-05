import tkinter as tk
from tkinter import messagebox
import pygame
import multiprocessing

class CountdownTimer:
    def __init__(self, root, blocked_flag, timer_active):
        print("Initializing CountdownTimer...")
        self.root = root
        self.blocked_flag = blocked_flag
        self.timer_active = timer_active
        #self.root.title("Таймер обратного отсчета")
        self.root.title("АХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХАХАХХАХХАХХАХАХАХАХ")
        self.root.geometry("500x500")

        self.time_left = 60000
        self.running = False
        self.timer_id = None
        self.text_size=100
        self.text_font="Rubic"
        self.color_graphite = "#474a51"
        self.color_greygreen = "#4a5147"
        self.color_darkred = "#744364"
        self.color_white = "#f6f6f7"
        self.pink_palette_heavypink = "#F38181"
        self.pink_palette_semiyellow = "#FCE38A"
        self.pink_palette_creamyellow = "#EAFFD0"
        self.pink_palette_marinegreemkrayola = "#95E1D3"
        self.all_bg_color = self.color_white
        self.all_text_color = self.pink_palette_heavypink
        self.all_secondary_bg_color = self.color_white
        self.all_bottom_buttons_grid_type = "flat"
        self.root.configure(bg=self.all_bg_color)

        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound("src/Sounds/Signal.wav")
        self.stop_sound = pygame.mixer.Sound("src/Sounds/Stop.wav")

        self.create_widgets()
        print("CountdownTimer initialized successfully.")

    def create_widgets(self):
        print("Creating widgets...")

        # Холдер между окнами ввода времени
        self.entry_frame = tk.Frame(self.root, bg=self.all_bg_color)
        self.entry_frame.pack(pady=20, expand=True, anchor="center")  # Центровка по вертикали и горизонтали

        # Ввод секунд
        self.seconds_entry = tk.Entry(self.entry_frame, width=2, font=(self.text_font, 20),
                                      bg=self.all_secondary_bg_color, fg=self.all_text_color, relief="flat")
        self.seconds_entry.insert(0, "60")
        self.seconds_entry.grid(row=0, column=0, padx=5)

        # Ввод миллисекунд
        self.milliseconds_entry = tk.Entry(self.entry_frame, width=3, font=(self.text_font, 20),
                                           bg=self.all_secondary_bg_color, fg=self.all_text_color, relief="flat")
        self.milliseconds_entry.insert(0, "0")
        self.milliseconds_entry.grid(row=0, column=1, padx=5)

        # Холдер для таймера
        self.timer_label = tk.Label(self.root, text="00:00.000", font=(self.text_font, self.text_size),
                                    bg=self.all_bg_color, fg=self.all_text_color, relief="flat")
        self.timer_label.pack(pady=20, expand=True, anchor="center")  # Центровка по вертикали и горизонтали

        # Холдер между кнопками
        self.button_frame = tk.Frame(self.root, bg=self.all_bg_color, relief="solid")
        self.button_frame.pack(pady=20, expand=True, anchor="center")  # Центровка по вертикали и горизонтали

        # Кнопка "Запустить"
        self.start_button = tk.Button(self.button_frame, text="Запустить", command=self.start_timer,
                                      width=10, bg=self.all_secondary_bg_color, fg=self.all_text_color,
                                      relief=self.all_bottom_buttons_grid_type)
        self.start_button.grid(row=0, column=0, padx=10)

        # Кнопка "Стоп"
        self.stop_button = tk.Button(self.button_frame, text="Стоп", command=self.stop_timer,
                                     width=10, bg=self.all_secondary_bg_color, fg=self.all_text_color,
                                     relief=self.all_bottom_buttons_grid_type)
        self.stop_button.grid(row=0, column=1, padx=10)

        # Кнопка "Продолжить"
        self.continue_button = tk.Button(self.button_frame, text="Продолжить", command=self.continue_timer,
                                         width=10, bg=self.all_secondary_bg_color, fg=self.all_text_color,
                                         relief=self.all_bottom_buttons_grid_type)
        self.continue_button.grid(row=0, column=2, padx=10)

        # Кнопка "Рестарт"
        self.restart_button = tk.Button(self.button_frame, text="Рестарт", command=self.restart_timer,
                                        width=10, bg=self.all_secondary_bg_color, fg=self.all_text_color,
                                        relief=self.all_bottom_buttons_grid_type)
        self.restart_button.grid(row=0, column=3, padx=10)

        self.update_timer_display()
        print("Widgets created.")

    def update_timer_display(self):
        seconds = self.time_left // 1000
        milliseconds = self.time_left % 1000
        minutes = seconds // 60
        seconds = seconds % 60
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}.{milliseconds:03}")

    def start_timer(self):
        print("Starting timer...")
        self.time_left = int(self.seconds_entry.get()) * 1000 + int(self.milliseconds_entry.get())
        self.running = True
        self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            if self.timer_active.value:
                if not self.blocked_flag.value:
                    self.update_timer_display()
                    self.time_left -= 10
                    self.timer_id = self.root.after(10, self.countdown)
                else:
                    # Останавливаем таймер, если blocked_flag активен
                    self.stop_timer()
                    self.root.after(100, self.countdown)  # Проверяем каждый 100 мс
            else:
                self.root.after(100, self.countdown)  # Ожидаем активации
        elif self.time_left <= 0:
            self.timer_label.config(text="00:00.000")
            self.running = False
            self.stop_sound.play()
            messagebox.showinfo("Таймер", "Пиздец, конец времени!")

    def stop_timer(self):
        print("Stopping timer...")
        self.alarm_sound.play()
        if self.running:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.running = False

    def continue_timer(self):
        print("Continuing timer...")
        if not self.running and self.time_left > 0:
            self.running = True
            self.countdown()

    def restart_timer(self):
        print("Restarting timer...")
        self.stop_timer()
        self.time_left = int(self.seconds_entry.get()) * 1000 + int(self.milliseconds_entry.get())
        self.update_timer_display()