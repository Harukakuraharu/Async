import asyncio
from datetime import datetime
from typing import Union

import requests
from aiohttp import ClientSession
from more_itertools import chunked

from models import Character
from settings import Session, init_db

MAX_CHUNK = 5
CHARACTER_COUNT = requests.get("https://swapi.py4e.com/api/people/").json()["count"]


async def get_character(character_id: str, session: ClientSession) -> dict:
    """Get data about all heroes"""
    response = await session.get(f"https://swapi.py4e.com/api/people/{character_id}/")
    if response.status == 200:
        data = await response.json()
        return data
    else:
        return {"detail": "Not found"}


async def read_url(url: str, key: str, session: ClientSession) -> str:
    """Read the URL to fill in information about heroes"""
    async with session.get(f"{url}") as response:
        data = await response.json()
        return data[key]


async def get_urls(urls: Union[list | str], key: str, session: ClientSession) -> str:
    """Get URL if urls contains more than one field"""
    if urls:
        if isinstance(urls, list):
            result = [await read_url(url, key, session) for url in urls]
            return ", ".join(result)
        if isinstance(urls, str):
            return await read_url(urls, key, session)
    return ""


async def insert_to_db(characters: list[dict]) -> None:
    """Insert data for database"""
    async with Session() as db_session:
        async with ClientSession() as session:
            for data in characters:
                if data.get("detail") == "Not found":
                    break
                character = Character(
                    birth_year=data.get("birth_year"),
                    eye_color=data.get("eye_color"),
                    films=await get_urls(data.get("films"), "title", session),
                    gender=data.get("gender"),
                    hair_color=data.get("hair_color"),
                    height=data.get("height"),
                    homeworld=await get_urls(data.get("homeworld"), "name", session),
                    mass=data.get("mass"),
                    name=data.get("name"),
                    skin_color=data.get("skin_color"),
                    species=await get_urls(data.get("species"), "name", session),
                    starships=await get_urls(data.get("starships"), "name", session),
                    vehicles=await get_urls(data.get("vehicles"), "name", session),
                )
                db_session.add(character)
                await db_session.commit()


async def main():
    await init_db()
    session = ClientSession()
    for item_chunk in chunked(range(1, CHARACTER_COUNT + 1), MAX_CHUNK):
        coros = [get_character(character_id, session) for character_id in item_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_to_db(result))
    await session.close()

    all_tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*all_tasks_set)


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    print(
        f"Successfully! Data loaded into database in {datetime.now() - start} seconds"
    )
