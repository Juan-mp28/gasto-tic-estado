import os

import psycopg


def conectar():
    return psycopg.connect(prepare_threshold=None)


if __name__ == "__main__":
    with conectar() as conn:
        version = conn.execute("select version()").fetchone()[0]
        tablas = conn.execute("""
            select table_name
            from information_schema.tables
            where table_schema = 'raw'
            order by table_name
        """).fetchall()

    print(version)
    print([t[0] for t in tablas])