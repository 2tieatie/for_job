from data import config
from db_connection import *
import asyncio
from funcs import create_job


async def main():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()
    await create_job(1, 1, 'https://minfin.com.ua/currency/crypto/bitcoin/')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
