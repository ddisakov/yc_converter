#!python3
import http
import time
import json
import boto3
import cv2

from http.server import BaseHTTPRequestHandler, HTTPServer


host = '0.0.0.0'
serverPort = 8080

#Set dimensions of the video for croping
dimensions = [(1280,720), (854,480), (640,360), (426,240)]


start_time = time.time()


#Web-server

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        print('Выполнен GET запрос')
        self.send_response(200)

    
    def do_POST(self):

        #Получение ссылки из запроса

        if 'Content-Length' in self.headers:
            nbytes = int(self.headers['Content-Length'])
        query = json.loads(self.rfile.read(nbytes))
        bucket = query['messages'][0]['details']['bucket_id']
        obj = query['messages'][0]['details']['object_id']
        link = 'https://storage.yandexcloud.net/' + bucket + '/' + obj
        print(link)

        #add assertion


        #Croping videos

        for i in dimensions:

            cap = cv2.VideoCapture(link)
            fps = cap.get(5)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, fps, i)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    frame_re = cv2.resize(frame, i)
                    out.write(frame_re)
                else:
                    break
            cap.release()
            out.release() #без этой строчки видео будет ломаться
            cv2.destroyAllWindows()

        # Подключение к бакету YC и загрузка

            session = boto3.session.Session()
            s3 = session.client(
                aws_access_key_id='z1EO_wkLKkx8jjSdXDlZ',
                aws_secret_access_key='gS9iiSE3vLAJgxWHxPJ1rb1s02yCp8VlVQFFNa2Q', 
                service_name='s3',
                endpoint_url='https://storage.yandexcloud.net')

            with open ('output.mp4', 'rb') as f:
                s3.upload_fileobj(f,'croped','uspex' + str(i[0]) +'.mp4') 


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    

if __name__ == "__main__":
    webServer = HTTPServer((host, serverPort), MyServer)
    print("Server started http://%s:%s" % (host, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.") 


    