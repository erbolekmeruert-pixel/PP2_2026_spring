try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None

from config import DB_CONFIG


def get_connection():
    if psycopg2 is None:
        raise RuntimeError(
            "psycopg2 is not installed. Run: pip install psycopg2-binary"
        )
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
                """
            )


def _get_or_create_player(cursor, username):
    cursor.execute(
        """
        INSERT INTO players (username)
        VALUES (%s)
        ON CONFLICT (username) DO UPDATE
        SET username = EXCLUDED.username
        RETURNING id
        """,
        (username,),
    )
    return cursor.fetchone()[0]


def save_session(username, score, level_reached):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            player_id = _get_or_create_player(cursor, username)
            cursor.execute(
                """
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s)
                """,
                (player_id, score, level_reached),
            )


def get_top_scores(limit=10):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    p.username,
                    gs.score,
                    gs.level_reached,
                    gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
                LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()


def get_personal_best(username):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s
                """,
                (username,),
            )
            row = cursor.fetchone()
            return row[0] if row else 0