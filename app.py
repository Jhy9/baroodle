from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
from routesCourse import course
app.register_blueprint(course)
from routesExercise import exercise
app.register_blueprint(exercise)
import routes
