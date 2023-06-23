from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movie(name = {name}, rating = {rating}, year = {year})"
    
# db.create_all()

movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument("name", type=str, help="Name of the movie required", required=True)
movie_put_args.add_argument("rating", type=int, help="Rating of the movie required", required=True)
movie_put_args.add_argument("year", type=int, help="Year of the movie required", required=True)

movie_update_args = reqparse.RequestParser()
movie_update_args.add_argument("name", type=str, help="Name of the movie required")
movie_update_args.add_argument("rating", type=int, help="Rating of the movie required")
movie_update_args.add_argument("year", type=int, help="Year of the movie required")

sample_put = [
    {"name":"The Shawshank Redemption", "rating":9, "year":1994},
    {"name":"The Godfather", "rating":9, "year":1972 },
    {"name":"The Dark Knight", "rating":9, "year":2008}]


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "rating": fields.Integer,
    "year": fields.Integer
}


class Movie(Resource):
    # GET METHOD
    @marshal_with(resource_fields)
    def get(self, movie_id):
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            abort(404, message="Could not find movie with that id...")
        return result
    
    # PUT METHOD
    @marshal_with(resource_fields)
    def put(self, movie_id):
        args = movie_put_args.parse_args()
        result = MovieModel.query.filter_by(id=movie_id).first()
        if result:
            abort(409, message="Movie ID taken...")
        movie = MovieModel(id=movie_id, name=args["name"], rating=args["rating"], year=args["year"])
        db.session.add(movie)
        db.session.commit()
        return movie, 201
    
    # PATCH METHOD
    @marshal_with(resource_fields)
    def patch(self, movie_id):
        args = movie_update_args.parse_args()
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            abort(409, message="Movie ID doesn't exist, cannot update...")
        if args["name"]:
            result.name = args["name"]
        if args["rating"]:
            result.rating = args["rating"]
        if args["year"]:
            result.year = args["year"]

        db.session.commit()
        return result



    # DEL METHOD
    def delete(self, movie_id):
        video_not_exists(movie_id)
        del movies[movie_id]
        return "", 204
    

api.add_resource(Movie, "/movie/<int:movie_id>")

if __name__ == "__main__":
    app.run(debug=True)