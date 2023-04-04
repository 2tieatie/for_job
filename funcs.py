from datetime import timedelta
import requests
from bs4 import BeautifulSoup as BS
from db_connection import *
from asyncpg import UniqueViolationError
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()
scheduler.start()


async def add_price(url: str):
    price, change = parse(url)
    obj = Price(price=1, change=1)
    await obj.create()
    try:
        obj = Price(price=price, change=change)
        await obj.create()
    except UniqueViolationError:
        print('Объект не добавлен')


def parse(url: str) -> tuple:
    request = requests.get(url)
    html = BS(request.content, 'html.parser')
    elements = html.select('.sc-18a2k5w-1')
    for element in elements:
        if "$" in element.text:
            value = element.text
            price = value[:value.find('.0') + 3]
            change = value.replace(price, '').replace('\xa0', '')
            data = (price, change)
            return data


async def create_job(delay: int, times: int, url: str):
    value = parse(url)
    for i in range(times):
        run_date = datetime.datetime.now() + timedelta(seconds=delay * i)
        scheduler.add_job(add_price, 'date', run_date=run_date, kwargs={'url': url})

