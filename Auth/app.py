from flask import request
from config import create_app

app = create_app()


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


if __name__ == '__main__':
    app.run(debug=True)

