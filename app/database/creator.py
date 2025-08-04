import aiosqlite

DBP = " " # CHANGE IT!

async def __db__():
    async with aiosqlite.connect(DBP) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 1,
                admin INTEGER DEFAULT 0
            )
        """)
        await db.commit()
