import psycopg

DB_NAME = "mini_downdetector"
DB_USER = "postgres"
DB_PASS = ""
DB_PORT = "5432"
DB_HOST = "127.0.0.1"

def db_connect():
    try:
        conn = psycopg.connect(
            dbname = DB_NAME,
            host = DB_HOST,
            port = DB_PORT,
            user = DB_USER,
            password = DB_PASS,
        )
        print("SUccessfully connected!")
        return conn
    except psycopg.Error as conn_err:
        print(f'Database could not connect with {conn_err}')
        return None

def store_result(response):
    try:
        db_conn = db_connect()
        if db_conn is None:
            return
        cur = db_conn.cursor()

        cur.execute("""
            INSERT INTO monitor_results (datetime, url, status_code,response_time, error) 
            VALUES (%s,%s,%s,%s,%s)""",
            (response.check_datetime, response.url, response.status_code, response.response_time, response.error)
        )
        db_conn.commit()
        cur.close()
        db_conn.close()
    except psycopg.Error as db_err:
        print(f'Database error: {db_err}')
    return


