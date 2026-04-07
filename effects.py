from PIL import Image
import math


def generate_wobble_frames(img, frame_count=36):
    """
    为静态图片创造弹动效果
    """

    frames = []
    width, height = img.size

    for i in range(frame_count):
        t = i / frame_count

        # =========================
        # 弹动曲线
        # =========================
        # 类似弹簧：快速上去 → 慢慢回落
        bounce = abs(math.sin(t * math.pi * 2)) ** 1.5

        # 强化弹动高度
        offset_y = int(25 * bounce)

        # =========================
        # 左右飘
        # =========================
        offset_x = int(8 * math.sin(t * math.pi * 2))

        # =========================
        # 轻微旋转
        # =========================
        angle = 4 * math.sin(t * math.pi * 2)

        rotated = img.rotate(angle, resample=Image.BICUBIC, expand=True)
        rw, rh = rotated.size

        # =========================
        # 画布
        # =========================
        canvas_w = width + 120
        canvas_h = height + 120
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

        paste_x = (canvas_w - rw) // 2 + offset_x
        paste_y = (canvas_h - rh) // 2 + offset_y

        canvas.paste(rotated, (paste_x, paste_y), rotated)

        frames.append(canvas)

    return frames