This web application allows users to upload images and count the number of pipes present in them using the Hough Circle Transform algorithm. It provides a simple user interface to adjust parameters and visualize the result, ensuring an efficient and user-friendly experience.

Installation
Clone the Repository:
git clone https://github.com/arpit57/countPipes

Install the required packages:
Ensure you have pip installed and run:
pip install -r requirements.txt

Usage
Starting the Application:
python test.py

Web Interface:
Once the application is running, navigate to http://127.0.0.1:8080/ on your web browser. You can then upload an image and adjust the parameters to detect the pipes.

Adjusting Parameters:
Users can tweak the Hough Circle Transform parameters to optimize the detection based on their image characteristics.

Contribution
Feel free to fork this repository and enhance the functionalities. If you make any changes which you believe are valuable, create a pull request detailing the changes you've made.

Credits
OpenCV for the implementation of the Hough Circle Transform.
Flask for the web framework.
