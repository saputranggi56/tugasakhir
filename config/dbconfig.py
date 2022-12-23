
import psycopg2
import psycopg2.extras

DB_HOST = "localhost"
DB_NAME = "skripsi"
DB_USER = "postgres"
DB_PASS = ""

CONN    = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
