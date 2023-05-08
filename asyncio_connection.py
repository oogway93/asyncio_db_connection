import asyncio
import asyncpg

table_name = 'asyncio_testdb'  # table name

QUERY = f"INSERT INTO {table_name} VALUES($1, $2, $3)"


async def make_requests(db_pool):
    """function which make requests"""
    await db_pool.fetch(QUERY, 1, "something", 13)


async def main() -> int:
    """main function which add info"""
    portion = 200  # you can add your own portion of connections to postgresql (but you should be carefull)
    tasks = []  # list of tasks
    pended = 0

    db_pool = await asyncpg.create_pool("postgres://postgres:12345@localhost:5432/postgres")
    # postgres://user:pass@host:port/database | it's a example of your pool
    for _ in range(10000):
        tasks.append(asyncio.create_task(make_requests(db_pool)))
        pended += 1
        if len(tasks) == portion or pended == 10000:
            await asyncio.gather(*tasks)
            tasks = []
            print(pended)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
