import aiohttp 

from api_data.config import BASE_URL


async def get_courier_data(username: str) -> dict:
    url = BASE_URL + f"courier/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            result: dict = await resp.json()
    return result


async def get_courier_order(username: str) -> dict:
    url = BASE_URL + f"courier/{username}/orders"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            result: dict = await resp.json()
    return result
