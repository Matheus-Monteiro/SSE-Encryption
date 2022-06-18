from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True

from .controllers import (
    controller
)

from .service import (
    service
)