from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the video is required", required=True
)

videos = {}


def abort_not_existing_video(video_id):
    if video_id not in videos:
        abort(
            404, message="Could not find video..."
        )  # 404: could not find, 409: already exists


def abort_existing_video(video_id):
    if video_id in videos:
        abort(
            409, message="Video aleardy exists with that ID..."
        )  # 404: could not find, 409: already exists


# Resource: handle GET, PUT, POST,...
class Video(Resource):
    def get(self, video_id):
        abort_not_existing_video(video_id)
        return videos[video_id]

    def put(self, video_id):  # create sth
        abort_existing_video(video_id)
        args = video_put_args.parse_args()  # 모든 args 가져오기
        videos[video_id] = args
        return videos[video_id], 201  # 200 = Suceed, 201 = created

    def delete(self, video_id):
        abort_not_existing_video(video_id)
        del videos[video_id]
        return "", 204  # 204 = deleted successfully


# Add resource to API
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)  # debug mode
