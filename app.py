from flask import Flask, render_template, request, jsonify  
import dash
from dashboard.component import load_component
from callbacks import *
import os 
import git
from dashboard import create_app


# ============================== back ============================== 
app = create_app()

# ========== 기본 라우터 ==========
# 인덱스 페이지
@app.route("/") 
def index(): 
    return render_template('index.html')

@app.route("/update_server", methods=['POST'])
def webhook(): 
    if request.method == "POST": 
        BASE_DIR = os.path.dirname(__file__)
        repo = git.Repo(BASE_DIR)
        origin = repo.remotes.origin
        origin.pull()
        return "Pythonanywhere 서버에 성공적으로 업로드되었습니다.", 200
    else: 
        return "유효하지 않은 이벤트 타입입니다.", 400



# ===== front ===== 
# Dash 애플리케이션 인스턴스 생성
dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/dashapp1/')

# 애플리케이션 레이아웃 
dash_app1.layout = load_component() 

# 콜백 
register_callbacks(dash_app1)
    

# 서버 실행
if __name__ == '__main__':
    app.debug = True 
    app.run() 
