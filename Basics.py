from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the movie required", required=True)
video_put_args.add_argument("rating", type=int, help="Rating of the movie required", required=True)
video_put_args.add_argument("year", type=int, help="Year of the movie required", required=True)

sample_put = [
    {"name":"The Shawshank Redemption", "rating":9, "year":1994},
    {"name":"The Godfather", "rating":9, "year":1972 },
    {"name":"The Dark Knight", "rating":9, "year":2008}]

users = {"halil": {"age":21, "gender":"male"},
         "tony": {"age":22, "gender":"male"},
         "taylor": {"age":23, "gender":"female"},
         "bojack": {"age":24, "gender":"horse:)"}}

movies = {}

def video_not_exists(movie_id):
    if movie_id not in movies:
        abort(404, message="Movie ID isn't valid!")

def video_exist(movie_id):
    if movie_id in movies:
        abort(409, message="Movie already exists with that ID!")


class HelloWorld(Resource):
    def get(self, name):
        return users[name]
    def post(self, name):
        return {"Message": f"Hello {name.title()}"}

class Movie(Resource):
    # GET METHOD
    def get(self, movie_id):
        video_not_exists(movie_id)
        return movies[movie_id]
    
    # PUT METHOD
    def put(self, movie_id):
        video_exist(movie_id)
        args = video_put_args.parse_args()
        movies[movie_id] = args
        return movies[movie_id], 201
    
    # DEL METHOD
    def delete(self, movie_id):
        video_not_exists(movie_id)
        del movies[movie_id]
        return "", 204
    

api.add_resource(HelloWorld, "/home/<string:name>")
api.add_resource(Movie, "/movie/<int:movie_id>")

if __name__ == "__main__":
    app.run(debug=True)