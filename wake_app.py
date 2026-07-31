import time
from playwright.sync_api import sync_playwright

# 1. 这里是你的真实 URL，不用改了
APP_URL = "https://aqrqu2ygrrmqc4f8rmj6vw.streamlit.app"

def wake_up():
    with sync_playwright() as p:
        # 模拟真实的桌面浏览器
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"正在打开应用页面: {APP_URL}")
        try:
            # 等待网络空闲
            page.goto(APP_URL, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"页面加载超时或出错: {e}")
            
        # --- 核心修改：留出更充足的时间让 Streamlit 渲染休眠页面 ---
        # 增加等待时间到 20 秒
        print("等待页面渲染完成 (20秒)...")
        time.sleep(20) 
        
        # --- 核心修改：优化按钮选择器，精准匹配你截图里的蓝色按钮 ---
        # 选择器意思：查找一个 button 元素，它的文本是 "Yes, get this app back up!"
        target_selectors = [
            'button:has-text("Yes, get this app back up!")', # 精准匹配
            'button:has-text("Wake it up")',                  # 备选旧版
            'button[kind="primary"]'                         # 备选样式
        ]
        
        clicked = False
        for selector in target_selectors:
            button = page.locator(selector)
            # 检查按钮是否存在并且可见
            if button.count() > 0 and button.first.is_visible():
                print(f"成功找到休眠按钮 (选择器: {selector})，正在点击唤醒...")
                try:
                    button.first.click()
                    clicked = True
                    # 唤醒需要一些时间启动容器
                    print("已点击唤醒按钮，正在等待应用启动 (25秒)...")
                    time.sleep(25)
                    print("唤醒指令已发送！")
                    break # 找到并点击后退出循环
                except Exception as e:
                    print(f"点击按钮失败: {e}")
                
        if not clicked:
            print("应用未显示休眠状态，或未检测到休眠按钮（可能已在运行）。")
            # 调试：如果有问题，这里可以选择打印页面 HTML 内容进行排查
            # print(page.content())
                
        browser.close()

if __name__ == "__main__":
    wake_up()
