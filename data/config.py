from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # list of admins
IP = env.str("IP")  # The host ip address
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
STRIPE_TOKEN = env.str("STRIPE_TOKEN")
# DB_USER = env.str("POSTGRESQL_USER")
# DB_PASS = env.str("POSTGRESQL_PASSWORD")
# DB_NAME = env.str("POSTGRESQL_DBNAME")
# DB_HOST = env.str("POSTGRESQL_HOST")
