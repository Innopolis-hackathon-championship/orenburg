import aiohttp

from api_data.config import BASE_URL


async def confirm(order_id: str) -> None:
    url = f"http://10.242.26.16:8000/api/order/take/?order_id={order_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            print(await resp.text())
