import tqdm
from scrapy.utils.log import configure_logging

import scrapy
import os


class MangaSpider(scrapy.Spider):
    name = "manga"

    def start_requests(self):
        manga_name = "against-the-gods"
        start_chapter = 0
        end_chapter = 3
        base_url = "https://aresmanga.net/"

        # Configure logging to disable Scrapy's default log output
        # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

        # Create a progress bar using tqdm
        progress_bar = tqdm.tqdm(total=end_chapter - start_chapter + 1)

        for chapter_number in range(start_chapter, end_chapter + 1):
            url = f"{base_url}{manga_name}-chapter-{chapter_number}/"
            folder_path = f"./mangas/{manga_name}/{chapter_number}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            yield scrapy.Request(url=url, callback=self.parse, meta={'folder_path': folder_path})

            # Update the progress bar
            progress_bar.update()

        # Close the progress bar
        progress_bar.close()

    def parse(self, response):
        folder_path = response.meta['folder_path']
        image_urls = response.css('img::attr(src)').getall()
        for image_url in image_urls:
            yield scrapy.Request(url=image_url, callback=self.save_image, meta={'folder_path': folder_path})

    def save_image(self, response):
        folder_path = response.meta['folder_path']
        filename = os.path.basename(response.url)
        image_path = os.path.join(folder_path, filename)

        with open(image_path, 'wb') as f:
            f.write(response.body)
