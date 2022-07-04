from flask_app import app
from flask_app.controllers import recipes
from flask_app.controllers import chefs

if __name__ == "__main__":
    app.run(debug=True)