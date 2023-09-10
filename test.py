from flask import Flask, render_template, request
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload'
RESULT_FOLDER = 'static/result'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_circles(image_path, output_path, dp=1.1, minDist=10, param1=300, param2=40, minRadius=10, maxRadius=40):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # resizing image
    height, width = image.shape

    target_width = 960
    target_height = 1280

    aspect_ratio = width / height

    if aspect_ratio >= 1:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    top_border = (target_height - new_height) // 2
    bottom_border = target_height - new_height - top_border

    left_border = (target_width - new_width) // 2
    right_border = target_width - new_width - left_border

    resized_image = cv2.copyMakeBorder(
        image, top_border, bottom_border, left_border, right_border, cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )

    # Hough Circle Transform using the passed parameters
    circles = cv2.HoughCircles(resized_image, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    output = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2BGR)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])  # center
            # cv2.circle(output, center, radius, (0, 255, 0), 2)
            cv2.circle(output, center, 2, (0, 0, 255), 3)  # Draw center

    # Count the number of detected circles
    num_circles = len(circles[0]) if circles is not None else 0
    count_text = f"Pipes: {num_circles}"

    # Draw the count on the image at the bottom left
    cv2.putText(output, count_text, (20, target_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imwrite(output_path, output)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            file_path = os.path.join(UPLOAD_FOLDER, 'upload.jpg')
            file.save(file_path)
            
            # Retrieve the circle detection parameters from the form with default values
            dp = float(request.form.get('dp', 1.1))
            minDist = int(request.form.get('minDist', 10))
            param1 = int(request.form.get('param1', 300))
            param2 = int(request.form.get('param2', 40))
            minRadius = int(request.form.get('minRadius', 10))
            maxRadius = int(request.form.get('maxRadius', 40))

            # Detect circles
            output_path = f"{RESULT_FOLDER}/result.jpg"
            detect_circles(file_path, output_path, dp, minDist, param1, param2, minRadius, maxRadius)

            return render_template('result.html', filename='result/result.jpg')


    return render_template('upload.html')





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
