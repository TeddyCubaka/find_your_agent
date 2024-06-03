# from flask import Flask, jsonify, request

# app = Flask(__name__)


# @app.route('/', methods=['get'])
# def index():
#     return jsonify({
#         "code": 200,
#         "message": "welcome to a demo with flask api"
#     })


# with app.test_request_context('/hello', method='POST'):
#     # now you can do something with the request until the
#     # end of the with block, such as basic assertions:
#     assert request.path == '/hello'
#     assert request.method == 'POST'


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     data = request.get_json()
#     data['message'] = 'siiuuuuuuuuuuuuuuuuuuuuu'
#     return jsonify(data)


# if __name__ == '__main__':
#     app.run(debug=True)


from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
