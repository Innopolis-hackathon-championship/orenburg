import aiohttp


async def register_user(data: dict) -> None:
    url = "api/users"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, ssl=False) as resp:
            print(await resp.text())
