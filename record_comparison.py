import asyncio
import subprocess
from playwright.async_api import async_playwright

async def run():
    print("Starting local server...")
    server_process = subprocess.Popen(["python3", "server.py"])
    await asyncio.sleep(3)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                record_video_dir="../videos_compare/",
                record_video_size={"width": 1920, "height": 1080}
            )
            page = await context.new_page()
            
            print("Navigating to comparison page...")
            await page.goto("http://localhost:8081")
            await page.wait_for_timeout(2000)
            
            print("Clicking Connect Both Streams...")
            await page.click("text='Connect Both Streams'")
            
            print("Waiting 15 seconds for connections...")
            await page.wait_for_timeout(15000)
            
            print("Typing prompt...")
            await page.fill("#promptInput", "A massive dragon flying over a futuristic cyberpunk city")
            await page.click("text='Send Prompt'")
            
            print("Recording for 30 more seconds...")
            await page.wait_for_timeout(30000)
            
            await context.close()
            await browser.close()
    finally:
        server_process.terminate()
        print("Done.")

asyncio.run(run())
