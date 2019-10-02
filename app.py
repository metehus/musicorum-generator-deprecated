from flask import Flask, request, send_file

import os
from io import BytesIO

# themes
from themes import Themes

app = Flask(__name__)
themes = Themes()


@app.route("/")
def main_route():
    return "Musiculum generator api"


@app.route('/generate', methods=['POST'])
def generator_route_post():
    content = request.json
    print(content)
    print(content['options']['size'])
    if content['user'] is None:
        return "Missing user", 400
    if content['theme'] is None:
        return "Missing user", 400
    img_io = BytesIO()
    img = themes.grid(content['user'], content['options']['size'],
                            content['options']['top'], content['options']['period'])
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(port=4000)
