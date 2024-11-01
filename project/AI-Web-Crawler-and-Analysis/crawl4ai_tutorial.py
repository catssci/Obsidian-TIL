import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://www.thenorthfacekorea.co.kr",
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

if __name__ == "__main__":
    asyncio.run(main())