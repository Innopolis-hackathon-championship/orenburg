import aiohttp

from typing import Tuple

from api_data.config import BASE_URL


async def confirm_order(order_id: str, telegram_id: str) -> Tuple[str, str]:
    url = f"http://10.242.26.16:8000/api/delivery/take/?order_id={order_id}" \
        f"&telegram_id={telegram_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            result = await resp.json()
    return result["delivery_address"], result["code"]
    

async def decline_order(order_id: str) -> None:
    url = f"http://10.242.26.16:8000/api/delivery/find/?order_id={order_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            print(await resp.json())
