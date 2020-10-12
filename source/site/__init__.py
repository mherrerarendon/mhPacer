from flask import Flask

app = Flask(__name__)

from source.site import parserRoutes, renderRoutes, speedmathRoutes
