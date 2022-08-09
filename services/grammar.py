import asyncio
import aiohttp
from bs4 import BeautifulSoup


class PluralService:
    def __init__(self):
        self.base_url = 'https://tools.dehumanizer.com/'
        self.url = f'{self.base_url}plural/index2.php/'
        self.arg = 'texto'
        self.selector = '#main h3 pre'
        self.words = {}

    async def __get_plural_html(self, word: str):
        async with aiohttp.ClientSession(self.base_url) as session:
            async with session.post(self.url, data={self.arg: word}) as response:
                return response.text()

    async def __parse_plural(self, word: str) -> str:
        html = await self.__get_plural_html(word)
        soup = BeautifulSoup(html, 'html.parser')
        plural = soup.select_one(self.selector).text
        self.words.update({word: plural})
    
    def get_plural(self, *words: tuple[str]) -> dict[str, str]:
        self.words.clear()
        loop = asyncio.get_event_loop()
        coroutines = [asyncio.create_task(self.__parse_plural(word)) for word in words]
        loop.run_until_complete(asyncio.wait(coroutines))
        return self.words
