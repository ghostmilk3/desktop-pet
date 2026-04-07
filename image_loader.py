from PIL import Image, ImageTk
from effects import generate_wobble_frames


def load_image_frames(path):
    """
    统一加载图片：
    - GIF：保持原始动画 + 原始帧间隔
    - PNG/JPG：生成伪动效
    """

    ext = path.lower().split(".")[-1]

    # =========================
    # GIF：完全按原动画播放
    # =========================
    if ext == "gif":
        gif = Image.open(path)

        tk_frames = []
        durations = []

        try:
            while True:
                frame = gif.convert("RGBA")

                # 缩放（不改变节奏）
                new_size = (
                    int(frame.width * 0.065),
                    int(frame.height * 0.065)
                )
                resized = frame.resize(new_size)

                tk_frames.append(ImageTk.PhotoImage(resized))

                # 使用GIF原始帧间隔
                duration = gif.info.get("duration", 100)
                durations.append(duration)

                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

        return {
            "frames": tk_frames,
            "durations": durations,
            "is_gif": True
        }

    # =========================
    # PNG/JPG：生成动效
    # =========================
    else:
        img = Image.open(path).convert("RGBA")

        frames = generate_wobble_frames(img)

        tk_frames = []
        durations = []

        for frame in frames:
            new_size = (
                int(frame.width * 0.065),
                int(frame.height * 0.065)
            )
            resized = frame.resize(new_size)

            tk_frames.append(ImageTk.PhotoImage(resized))

            # 静态图统一节奏
            durations.append(50)

        return {
            "frames": tk_frames,
            "durations": durations,
            "is_gif": False
        }