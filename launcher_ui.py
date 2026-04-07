from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class LauncherUI:
    def __init__(self):
        self.paths = []
        self.scales = {}

        self.root = TkinterDnD.Tk()
        self.root.title("小放光明●桌宠工坊 🍀")
        self.root.geometry("900x520")
        self.root.minsize(700, 420)

        # 四叶草主题色
        self.bg_color = "#f3fbf5"
        self.primary = "#7bd88f"
        self.primary_dark = "#5ccf75"
        self.text_main = "#3aa65c"
        self.text_sub = "#7a9c84"
        self.card_bg = "#e8f8ec"

        self.root.configure(bg=self.bg_color)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # =========================
        # 主布局
        # =========================
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side="left", fill="y", padx=15, pady=10)

        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # =========================
        # 标题
        # =========================
        tk.Label(
            left_frame,
            text="🍀 小放光明●桌宠工坊 🍀",
            font=("微软雅黑", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_main
        ).pack(pady=(5, 2))

        tk.Label(
            left_frame,
            text="让小放光明陪你待在桌面吧 ✨",
            font=("微软雅黑", 10),
            bg=self.bg_color,
            fg=self.text_sub
        ).pack(pady=(0, 8))

        # =========================
        # 拖拽区
        # =========================
        self.drop_area = tk.Label(
            left_frame,
            text="🍀 请把图片丢进这里\n（或者点击下方按钮选择）",
            bg=self.card_bg,
            fg=self.text_main,
            width=28,
            height=4,
            relief="ridge",
            bd=2,
            font=("微软雅黑", 10)
        )
        self.drop_area.pack(pady=6)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        # =========================
        # 列表
        # =========================
        self.listbox = tk.Listbox(
            left_frame,
            height=10,
            bg="white",
            fg="#333",
            selectbackground=self.primary
        )
        self.listbox.pack(fill="y", pady=6)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # =========================
        # 滑块
        # =========================
        self.scale_slider = tk.Scale(
            left_frame,
            from_=0.02,
            to=0.3,
            resolution=0.005,
            orient="horizontal",
            label="🍀 调整桌宠大小",
            bg=self.bg_color,
            fg=self.text_main,
            highlightthickness=0,
            troughcolor="#dff5e6",
            command=self.on_scale_change
        )
        self.scale_slider.set(0.065)
        self.scale_slider.pack(fill="x", pady=6)

        # =========================
        # 按钮
        # =========================
        btn_frame = tk.Frame(left_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)

        def cute_btn(text, cmd):
            return tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=self.primary,
                fg="white",
                activebackground=self.primary_dark,
                relief="flat",
                padx=10,
                pady=5
            )

        cute_btn("📁 选择图片", self.select_files).pack(side="left", padx=4)
        cute_btn("🗑 删除", self.remove_selected).pack(side="left", padx=4)
        cute_btn("✨ 召唤桌宠", self.start).pack(side="left", padx=4)

        # =========================
        # 🪟 右侧预览
        # =========================
        tk.Label(
            right_frame,
            text="🍀 在这里预览桌宠效果 ✨",
            bg="white",
            fg="#999",
            font=("微软雅黑", 10)
        ).pack(pady=5)

        self.preview_label = tk.Label(right_frame, bg="white")
        self.preview_label.pack(expand=True)

        self.preview_label.bind("<MouseWheel>", self.on_mousewheel)

    # =========================
    # 文件选择
    # =========================
    def select_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")]
        )
        self.add_files(files)

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)

    def add_files(self, files):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                if f not in self.paths:
                    self.paths.append(f)
                    self.scales[f] = 0.065
                    name = f.split("/")[-1]
                    self.listbox.insert(tk.END, f"🍀 {name}")

    def remove_selected(self):
        selected = list(self.listbox.curselection())
        for index in reversed(selected):
            path = self.paths[index]
            self.listbox.delete(index)
            del self.paths[index]
            del self.scales[path]
        self.preview_label.config(image="")

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

    def on_scale_change(self, val):
        if not hasattr(self, "current_path"):
            return
        scale = float(val)
        self.scales[self.current_path] = scale
        self.on_select(None)

    def on_mousewheel(self, event):
        if not hasattr(self, "current_path"):
            return

        delta = 0.01 if event.delta > 0 else -0.01
        scale = self.scales[self.current_path] + delta
        scale = max(0.02, min(0.5, scale))

        self.scales[self.current_path] = scale
        self.scale_slider.set(scale)
        self.on_select(None)

    def start(self):
        if not self.paths:
            return
        self.root.destroy()

    def on_close(self):
        import sys
        sys.exit()

    def run(self):
        self.root.mainloop()
        return [{"path": p, "scale": self.scales[p]} for p in self.paths]