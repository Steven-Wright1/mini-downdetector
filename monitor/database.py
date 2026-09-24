import psycopg
import mini_downdetector_logger
import logging

logger = logging.getLogger("mini-downdetector.database")


DB_NAME = "mini_downdetector"
DB_USER = "postgres"
DB_PASS = ""
DB_PORT = "5432"
DB_HOST = "127.0.0.1"

def db_conn_open():
    try:
        logger.info("Attempting database connection")
        return psycopg.connect(
            dbname = DB_NAME,
            host = DB_HOST,
            port = DB_PORT,
            user = DB_USER,
            password = DB_PASS,
            connect_timeout = 3
        )
    except psycopg.Error as conn_err:
        logger.error("Connection to database failed", extra={"error":conn_err})
        return None

def db_conn_close(db_conn):
        logger.info("Closing database connection")
        db_conn.close()

def store_result(response, db_conn):
    cur = None
    try:
        cur = db_conn.cursor()
        
        logger.info("Attempting to insert monitoring results into database", extra={"txid": response.txid})
        logger.debug(
            "Inserting monitoring result",
            extra={
                "txid": response.txid,
                "datetime": response.check_datetime,
                "url": response.url,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "error": response.error,
            }
        )
        cur.execute("""
            INSERT INTO monitor_results (datetime, url, status_code,response_time, error, txid) 
            VALUES (%s,%s,%s,%s,%s,%s)""",
            (
             response.check_datetime, 
             response.url, 
             response.status_code,
             response.response_time,
             response.error, 
             response.txid
            )
        )
        logger.info("Committing changes to database", extra={"txid": response.txid})
        db_conn.commit()
    except psycopg.Error as db_err:
        logger.error("Error inserting results into the database", extra={"error":db_err, "txid": response.txid})
        db_conn.rollback()
    finally:
        if cur is not None:
            cur.close()
    return


