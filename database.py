import aiosqlite
import logging
import datetime

logger = logging.getLogger(__name__)
DB_FILE = "discord_bot_data.db"

async def initialize_database():
    """Initializes the database and creates the chat_history table if it doesn't exist."""
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    message_id INTEGER PRIMARY KEY,
                    channel_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    username TEXT NOT NULL, -- Store username for easier history formatting
                    content TEXT NOT NULL,
                    persona_name TEXT NULL -- Which persona said it (if bot)
                )
            """)
            await db.commit()
            logger.info(f"Database '{DB_FILE}' initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise # Re-raise exception to signal failure

async def add_message(message_id: int, channel_id: int, user_id: int, timestamp: datetime.datetime, username: str, content: str, persona_name: str | None = None):
    """Adds a message to the chat_history table."""
    timestamp_iso = timestamp.isoformat()
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(
                """
                INSERT INTO chat_history (message_id, channel_id, user_id, timestamp, username, content, persona_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (message_id, channel_id, user_id, timestamp_iso, username, content, persona_name)
            )
            await db.commit()
            logger.debug(f"Added message {message_id} to database.")
    except aiosqlite.IntegrityError:
         logger.warning(f"Message with ID {message_id} already exists in database. Skipping.")
    except Exception as e:
        logger.error(f"Error adding message {message_id} to database: {e}")

async def get_recent_messages(channel_id: int, limit: int = 15) -> list[dict]:
    """Retrieves the most recent messages from the chat_history table for a specific channel."""
    messages = []
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row # Return rows as dictionary-like objects
            async with db.execute(
                """
                SELECT message_id, channel_id, user_id, timestamp, username, content, persona_name
                FROM chat_history
                WHERE channel_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (channel_id, limit)
            ) as cursor:
                rows = await cursor.fetchall()
                # Convert rows to simple dicts and reverse order to be chronological
                messages = [dict(row) for row in reversed(rows)]
                logger.debug(f"Retrieved {len(messages)} recent messages for channel {channel_id}.")
    except Exception as e:
        logger.error(f"Error retrieving recent messages for channel {channel_id}: {e}")
    return messages
