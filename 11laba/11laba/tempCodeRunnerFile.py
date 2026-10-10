init_db()
    app = Flask(__name__)
    app.json.ensure_ascii = False
    cache = RedisCache()