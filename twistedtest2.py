from twisted.internet import asyncioreactor
asyncioreactor.install()

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, defer
from twisted.python import log

import sys
import os
import asyncio
import aiomysql


class MyProtocol(Protocol):
    def connectionMade(self):
        log.msg('connectionMade')

        d = defer.ensureDeferred(self.testDb())
        d.addErrback(self.dFail)
        d.addCallback(self.dCall)

        self.transport.loseConnection()

    async def testDb(self):
        awaitable = self.factory.get_something()
        log.msg(type(awaitable))
        log.msg(repr(awaitable))
        one = await awaitable
        log.msg(repr(one))
        return repr(one)

    def dFail(self, failure):
        log.err('Failure!')
        log.err(failure)

    def dCall(self, result):
        log.msg(f'Success: {result}')


class MyFactory(Factory):
    protocol = MyProtocol

    def __init__(self):
        log.msg('MyFactory.__init__()')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init())

    async def init(self):
        self.mysql_pool = await aiomysql.create_pool(
            unix_socket=os.environ['MYSQL_SOCKET'],
            user=os.environ['MYSQL_USER'],
            db=os.environ['MYSQL_DB'],
            charset='utf8mb4',
            maxsize=3,
            loop=asyncio.get_event_loop()
        )

    async def get_something(self):
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('select 1')
                one = await cur.fetchone()

        return one


if __name__ == '__main__':
    log.startLogging(sys.stderr)
    f = MyFactory()
    reactor.listenTCP(23456, f)
    log.msg('starting reactor...')
    reactor.run()

# vim: ts=4 sw=4
