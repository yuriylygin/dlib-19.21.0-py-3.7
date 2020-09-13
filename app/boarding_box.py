from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import dlib
import tempfile

app = Flask(__name__)
api = Api(app)

print(dlib.__version__)

class BoardingBox(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

    def post(self):
        args = self.parser.parse_args()
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(args.file.read())
            image = dlib.load_rgb_image(temp.name)
            
            face_detector = dlib.get_frontal_face_detector()
            faces = face_detector(image, 1)
            predictor = dlib.shape_predictor('/src/model/shape_predictor_5_face_landmarks.dat')  # эту модель надо скачать https://github.com/davisking/dlib-models/blob/master/shape_predictor_5_face_landmarks.dat.bz2

            res = []

            for face in faces:
                shape = predictor(image, face)
                face_points = list(map(lambda i:(shape.part(i).x, shape.part(i).y), range(shape.num_parts)))
                tl_corner = face.tl_corner()
                br_corner = face.br_corner()

                res.append({
                    'rectangle': [(tl_corner.x, tl_corner.y), (br_corner.x, br_corner.y)],
                    'facePoints': face_points
                })

        return res
        

api.add_resource(BoardingBox, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)