import aiohttp

from api_data.config import BASE_URL


async def cancel_order(order_id: str) -> bool:
    url = BASE_URL + f"order/{order_id}"
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, ssl=False) as resp:
            status = resp.status
    return status == 200
