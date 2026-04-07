import tkinter as tk
from tkinter import messagebox
import win32api
import win32con
import random
import threading

from image_loader import load_image_frames
from launcher_ui import LauncherUI


class DesktopPet:
    def __init__(self):
        # ===== 选择图片 =====
        ui = LauncherUI()

        self.image_configs = ui.run()

        if not self.image_configs:
            messagebox.showerror("错误", "未选择任何图片！")
            exit()

        # ===== 主窗口 =====
        self.root = tk.Tk()
        self.root.withdraw()
        self.create_loading_window()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

        # ===== 状态 =====
        self.move_paused = False
        self.dragging = False

        # 进度相关变量
        self.current_text = "准备加载图片..."
        self.loading_done = False

        # 启动子线程加载
        threading.Thread(target=self.load_images_async, daemon=True).start()

        # 刷新加载文字
        self.update_loading_text()

    # =========================
    # 后台加载图片（子线程）
    # =========================
    def load_images_async(self):
        self.all_gifs = []

        for i, item in enumerate(self.image_configs):
            path = item["path"]
            scale = item["scale"]

            self.current_text = f"正在处理第 {i+1}/{len(self.image_configs)} 张图片..."
            anim = load_image_frames(path, scale)
            self.all_gifs.append(anim)

        self.loading_done = True

    # =========================
    # 加载窗口
    # =========================
    def create_loading_window(self):
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.protocol("WM_DELETE_WINDOW", self.exit_all)
        self.loading_win.title("正在处理")
        self.loading_win.geometry("260x120")
        self.loading_win.configure(bg="white")
        self.loading_win.attributes("-topmost", True)

        screen_w = self.loading_win.winfo_screenwidth()
        screen_h = self.loading_win.winfo_screenheight()
        x = (screen_w - 260) // 2
        y = (screen_h - 120) // 2
        self.loading_win.geometry(f"+{x}+{y}")

        self.loading_label = tk.Label(
            self.loading_win,
            text="准备加载图片...",
            bg="white",
            font=("微软雅黑", 11)
        )
        self.loading_label.pack(expand=True)

        def start_move(event):
            self.offset_x = event.x
            self.offset_y = event.y

        def do_move(event):
            x = event.x_root - self.offset_x
            y = event.y_root - self.offset_y
            self.loading_win.geometry(f"+{x}+{y}")

        self.loading_win.bind("<ButtonPress-1>", start_move)
        self.loading_win.bind("<B1-Motion>", do_move)

    # =========================
    # 刷新加载文字（主线程）
    # =========================
    def update_loading_text(self):
        self.loading_label.config(text=self.current_text)

        if self.loading_done:
            self.init_pet()
        else:
            self.root.after(100, self.update_loading_text)

    # =========================
    # 初始化桌宠（主线程）
    # =========================
    def init_pet(self):
        self.current_gif_index = 0
        self.current_anim = self.all_gifs[self.current_gif_index]

        self.frames = self.current_anim["frames"]
        self.durations = self.current_anim["durations"]
        self.current_frame = 0

        self.loading_win.destroy()
        self.root.deiconify()

        self.label = tk.Label(self.root, image=self.frames[self.current_frame], bg="white")
        self.label.pack()

        self.label.bind("<ButtonPress-1>", self.on_press)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<ButtonPress-3>", self.on_quit)

        self.root.bind("<space>", self.on_quit)

        self.animate()

        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        self.root.geometry(f"+{self.screen_width - 200}+{self.screen_height - 200}")

        self.move_x = random.choice([-2, 2])
        self.move_y = random.choice([-2, 2])
        self.start_auto_move()

        self.gif_stay_time = 0
        if len(self.all_gifs) > 1:
            self.root.after(1000, self.update_gif_stay_time)
            self.root.after(5000, self.random_change_gif)

    # =========================
    # 动画播放
    # =========================
    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.config(image=self.frames[self.current_frame])

        delay = self.durations[self.current_frame]
        self.root.after(delay, self.animate)

    # =========================
    # 自动移动
    # =========================
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

    # =========================
    # 随机切换
    # =========================
    def random_change_gif(self):
        probability = 0.3 + (self.gif_stay_time * 0.05)

        if random.random() < min(probability, 0.9):
            self.current_gif_index = random.randint(0, len(self.all_gifs) - 1)

            self.current_anim = self.all_gifs[self.current_gif_index]
            self.frames = self.current_anim["frames"]
            self.durations = self.current_anim["durations"]

            self.current_frame = 0
            self.gif_stay_time = 0

            self.fix_position()

        self.root.after(5000, self.random_change_gif)

    def fix_position(self):
        self.root.update_idletasks()

        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = self.label.winfo_width()
        h = self.label.winfo_height()

        if x < 0:
            x = 0
        elif x + w > self.screen_width:
            x = self.screen_width - w

        if y < 0:
            y = 0
        elif y + h > self.screen_height:
            y = self.screen_height - h

        self.root.geometry(f"+{x}+{y}")

    def update_gif_stay_time(self):
        self.gif_stay_time += 1
        self.root.after(1000, self.update_gif_stay_time)

    # =========================
    # 鼠标交互
    # =========================
    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.offset_x = event.x
        self.offset_y = event.y
        self.dragging = False

    def on_drag(self, event):
        self.dragging = True
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def on_release(self, event):
        if not hasattr(self, "start_x"):
            return

        dx = abs(event.x_root - self.start_x)
        dy = abs(event.y_root - self.start_y)

        if dx < 5 and dy < 5:
            self.move_paused = not self.move_paused

        self.dragging = False

    def on_quit(self, event=None):
        self.root.destroy()

    def exit_all(self):
        try:
            self.root.destroy()
        except:
            pass

        import os
        os._exit(0)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DesktopPet().run()