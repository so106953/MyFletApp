import asyncio
import flet as ft

DEFAULT_SECONDS = 25 * 60  # 25 分钟

# 小清新配色
BG = "#F7FAF8"
CARD = "#FFFFFF"
TEXT = "#2F3E46"
MUTED = "#84A98C"
ACCENT = "#52796F"

# 安全的系统本地中文字体族
FONT_F = "Segoe UI, Microsoft YaHei, 微软雅黑, Sans-Serif"


def format_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02d}:{s:02d}"


def main(page: ft.Page):
    # ==========================================
    # 👇 完美对接：格式已为您安全更改为 .ico
    page.window.icon = "assets/tomato.ico"
    page.window.version = "1.0.0"
    # ==========================================

    page.title = "番茄钟"
    page.bgcolor = BG
    page.padding = 40
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 420
    page.window.height = 560
    page.window.resizable = False
    
    # 🌟 字体安全降维：彻底消除网络字体拉取报错
    page.font_family = FONT_F

    remaining = DEFAULT_SECONDS
    running = False
    task: asyncio.Task | None = None

    time_text = ft.Text(
        format_time(remaining),
        size=72,
        weight=ft.FontWeight.W_300,
        color=TEXT,
        font_family="Segoe UI",
    )

    status_text = ft.Text(
        "专注一下 ☘️",
        size=16,
        color=MUTED,
        font_family=FONT_F,
    )

    progress = ft.ProgressBar(
        value=1.0,
        width=280,
        height=6,
        color=ACCENT,
        bgcolor="#E8F0EC",
        border_radius=8,
    )

    def update_ui():
        time_text.value = format_time(remaining)
        progress.value = remaining / DEFAULT_SECONDS
        page.update()

    def close_alert(_):
        # 🌟 修正：使用新版标准关闭弹窗语法
        page.close(alert)
        page.update()

    alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("时间到 🍅", weight=ft.FontWeight.BOLD, color=TEXT, font_family=FONT_F),
        content=ft.Text("25 分钟专注已完成，休息一下吧～", color=MUTED, font_family=FONT_F),
        actions=[
            ft.TextButton(content="知道了", on_click=close_alert),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=16),
    )

    # 🌟 修正：使用安全的 asyncio 挂起，保持界面 100% 灵敏
    async def tick():
        nonlocal remaining, running
        while running and remaining > 0:
            await asyncio.sleep(1)  # 👈 核心修正：释放主线程控制权，按键秒响应
            if not running:
                break
            remaining -= 1
            update_ui()

        if remaining == 0 and running:
            running = False
            status_text.value = "完成 ✨"
            start_btn.content = "开始"
            start_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED
            # 🌟 修正：使用新版标准打开弹窗语法
            page.open(alert)
            page.update()

    def stop_task():
        nonlocal task, running
        running = False
        if task and not task.done():
            task.cancel()
        task = None

    def on_start(_):
        nonlocal running, task
        if running:
            running = False
            start_btn.content = "继续"
            start_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED
            status_text.value = "已暂停"
        else:
            if remaining == 0:
                return
            running = True
            start_btn.content = "暂停"
            start_btn.icon = ft.Icons.PAUSE_ROUNDED
            status_text.value = "专注中…"
            task = page.run_task(tick)
        page.update()

    def on_reset(_):
        nonlocal remaining
        stop_task()
        remaining = DEFAULT_SECONDS
        start_btn.content = "开始"
        start_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED
        status_text.value = "专注一下 ☘️"
        update_ui()

    btn_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ACCENT,
        padding=ft.Padding.symmetric(horizontal=28, vertical=14),
        shape=ft.RoundedRectangleBorder(radius=24),
        elevation=0,
    )

    start_btn = ft.Button(
        content="开始",
        icon=ft.Icons.PLAY_ARROW_ROUNDED,
        style=btn_style,
        on_click=on_start,
    )

    reset_btn = ft.OutlinedButton(
        content="重置",
        icon=ft.Icons.REFRESH_ROUNDED,
        style=ft.ButtonStyle(
            color=ACCENT,
            side=ft.BorderSide(1, ACCENT),
            padding=ft.Padding.symmetric(horizontal=24, vertical=14),
            shape=ft.RoundedRectangleBorder(radius=24),
        ),
        on_click=on_reset,
    )

    card = ft.Container(
        content=ft.Column(
            [
                status_text,
                ft.Container(height=12),
                time_text,
                ft.Container(height=20),
                progress,
                ft.Container(height=32),
                ft.Row(
                    [start_btn, reset_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=CARD,
        padding=48,
        border_radius=28,
        shadow=ft.BoxShadow(
            blur_radius=24,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        ),
        width=340,
    )

    page.add(card)


if __name__ == "__main__":
    # 🌟 修正：改用官方最新的标准启动方法
    ft.app(main)