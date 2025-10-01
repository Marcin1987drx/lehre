import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # 1. Launch the page
        await page.goto(f'file://{file_path}')

        # 2. Initial state verification: "New Busbar Type" modal should be visible
        print("Verifying initial empty state...")
        modal_title = page.locator("#modalTitle")
        await expect(modal_title).to_have_text("New Busbar Type")
        await page.screenshot(path="jules-scratch/verification/01_initial_empty_state.png")
        print("Screenshot 1: Initial empty state verified.")

        # 3. Add a new type
        print("Adding a new busbar type...")
        await page.locator("#m_name").fill("Test Type")
        await page.locator("#m_points").select_option("10")
        await page.locator("#m_tolMin").fill("-0.15")
        await page.locator("#m_tolMax").fill("0.15")
        await page.locator("#saveTypeBtn").click()

        # Wait for the modal to disappear
        await expect(page.locator("#typeModal")).not_to_be_visible()
        print("New type created successfully.")

        # 4. Verify the new type is active and the main view is updated
        print("Verifying main view after adding a type...")
        await expect(page.locator("#measureTbody tr")).to_have_count(10)
        await page.screenshot(path="jules-scratch/verification/02_main_view_with_type.png")
        print("Screenshot 2: Main view with new type verified.")

        # 5. Verify Polish translation update
        print("Verifying Polish translations...")
        # Click the Polish language button
        await page.locator('button[data-lang-key="PL"]').click()

        # Check the save button text
        save_button = page.locator("#saveMeasurementBtn")
        await expect(save_button).to_have_text("Zapisz pomiar")

        # Click the save button to trigger the confirmation message
        await save_button.click()

        # Check the confirmation message text
        status_message = page.locator("#status")
        # In a headless environment, the file picker for CSV won't work, so we expect the base message.
        await expect(status_message).to_have_text("Zapisano.")

        await page.screenshot(path="jules-scratch/verification/03_polish_translation.png")
        print("Screenshot 3: Polish translation verified.")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())