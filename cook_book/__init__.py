from flask import Flask


app = Flask("CookMe!!")
app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
app.debug = True

