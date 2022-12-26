
import psycopg2
import psycopg2.extras

# DB_HOST = "103.126.28.66"
# DB_NAME = "news"
# DB_USER = "postgres"
# DB_PASS = "khansia215758"

DB_HOST = "localhost"
DB_NAME = "skripsi"
DB_USER = "postgres"
DB_PASS = ""


connection_kwargs = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST,
}

