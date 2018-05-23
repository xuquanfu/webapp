from flask import Flask,render_template,Response
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
from camera import Camera
from uartrev import ComThread
from multiprocessing import Process,Queue



app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
filename="mydata.txt"


#串口进程
def run_uartproc():
    rt = ComThread()

    try:
        if rt.start():
            print(rt.l_serial.name)
            rt.waiting()
            rt.stop()
        else:
            pass
    except Exception as se:
        print(str(se))

    if rt.alive:
        rt.stop()

    del rt

'''
#数据库类
class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    value = db.Column(db.String(120), unique=True)
    def __init__(self,name):
        self.username = name
    def __repr__(self):
        return '<Role %r>' % self.name
'''




#路由定向
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html', current_time=datetime.utcnow())
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/user')
def user():
    f1 = open(filename, 'r')
    content = f1.read()
    return render_template('user.html',value=content)


if __name__ == '__main__':


    Myuart = Process(target=run_uartproc)
    Myuart.start()
    manager.run()






    #python E:\code\webapp\haha.py runserver --host 0.0.0.0