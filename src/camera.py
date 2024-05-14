from flask import Flask, Response, render_template, jsonify, request as flask_req
import cv2
import post_ip

app = Flask(__name__)
port = 5000

post_ip.get_and_post_ip()

def generate_frames(cameraIndex=0):
    camera = cv2.VideoCapture(cameraIndex)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    camera_index = flask_req.args.get("cameraIndex", default=0, type=int)
    return Response(
        generate_frames(camera_index),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    # app.run(ssl_context=('cert.pem', 'key.pem'),debug=True, host='0.0.0.0', port=5001)
    # app.run(debug=True, host="0.0.0.0", port=port)
    app.run(debug=True, port=port)
