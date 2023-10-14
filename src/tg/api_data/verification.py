import aiohttp

from typing import Tuple

from api_data.config import BASE_URL


async def get_user_by_username(username: str) -> Tuple[dict, bool]:
    url = BASE_URL + f"users/{username}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            result = await resp.json()
            status = resp.status
    print(result)
    return result, status == 200


async def check_verification_code(username: str, code: str) -> bool:
    url = BASE_URL + f"users/{username}/verify?code={code}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, ssl=False) as resp:
            print(await resp.json())
            status = resp.status
    return status == 200
