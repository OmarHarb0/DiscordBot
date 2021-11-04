import logging
import time
import types

import discord
from asyncpg.exceptions import PostgresError
from discord.errors import InvalidArgument

class DatabaseUtils:
    def __init__(self, bot):
        self._bot = bot

    @property
    def bot(self):
        return self._bot

    @staticmethod
    def create_bind_groups(group_amount, group_size):
        s = ''
        # If group size is 1 range will produce one too few groups
        if group_size == 1:
            group_amount += 1

        for i in range(1, group_amount*group_size, group_size):
            s += '('

            s += ','.join(map(lambda n: f'${n}', range(i, i+group_size))) + '),'

        return s.rstrip(',')

    async def fetchval(self, sql, args=None):
        args = args or ()

        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetchval(sql, *args)

    async def fetch(self, sql, args=None, timeout=None, measure_time=False, fetchmany=True):
        args = args or ()

        async with self.bot.pool.acquire() as conn:
            t = time.perf_counter()

            if fetchmany:
                row = await conn.fetch(sql, *args, timeout=timeout)
            else:
                row = await conn.fetchrow(sql, *args, timeout=timeout)

            if measure_time:
                return row, time.perf_counter() - t

            return row

    async def execute_chunked(self, sql_statements, args=None, insertmany=False,
                              measure_time=False, timeout=None):
        """
        Args:
            sql_statements:
            args:
            insertmany:
            measure_time:
            timeout:
        Returns:
        """
        args = args or [() for _ in sql_statements]

        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                try:
                    t = time.perf_counter()
                    rows = []

                    for idx, sql in enumerate(sql_statements):
                        if insertmany:
                            row = await conn.executemany(sql, args[idx], timeout=timeout)
                        else:
                            row = await conn.execute(sql, *args[idx], timeout=timeout)

                        rows.append(rows)

                    if measure_time:
                        return rows, time.perf_counter() - t

                except PostgresError as e:
                    raise e

        return row

    async def execute(self, sql, args=None, measure_time=False,
                      insertmany=False, timeout=None):
        """
        Args:
            sql: sql query
            *args: args passed to execute
            measure_time: Return time it took to run query as well as ResultProxy
            **params: params passed to execute
        Returns:
            ResultProxy or ResultProxy, int depending of the value of measure time
        """

        args = args or ()

        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                try:
                    t = time.perf_counter()
                    if insertmany:
                        row = await conn.executemany(sql, args, timeout=timeout)
                    else:
                        row = await conn.execute(sql, *args, timeout=timeout)

                    if measure_time:
                        return row, time.perf_counter() - t

                except PostgresError as e:
                    raise e

        return row

    async def user_add(self, user_id: int, steam32: int, steam64: int, url: str):
        """
        params:
           user_id:
           steam64:
           steam32:
           url:
        """
        data = [user_id, steam32, steam64, url]
        sql = 'INSERT INTO users (id, steamid32, steamid64, url) VALUES ($1,$2,$3,$4)'
        await self.execute(sql, data)

    async def get_steam_id(self, user_id: int):
        """
        params:
            user_id:
        """
        sql = 'SELECT steamid32 FROM users WHERE id=$1'
        return await self.fetch(sql, (user_id,), fetchmany=False)
