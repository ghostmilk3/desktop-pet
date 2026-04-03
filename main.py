import tkinter as tk
from PIL import Image, ImageTk
import win32api
import win32con
import random
import os
import sys

class DesktopPet:
    def __init__(self):
        # ===== 窗口 =====
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        # ===== GIF路径 =====
        base_path = resource_path("pictures")
        self.gif_paths = [
            os.path.join(base_path, "1.gif"),
            # os.path.join(base_path, "2.gif"),
            # os.path.join(base_path, "3.gif"),
            # os.path.join(base_path, "4.gif"),
        ]

        # ===== 预加载GIF（解决卡顿）=====
        self.all_gifs = []
        for path in self.gif_paths:
            self.all_gifs.append(self.load_gif_frames(path))

        self.current_gif_index = 0
        self.frames = self.all_gifs[self.current_gif_index]

        # ===== 显示 =====
        self.current_frame = 0
        self.label = tk.Label(self.root, image=self.frames[self.current_frame], bg="white")
        self.label.pack()

        # ===== 鼠标 =====
        self.label.bind("<ButtonPress-1>", self.on_press)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<ButtonPress-3>", self.on_quit)

        # ===== 键盘 =====
        self.root.bind("<space>", self.on_quit)

        # ===== 状态 =====
        self.move_paused = False   # 只控制移动
        self.dragging = False

        # ===== 启动动画 =====
        self.animate()

        # ===== 屏幕 =====
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        self.root.geometry(f"+{self.screen_width - 200}+{self.screen_height - 200}")

        # ===== 自动移动 =====
        self.move_x = random.choice([-2, 2])
        self.move_y = random.choice([-2, 2])
        self.start_auto_move()

        # ===== 随机切换GIF =====
        self.gif_stay_time = 0
        self.root.after(1000, self.update_gif_stay_time)
        self.root.after(5000, self.random_change_gif)

    # ===== 预加载GIF =====
    def load_gif_frames(self, path):
        gif = Image.open(path)
        frames = []
        scale_factor = 0.11

        try:
            while True:
                frame = gif.convert("RGBA")  # 强制完整帧

                new_width = int(frame.width * scale_factor)
                new_height = int(frame.height * scale_factor)

                resized = frame.resize((new_width, new_height), Image.LANCZOS)

                frames.append(ImageTk.PhotoImage(resized))
                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

        return frames

    # ===== 动画 =====
    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.config(image=self.frames[self.current_frame])
        self.root.after(120, self.animate)

    # ===== 自动移动（受控制）=====
    def start_auto_move(self):
        if not self.move_paused:
            x = self.root.winfo_x() + self.move_x
            y = self.root.winfo_y() + self.move_y

            if x < 0 or x + self.label.winfo_width() > self.screen_width:
                self.move_x = -self.move_x
            if y < 0 or y + self.label.winfo_height() > self.screen_height:
                self.move_y = -self.move_y

            self.root.geometry(f"+{x}+{y}")

        self.root.after(30, self.start_auto_move)

    # ===== 随机切换GIF（无卡顿）=====
    def random_change_gif(self):
        probability = 0.3 + (self.gif_stay_time * 0.05)

        if random.random() < min(probability, 0.9):
            self.current_gif_index = random.randint(0, len(self.all_gifs) - 1)
            self.frames = self.all_gifs[self.current_gif_index]
            self.current_frame = 0
            self.gif_stay_time = 0

        self.root.after(5000, self.random_change_gif)

    def update_gif_stay_time(self):
        self.gif_stay_time += 1
        self.root.after(1000, self.update_gif_stay_time)

    # ===== 鼠标按下 =====
    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root

        self.offset_x = event.x
        self.offset_y = event.y

        self.dragging = False

    # ===== 拖动（丝滑）=====
    def on_drag(self, event):
        self.dragging = True

        mouse_x = event.x_root
        mouse_y = event.y_root

        x = mouse_x - self.offset_x
        y = mouse_y - self.offset_y

        self.root.geometry(f"+{x}+{y}")

    # ===== 松开 =====
    def on_release(self, event):
        end_x = event.x_root
        end_y = event.y_root

        dx = abs(end_x - self.start_x)
        dy = abs(end_y - self.start_y)

        # 点击（不是拖动）
        if dx < 5 and dy < 5:
            self.move_paused = not self.move_paused

        self.dragging = False

    # ===== 退出 =====
    def on_quit(self, event=None):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    pet = DesktopPet()
    pet.run()