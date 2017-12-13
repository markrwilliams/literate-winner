import os
import asyncio
import aiomysql

from mypackage.something import Something


async def init(app, loop):
    app['mysql_pool'] = await aiomysql.create_pool(
        unix_socket=os.environ['MYSQL_SOCKET'],
        user=os.environ['MYSQL_USER'],
        db=os.environ['MYSQL_DB'],
        charset='utf8mb4',
        maxsize=5,
        loop=loop
    )

    app['my_something'] = Something(mysql_pool=app['mysql_pool'])


async def test(app):
    one = await app['my_something'].get_something()
    print(repr(one))


async def done(app):
    app['mysql_pool'].close()
    await app['mysql_pool'].wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    app = {}

    loop.run_until_complete(init(app, loop))
    loop.run_until_complete(test(app))
    loop.run_until_complete(done(app))

# vim: ts=4 sw=4
