from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

from app.predictor.controllers import predict

app.register_blueprint(predict)

