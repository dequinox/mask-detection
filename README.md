# mask-detection

A small project for face mask detection. Pytorch and YOLOv3 were used for building the models.
Frontend uses P5.js for capturing and sending the images back to the backend.
Backend uses Flask to receive the images and send it to the model for further processing. Upon completion model returns the processed image back to backend and backend returns to front.

## INSTALLATION

Clone the project

```
> git clone https://github.com/dequinox/mask-detection.git
```

Clone YOLOv3 inside the main project
```
> git clone https://github.com/roboflow-ai/yolov3
```

Download the trained model [GoogleDrive](https://drive.google.com/drive/folders/1zSC8j9dU0Urm38C8_U83_v3UW6Oo1vxG).
Save it to the root folder.

## DETECTION

Start the application
```
python3 app.py
```

Open the browser at `http://localhost:5000/`.
And send the image to process or capture from video.