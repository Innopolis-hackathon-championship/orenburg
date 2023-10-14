import aiohttp

from api_data.config import BASE_URL


async def change_user_state(username: str, is_online: bool) -> None:
    url = BASE_URL + f"api/courier/{username}/state?is_online={is_online}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, ssl=False) as resp:
            print(await resp.json())
