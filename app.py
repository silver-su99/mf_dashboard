from flask import Flask, render_template, request, jsonify  
import dash
from layout import streaming 
from dash import html, dcc, Input, Output, State, ctx, MATCH, ALL
from dash import callback_context
from flask_sqlalchemy import SQLAlchemy
from os import path
import git



# flask 애플리케이션 인스턴스 생성 
app = Flask(__name__)

# Dash 애플리케이션 인스턴스 생성
dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/dashapp1/')

# 인덱스 페이지
@app.route("/") 
def index(): 
    return render_template('index.html')

@app.route("/update_server", method=['POST'])
def webhook(): 
    if request.method == "POST": 
        repo = git.Repo("깃허브 레포 주소")
        origin = repo.remotes.origin
        origin.pull()
        return "Pythonanywhere 서버에 성공적으로 업로드되었습니다.", 200
    else: 
        return "유효하지 않은 이벤트 타입입니다.", 400

# 애플리케이션 레이아웃 정의
dash_app1.layout = streaming.streaming_pred() 


# 콜백 설정
@dash_app1.callback(
    [Output("modal-previous", "style"), Output("modal-state-previous", "data")],
    [Input("open-modal-btn-previous", "n_clicks"), Input("close-modal-btn-previous", "n_clicks")],
    [State("modal-previous", "style"), State("modal-state-previous", "data")],
)
def toggle_modal_previous(open_clicks, close_clicks, style, is_open):
    if open_clicks and (not is_open): 
        return {"display": "flex"}, True     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False 
    
    return {"display": "none"}, False


# 곡 정보 데이터 (곡 ID: [제목, 발매일])
artist_data = {
    '000001': ['이름 1', '1999-02-15', "2020-08-09", "2020", '그룹', "남성", '댄스', "소속사1"],
    '000002': ['이름 2', '1997-06-10', "2016-12-29", "2010", '솔로', "여성", '발라드', "소속사2"],
    '000003': ['이름 3', '1980-11-22', "2023-01-05", "2020", '그룹', "혼성", '댄스', '소속사3']
}

@dash_app1.callback(
    [
        Output("modal-artist", "style"),
        Output("modal-state-artist", "data"),
        Output("output-container-artist", "children", allow_duplicate=True),
        Output("artist-checklist", "value", allow_duplicate=True),
        Output('value-artist', 'data')
    ],
    [
        Input("open-modal-btn-artist", "n_clicks"),
        Input("close-modal-btn-artist", "n_clicks"),
        Input('load-btn-artist', 'n_clicks'),
    ],
    [
        State("modal-artist", "style"),
        State("modal-state-artist", "data"),
        State('artist-checklist', 'value'),
        State('value-artist', 'data')
    ],
        prevent_initial_call="initial_duplicate",

)
def handle_modal_and_update_output_artist(open_clicks, close_clicks, load_clicks, style, is_open, checked_values, data_artist):
    triggered = [p['prop_id'] for p in callback_context.triggered][0]
    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    
    if 'open-modal-btn-artist' in triggered:
        # Open modal button clicked
        return {"display": "flex"}, True, dash.no_update, dash.no_update, dash.no_update
    
    elif 'close-modal-btn-artist' in triggered:
        # Close modal button clicked
        return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update
    
    elif 'load-btn-artist' in triggered:
        # Load button clicked
        if not checked_values:
            return {"display": "none"}, False, "", checked_values, dash.no_update
        

        output_list = [
            html.Div(
                className="span-output-artist",
                children=[
                html.Span(artist_data[key][0], className='item-name'),   
            ]) for key in checked_values 
        ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]
        
        lst_update = [] 
        for key in checked_values:
            lst_update.append({"name": artist_data[key][0]})

        return {"display": "none"}, False, output_list, [], lst_update


    # Default return for no trigger
    return style, is_open, dash.no_update, dash.no_update, dash.no_update


@dash_app1.callback(
    [
        Output("output-container-artist", "children", allow_duplicate=True),
        Output("artist-checklist", "value", allow_duplicate=True)
    ],
    [Input("delete-btn-artist", "n_clicks")],
    prevent_initial_call="initial_duplicate"
)
def handle_delete_artist(*args):
    # Determine which button was clicked
    ctx = callback_context
    triggered = ctx.triggered[0]['value']

    # Clear the output and checklist
    if triggered:
        return [], []


# 콜백 설정
@dash_app1.callback(
    [Output("modal-info-artist", "style"), 
     Output("modal-state-info-artist", "data"),
     Output("output-container-artist-info", "children")],
    [Input(f"open-modal-btn-info-artist-{key}", "n_clicks") for key in artist_data.keys()]
    + [ Input("close-modal-btn-info-artist", "n_clicks")],
    [State("modal-info-artist", "style"), 
     State("modal-state-info-artist", "data")],
)
def toggle_modal_artist_info(*args):
    ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
    triggered = ctx.triggered[0] if ctx.triggered else None
    open_clicks = triggered['value']
    close_clicks = args[-3]
    is_open = args[-1]

    if open_clicks and (not is_open): 
        artist_id = triggered['prop_id'].split(".")[0].split('-')[-1]
        item = artist_data[artist_id]
        output_list = [
            html.Div([
                    html.Div(artist_id, className="value-artist-id"),
                    html.Div(item[0], className="value-name"),
                    html.Div(item[1], className="value-birth"),
                    html.Div(item[2], className="value-debut"),
                    html.Div(item[3], className="value-activity"),
                    html.Div(item[4], className="value-type"),
                    html.Div(item[5], className="value-gender"),
                    html.Div(item[6], className="value-genre"),
                    html.Div(item[7], className="value-agency"),
            ]) 
        ]
        
        return {"display": "flex"}, True, output_list     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False, [] 
    
    return {"display": "none"}, False, []


# 콜백 설정
@dash_app1.callback(
    [Output("modal-add-artist", "style"), Output("modal-state-add-artist", "data")],
    [Input("open-modal-btn-add-artist", "n_clicks"), Input("close-modal-btn-add-artist", "n_clicks")],
    [State("modal-add-artist", "style"), State("modal-state-add-artist", "data")],
)
def toggle_modal_artist_add(open_clicks, close_clicks, style, is_open):
    if open_clicks and (not is_open): 
        return {"display": "flex"}, True     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False 
    
    return {"display": "none"}, False


song_data = {
    '000001': ['제목 1', '2021-02-15', '발라드', '싱글'],
    '000002': ['제목 2', '2020-06-10', '댄스', 'EP'],
    '000003': ['제목 3', '2019-11-22', "발라드", '정규']
}

@dash_app1.callback(
    [
        Output("modal-song", "style"),
        Output("modal-state-song", "data"),
        Output("output-container-song", "children", allow_duplicate=True),
        Output("song-checklist", "value", allow_duplicate=True),
        Output('value-song', 'data')
    ],
    [
        Input("open-modal-btn-song", "n_clicks"),
        Input("close-modal-btn-song", "n_clicks"),
        Input('load-btn-song', 'n_clicks'),
    ],
    [
        State("modal-song", "style"),
        State("modal-state-song", "data"),
        State('song-checklist', 'value'),
        State('value-song', 'data')
    ],
        prevent_initial_call="initial_duplicate",

)
def handle_modal_and_update_output(open_clicks, close_clicks, load_clicks, style, is_open, checked_values, data_song):
    triggered = [p['prop_id'] for p in callback_context.triggered][0]
    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    
    if 'open-modal-btn-song' in triggered:
        # Open modal button clicked
        return {"display": "flex"}, True, dash.no_update, dash.no_update, dash.no_update
    
    elif 'close-modal-btn-song' in triggered:
        # Close modal button clicked
        return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update
    
    elif 'load-btn-song' in triggered:
        # Load button clicked
        if not checked_values:
            return {"display": "none"}, False, "", checked_values, dash.no_update
        
        # Only keep the last selected value
        checked_values = [checked_values[-1]]
        
        output_list = [
            html.Div(
                className="span-output-song",
                children=[
                html.Span(song_data[key][0], className='item-subject'),
                html.Button("X", id="delete-btn-song", className="delete-btn")
            ]) for key in checked_values
        ]
        
        for key in checked_values:
            subject = song_data[key][0]
        
        dic_song = {"subject": subject}

        print(dic_song)

        return {"display": "none"}, False, output_list, [], dic_song


    # Default return for no trigger
    return style, is_open, dash.no_update, dash.no_update, dash.no_update


@dash_app1.callback(
    [
        Output("output-container-song", "children", allow_duplicate=True),
        Output("song-checklist", "value", allow_duplicate=True)
    ],
    [Input("delete-btn-song", "n_clicks")],
    prevent_initial_call="initial_duplicate"
)
def handle_delete_song(delete_clicks):
    # Determine which button was clicked
    ctx = callback_context
    triggered = ctx.triggered[0]['value']

    # Clear the output and checklist
    if triggered:
        return [], []


# 콜백 설정
@dash_app1.callback(
    [Output("modal-info-song", "style"), 
     Output("modal-state-info-song", "data"),
     Output("output-container-song-info", "children")],
    [Input(f"open-modal-btn-info-song-{key}", "n_clicks") for key in song_data.keys()]
    + [ Input("close-modal-btn-info-song", "n_clicks")],
    [State("modal-info-song", "style"), 
     State("modal-state-info-song", "data")],
)
def toggle_modal_song_info(*args):
    ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
    triggered = ctx.triggered[0] if ctx.triggered else None
    open_clicks = triggered['value']
    close_clicks = args[-3]
    is_open = args[-1]

    if open_clicks and (not is_open): 
        song_id = triggered['prop_id'].split(".")[0].split('-')[-1]
        item = song_data[song_id]
        output_list = [
            html.Div([
                    html.Div(song_id, className="value-song-id"),
                    html.Div(item[0], className="value-subject"),
                    html.Div(item[1], className="value-genre"),
                    html.Div(item[2], className="value-release"),
                    html.Div(item[3], className="value-type"),
            ]) 
        ]
        
        return {"display": "flex"}, True, output_list     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False, [] 
    
    return {"display": "none"}, False, []


# 콜백 설정
@dash_app1.callback(
    [Output("modal-add-song", "style"), Output("modal-state-add-song", "data")],
    [Input("open-modal-btn-add-song", "n_clicks"), Input("close-modal-btn-add-song", "n_clicks")],
    [State("modal-add-song", "style"), State("modal-state-add-song", "data")],
)
def toggle_modal_song_add(open_clicks, close_clicks, style, is_open):
    if open_clicks and (not is_open): 
        return {"display": "flex"}, True     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False 
    
    return {"display": "none"}, False


# 콜백 설정
@dash_app1.callback(
    [Output("modal-score", "style", allow_duplicate=True), 
     Output("modal-state-score", "data", allow_duplicate=True)],
     
    [Input("open-modal-btn-score", "n_clicks"), 
     Input("close-modal-btn-score", "n_clicks")],
    
    [State("modal-score", "style"), 
     State("modal-state-score", "data")],

     prevent_initial_call=True
)
def toggle_modal_score(open_clicks, close_clicks, style, is_open):
    if open_clicks and (not is_open): 
        return {"display": "flex"}, True     
    
    if close_clicks and is_open: 
        return {"display": "none"}, False 
    
    return {"display": "none"}, False


@dash_app1.callback(  
    [Output("output-container-score", "children", allow_duplicate=True),
     Output("modal-score", "style", allow_duplicate=True), 
     Output("modal-state-score", "data", allow_duplicate=True), 
     Output("complete-btn-score", "n_clicks"),
     Output("output-container-graph", "children"),],

    [Input({"type": "score-input-activae", "index": ALL}, "value"),
     Input({"type": "score-input-streaming", "index": ALL}, "value"),
     Input({"type": "score-input-listener", "index": ALL}, "value"),
     Input("complete-btn-score", "n_clicks")],

     [State("modal-score", "style"), 
      State("modal-state-score", "data"),
      State('value-artist', 'data'),
      State('value-song', 'data')],
         # 모든 score-input의 value를 Input으로 사용
    prevent_initial_call=True
)
def update_output_score(input_values_activae, input_values_streaming, input_values_listener, complete_clicks, style, is_open, data_artist, data_song):
    def create_graph(output_activae, data_artist): 
        n = ', '.join([dic['name'] for dic in data_artist])
        s = data_song['subject']
        return dcc.Graph(
                id='xgb-pred-graph',
                figure={
                    'data': [
                        {
                            'x': list(range(1, len(output_activae)+1)), 
                            'y': output_activae, 
                            'type': 'line', 
                            'name': 'Example Line',
                            'line': {
                                    'color': 'gray'  # 선 색깔을 빨간색으로 설정
                                        },
                            },
                    ],
                                        
                    'layout': {
                        'title': f"{n} - {s}",
                        'yaxis': {
                            'tickformat': ',d'  # 천 단위 구분 없이 정수 형태로 표시
                        }
                    }
                }
            )

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, create_graph([0, 0, 0, 0, 0])
    

    # 콜백이 호출된 이유 파악
    triggered = ctx.triggered[0]
    # triggered_input_id = triggered["prop_id"].split(".")[0]  # 어떤 Input이 트리거됐는지 확인

    # 모든 인풋의 값을 받아옴

    output_activae = [v for v in input_values_activae if v is not None]
    output_streaming = [v for v in input_values_streaming if v is not None]
    output_listener = [v for v in input_values_listener if v is not None]

    output = html.Div(
        children=[
            html.Span(f"Day {len(output_activae)}", className="item-score"),
            html.Span(f"일감상자수  |  {output_activae[-1]}", className="item-score"),
            html.Span(f"누적 스트리밍수  |  {output_streaming[-1]}", className="item-score"),
            html.Span(f"누적 감상자수  |  {output_listener[-1]}", className="item-score"),
            html.Button("X", id="delete-btn-score", className="delete-btn")
        ]
    )

    if complete_clicks and (len(output_activae) == len(output_streaming) == len(output_listener)): 
        return output, {"display": "none"}, False, 0, create_graph(output_activae, data_artist) 
    
    return [], dash.no_update, dash.no_update, 0, create_graph([0, 0, 0, 0, 0])


@dash_app1.callback(
    [
        Output("output-container-score", "children", allow_duplicate=True),
        Output({"type": "score-input-activae", "index": ALL}, "value"),
        Output({"type": "score-input-streaming", "index": ALL}, "value"),
        Output({"type": "score-input-listener", "index": ALL}, "value"),
    ],
    [Input("delete-btn-score", "n_clicks")],
    prevent_initial_call="initial_duplicate"
)
def handle_delete_artist(*args):
    # Determine which button was clicked
    ctx = callback_context
    triggered = ctx.triggered[0]['value']

    # Clear the output and checklist
    if triggered:
        return [html.Div()], [None]*30, [None]*30, [None]*30
    

# 서버 실행
if __name__ == '__main__':
    app.debug = True 
    app.run() 
