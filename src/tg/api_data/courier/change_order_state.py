import aiohttp

from api_data.config import BASE_URL


async def change_order_state(status: str, order_id: str) -> None:
    url = BASE_URL + f"order/{order_id}/status?status={status}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, ssl=False) as resp:
            print(await resp.text())


async def delivery_arrived(order_id: str) -> None:
    url = f"http://10.242.26.16:8000/api/delivery/arrived/?order_id={order_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            print(await resp.text())
