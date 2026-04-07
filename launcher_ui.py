from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class LauncherUI:
    def __init__(self):
        self.paths = []
        self.scales = {}

        self.root = TkinterDnD.Tk()
        self.root.title("桌宠生成器")
        self.root.geometry("900x500")
        self.root.minsize(700, 400)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # =========================
        # 主布局（左右）
        # =========================
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # ===== 左侧 =====
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # ===== 右侧 =====
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # =========================
        # 左侧内容
        # =========================

        tk.Label(
            left_frame,
            text="拖拽图片 或 点击选择",
            font=("微软雅黑", 12)
        ).pack(pady=5)

        self.drop_area = tk.Label(
            left_frame,
            text="【拖拽图片到这里】",
            bg="#eeeeee",
            width=30,
            height=4
        )
        self.drop_area.pack(pady=5)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        self.listbox = tk.Listbox(left_frame, height=10)
        self.listbox.pack(fill="y", pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # ===== 滑块 =====
        self.scale_slider = tk.Scale(
            left_frame,
            from_=0.02,
            to=0.3,
            resolution=0.005,
            orient="horizontal",
            label="大小调整",
            command=self.on_scale_change
        )
        self.scale_slider.set(0.065)
        self.scale_slider.pack(fill="x", pady=5)

        # ===== 按钮 =====
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="选择图片", command=self.select_files).pack(side="left", padx=5)
        tk.Button(btn_frame, text="删除选中", command=self.remove_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="开始生成", command=self.start).pack(side="left", padx=5)

        # =========================
        # 右侧预览（核心）
        # =========================
        self.preview_label = tk.Label(right_frame, bg="white")
        self.preview_label.pack(expand=True)

        # 滚轮缩放
        self.preview_label.bind("<MouseWheel>", self.on_mousewheel)

    # =========================
    # 文件选择
    # =========================
    def select_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")]
        )
        self.add_files(files)

    # =========================
    # 拖拽
    # =========================
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)

    # =========================
    # 添加文件
    # =========================
    def add_files(self, files):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                if f not in self.paths:
                    self.paths.append(f)
                    self.scales[f] = 0.065
                    self.listbox.insert(tk.END, f)

    # =========================
    # 删除
    # =========================
    def remove_selected(self):
        selected = list(self.listbox.curselection())

        for index in reversed(selected):
            path = self.paths[index]
            self.listbox.delete(index)
            del self.paths[index]
            del self.scales[path]

        self.preview_label.config(image="")

    # =========================
    # 选中预览
    # =========================
    def on_select(self, event):
        if not self.listbox.curselection():
            return

        index = self.listbox.curselection()[0]
        path = self.paths[index]
        self.current_path = path

        img = Image.open(path).convert("RGBA")
        scale = self.scales[path]

        w = int(img.width * scale)
        h = int(img.height * scale)

        resized = img.resize((w, h))

        self.preview_img = ImageTk.PhotoImage(resized)
        self.preview_label.config(image=self.preview_img)

        self.scale_slider.set(scale)

    # =========================
    # 滑块
    # =========================
    def on_scale_change(self, val):
        if not hasattr(self, "current_path"):
            return

        scale = float(val)
        self.scales[self.current_path] = scale
        self.on_select(None)

    # =========================
    # 滚轮缩放
    # =========================
    def on_mousewheel(self, event):
        if not hasattr(self, "current_path"):
            return

        delta = 0.01 if event.delta > 0 else -0.01

        scale = self.scales[self.current_path] + delta
        scale = max(0.02, min(0.5, scale))

        self.scales[self.current_path] = scale
        self.scale_slider.set(scale)
        self.on_select(None)

    # =========================
    # 开始
    # =========================
    def start(self):
        if not self.paths:
            return
        self.root.destroy()

    def on_close(self):
        import sys
        sys.exit()

    # =========================
    # 返回数据
    # =========================
    def run(self):
        self.root.mainloop()

        return [
            {"path": p, "scale": self.scales[p]}
            for p in self.paths
        ]