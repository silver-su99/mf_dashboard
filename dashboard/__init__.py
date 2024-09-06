from flask import Flask
from flask_restx import Resource, Api




def create_app(): 
    # flask 애플리케이션 인스턴스 생성 
    app = Flask(__name__)



    # ========== api ==========
    from dashboard.apis.artist import artist_ns
    api = Api(app)
    api.add_namespace(artist_ns, '/artists')

    return app

