import aiohttp


async def check_verification_code(username: str, code: str) -> bool:
    url = f"api/users/{username}/verify?code={code}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            status = resp.status
    return status == 200
