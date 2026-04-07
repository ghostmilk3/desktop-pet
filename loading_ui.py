import tkinter as tk


class LoadingUI:
    def __init__(self, root, on_close):
        self.root = root
        self.on_close = on_close

        # 主题色
        self.bg_color = "#f3fbf5"
        self.text_main = "#3aa65c"
        self.text_sub = "#7a9c84"

        self.win = tk.Toplevel(root)
        self.win.title("Twinkle Loading 🍀")
        self.win.geometry("320x180")
        self.win.configure(bg=self.bg_color)
        self.win.attributes("-topmost", True)

        # 绑定关闭事件
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

        # =========================
        # 居中
        # =========================
        self.win.update_idletasks()
        screen_w = self.win.winfo_screenwidth()
        screen_h = self.win.winfo_screenheight()
        x = (screen_w - 320) // 2
        y = (screen_h - 180) // 2
        self.win.geometry(f"+{x}+{y}")

        # =========================
        # 标题
        # =========================
        tk.Label(
            self.win,
            text="🍀 TwinkleFun 召唤中...",
            bg=self.bg_color,
            fg=self.text_main,
            font=("微软雅黑", 12, "bold")
        ).pack(pady=(15, 5))

        # =========================
        # 进度文本（上）
        # =========================
        self.progress_label = tk.Label(
            self.win,
            text="🍀 正在准备中...",
            bg=self.bg_color,
            fg=self.text_main,
            font=("微软雅黑", 10, "bold")
        )
        self.progress_label.pack(pady=(5, 2))

        # =========================
        # 动态文案（下）
        # =========================
        self.texts = [
            "小放光明正在降落桌面 ✨",
            "小狐狸在整理尾巴 🦊",
            "小熊正在打哈欠 🐻",
            "蓝莓补给中 🍇",
            "四叶草好运加载中 🍀"
        ]

        self.index = 0

        self.tip_label = tk.Label(
            self.win,
            text=self.texts[0],
            bg=self.bg_color,
            fg=self.text_sub,
            font=("微软雅黑", 10)
        )
        self.tip_label.pack(expand=True)

        self.update_text()

    # =========================
    # 动态文案轮播
    # =========================
    def update_text(self):
        self.tip_label.config(
            text=self.texts[self.index % len(self.texts)]
        )
        self.index += 1
        self.win.after(2800, self.update_text)

    # =========================
    # 更新进度
    # =========================
    def update_progress(self, text):
        try:
            self.progress_label.config(text=text)
        except:
            pass

    # =========================
    # 销毁
    # =========================
    def destroy(self):
        self.win.destroy()