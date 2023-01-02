import asyncio
import aiohttp

from loguru import logger
from aiohttp import ClientSession
from pyuseragents import random as random_useragent


async def worker(q: asyncio.Queue):
    while True:
        try:
            async with aiohttp.ClientSession(
                headers={'user-agent': random_useragent()}
            ) as client:

                email = await q.get()

                response = await client.post('https://webflow.com/api/v1/form/6399959f3306e532553eb712',
                                             data={
                                                 'name': 'Email Form',
                                                 'source': 'https://concordex.io/#get-early-access',
                                                 'test': 'false',
                                                 'fields[Name]': email.split('@')[0],
                                                 'fields[Email]': email,
                                                 'dolphin': 'false'
                                             })
                if 'ok' not in await response.text():
                    raise Exception()

        except:
            logger.error('Error\n')
            with open('error.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}\n')
        else:
            logger.info('Saving data')
            with open('successfully.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}\n')
            logger.success('Successfully\n')

        await asyncio.sleep(delay)


async def main():
    emails = open("emails.txt", "r+").read().strip().split("\n")

    q = asyncio.Queue()

    for account in list(emails):
        q.put_nowait(account)

    tasks = [asyncio.create_task(worker(q)) for _ in range(threads)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print("Bot Concordex @flamingoat\n")

    delay = int(input('Delay(sec): '))
    threads = int(input('Threads: '))

    asyncio.run(main())