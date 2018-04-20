from flask import Flask
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address
)
bootstrap = Bootstrap(app)

app.secret_key = 'super secret key'



from app import routes
