

import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="",
            # Content filtering
            word_count_threshold=10,
            excluded_tags=['form', 'header'],
            exclude_external_links=True,

            # Content processing
            process_iframes=True,
            remove_overlay_elements=True,

            # Cache control
            bypass_cache=False  # Use cache if available
        )

        if result.success:
            # Print clean content
            print("Content:", result.markdown[:500])  # First 500 chars

            # Process images
            for image in result.media["images"]:
                print(f"Found image: {image['src']}")

            # Process links
            for link in result.links["internal"]:
                print(f"Internal link: {link['href']}")

        else:
            print(f"Crawl failed: {result.error_message}")

async def crawl_article_feed():
    async with AsyncWebCrawler() as crawler:
        session_id = "feed_session"

        for page in range(3):
            result = await crawler.arun(
                url="https://www.thenorthfacekorea.co.kr",
                session_id=session_id,
                js_code="document.querySelector('.load-more-button').click();" if page > 0 else None,
                wait_for="css:.article",
                css_selector=".article"  # Target article elements
            )
            print(f"Page {page + 1}: Extracted {len(result.extracted_content)} articles")

async def extract_filtered_products():
    async with AsyncWebCrawler() as crawler:
        session_id = "product_session"

        # Step 1: Open product page
        result = await crawler.arun(
            url="https://www.thenorthfacekorea.co.kr",
            session_id=session_id,
            wait_for="css:.product-item"
        )

        # Step 2: Apply filter (e.g., "On Sale")
        result = await crawler.arun(
            url="https://www.thenorthfacekorea.co.kr",
            session_id=session_id,
            js_code="document.querySelector('#sale-filter-checkbox').click();",
            wait_for="css:.product-item"
        )

        # Step 3: Scroll to load additional products
        for _ in range(2):  # Scroll down twice
            result = await crawler.arun(
                url="https://www.thenorthfacekorea.co.kr",
                session_id=session_id,
                js_code="window.scrollTo(0, document.body.scrollHeight);",
                wait_for="css:.product-item"
            )
            print(f"Loaded {len(result.extracted_content)} products after scroll")

if __name__ == "__main__":
    asyncio.run(extract_filtered_products())