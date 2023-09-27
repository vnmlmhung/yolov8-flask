# yolov8-flask
use for research object detection through api on flask 


`docker compose build`

`docker compose up`

run test api detction

`curl --request POST --header "Content-Type: application/json" -d '{ "image_uri": "https://firebasestorage.googleapis.com/v0/b/g2b2b-vnm.appspot.com/o/invoices%2F230901%2Fcd24d5c7-0123-49a9-b90d-003f225df19d20230901132105.jpg?alt=media&token=982d8211-f277-4f91-a604-8e690a3b4a5a" }' 'http://192.168.232.72:5000/v1/object-detection'`