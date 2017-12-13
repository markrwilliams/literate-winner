class Something(object):
    def __init__(self, mysql_pool=None):
        if mysql_pool is None:
            raise Exception('mysql_pool must not be None')

        self.mysql_pool = mysql_pool

    async def get_something(self):
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('select 1')
                one = await cur.fetchone()

        return one

# vim: ts=4 sw=4
