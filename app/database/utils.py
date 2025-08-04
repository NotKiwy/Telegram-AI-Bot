import aiosqlite

DBP = " " # CHANGE IT!

async def _reg_(uid: int):
    async with aiosqlite.connect(DBP) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (id, coins, admin) VALUES (?, ?, ?)
        """, (uid, 0, 0))
        await db.commit()

async def _get_info_(uid: int):
    async with aiosqlite.connect(DBP) as db:
        async with db.execute("""
            SELECT coins, admin FROM users WHERE id = ?
        """, (uid,)) as cur:
            return await cur.fetchone()

async def _add_coins_(ncoins: int, uid: int):
    async with aiosqlite.connect(DBP) as db:
        await db.execute("""
            UPDATE users SET coins = coins + ? WHERE id = ?
        """, (ncoins, uid))
        await db.commit()

async def _remove_coins_(ncoins: int, uid: int):
    async with aiosqlite.connect(DBP) as db:
        await db.execute("""
            UPDATE users SET coins = coins - ? WHERE id = ?
        """, (ncoins, uid))
        await db.commit()

async def _use_admin_(val: int, uid: int):
    async with aiosqlite.connect(DBP) as db:
        await db.execute("""
            UPDATE users SET admin = ? WHERE id = ?
        """, (val, uid,))
        await db.commit()

async def _check_admin_(uid: int) -> bool:
    async with aiosqlite.connect(DBP) as db:
        async with db.execute("""
            SELECT admin FROM users WHERE id = ?
        """, (uid,)) as cur:
            result = await cur.fetchone()

            if result is None:
                return False

            return result[0] == 1