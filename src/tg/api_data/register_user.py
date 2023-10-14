import aiohttp

from api_data.config import BASE_URL


async def register_user(data: dict) -> None:
    url = BASE_URL + "users/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, ssl=False) as resp:
            print(await resp.text())
