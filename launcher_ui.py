from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog


class LauncherUI:
    def __init__(self):
        self.paths = []

        self.root = TkinterDnD.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("桌宠生成器")
        self.root.geometry("420x360")

        # ===== 标题 =====
        tk.Label(
            self.root,
            text="拖拽图片到下方区域 或 点击选择",
            font=("微软雅黑", 12)
        ).pack(pady=10)

        # ===== 拖拽区域 =====
        self.drop_area = tk.Label(
            self.root,
            text="【拖拽图片到这里】",
            bg="#eeeeee",
            width=40,
            height=5
        )
        self.drop_area.pack(padx=10, pady=5)

        # 注册拖拽
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        # ===== 列表 =====
        self.listbox = tk.Listbox(self.root, height=8)
        self.listbox.pack(fill="both", expand=True, padx=10)

        # ===== 按钮区 =====
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="选择图片", command=self.select_files).pack(side="left", padx=5)
        tk.Button(btn_frame, text="删除选中", command=self.remove_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="开始生成", command=self.start).pack(side="left", padx=5)

        # ===== 状态 =====
        self.status = tk.Label(self.root, text="")
        self.status.pack()

    # =========================
    # 文件选择
    # =========================
    def select_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")]
        )

        self.add_files(files)

    # =========================
    # 拖拽处理
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
                    self.listbox.insert(tk.END, f)

    # =========================
    # 删除选中
    # =========================
    def remove_selected(self):
        selected = list(self.listbox.curselection())

        # 从后往前删（避免索引错乱）
        for index in reversed(selected):
            self.listbox.delete(index)
            del self.paths[index]

    # =========================
    # 开始生成
    # =========================
    def start(self):
        if not self.paths:
            self.status.config(text="请先选择图片！")
            return

        self.root.destroy()

    def on_close(self):
        import sys
        sys.exit()   # 杀进程

    def run(self):
        self.root.mainloop()
        return self.paths