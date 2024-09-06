from dash import html, dcc, Input, Output, State, ctx, ALL, MATCH
from dash import callback_context
import dash
import requests
import json
import math

def register_callbacks(dash_app1):
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


    # 아티스트 정보 데이터 
    artist_data = {
        '000001': ['이름 1', '1999-02-15', "2020-08-09", "2020", '그룹', "남성", '댄스', "소속사1"],
        '000002': ['이름 2', '1997-06-10', "2016-12-29", "2010", '솔로', "여성", '발라드', "소속사2"],
        '000003': ['이름 3', '1980-11-22', "2023-01-05", "2020", '그룹', "혼성", '댄스', '소속사3']
    }

    @dash_app1.callback(
        [
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
            Output('output-container-artist-checklist', 'children'),
            Output("output-container-page-info-artist", "children"),
            Output('current-page-artist', 'data'),
        ],
        [
            Input("open-modal-btn-artist", "n_clicks"),
            Input("close-modal-btn-artist", "n_clicks"),
            Input("prev-button-artist", "n_clicks"),
            Input("next-button-artist", "n_clicks"),
            Input("search-input-artist", "n_submit"),
            Input("btn-search-artist", "n_clicks"),
            Input("search-input-artist", "value")
        ],
        [
            State("modal-artist", "style"),
            State("modal-state-artist", "data"),
            State('current-page-artist', 'data'),
            State('total-page-artist', 'data')
        ],
        prevent_initial_call="initial_duplicate",
    )
    def handle_modal_and_update_output_artist(open_clicks, close_clicks, prev_clicks, next_clicks, submit, search_clicks, search_value, style, is_open, current_page, total_page):
        
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            artists = data.get('artists', {})
            total = data.get('total', 0)
            total_page = -(-total // per_page)
            
            output_div = [
                dcc.Checklist(
                    id='artist-checklist',
                    className='checklist',
                    options=[
                        {   
                            "label": html.Div([
                                html.Span(key, className="data-artist-id"),
                                html.Span(get_value(artist[0], default='N/A'), className="data-artist-name"),
                                html.Span(get_value(artist[1], default='N/A'), className="data-artist-birth"),
                                html.Button("👀", id={"type":"open-modal-btn-info-artist", "index":key}, className="btn-more")
                            ],  className='checklist-item'),
                            "value": [key] + artist,
                        }
                        for key, artist in artists.items()
                    ],
                    value=[],
                    labelStyle={"display": "flex", "align-items": "center"}
                )
            ]

            output_div_page = [
                            html.Span(f"{current_page_tmp}"),
                            html.Span("/"),
                            html.Span(f"{total_page}")
                            ]
            
            return output_div, output_div_page
        
        triggered = [p['prop_id'] for p in callback_context.triggered][0]
        
        current_page_tmp = current_page
        
        if 'prev-button-artist' in triggered: 
            if current_page > 1:
               current_page_tmp -= 1    
             
        if 'next-button-artist' in triggered: 
            if current_page < total_page:
                current_page_tmp += 1 

        if ('open-modal-btn-artist' in triggered) or ('prev-button-artist' in triggered) or ('next-button-artist' in triggered):
            per_page = 10 
            url = f'http://localhost:5000/artists?page={current_page_tmp}&per_page={per_page}'
            
            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')


        
        if ('search-input-artist.n_submit' in triggered) or ('btn-search-artist' in triggered):
            per_page = 10 

            if search_value.isdigit(): 
                url = f'http://localhost:5000/artists?page={current_page_tmp}&per_page={per_page}&artist_id={search_value}'
            elif type(search_value) == str: 
                url = f'http://localhost:5000/artists?page={current_page_tmp}&per_page={per_page}&name={search_value}'

            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-artist' in triggered:
            return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update
        
        return style, is_open, dash.no_update, dash.no_update, dash.no_update


    @dash_app1.callback(
        [
            Input("search-input-artist", "n_submit"),
            Input("btn-search-artist", "n_clicks")
        ],
        
        prevent_initial_call="initial_duplicate"
    )
    def handle_search_artist(*args):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['value']

        # Clear the output and checklist
        if triggered:
            return [], [], []


    @dash_app1.callback(
        [
            Output('output-container-artist', 'children', allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
        ],
        [
            Input('load-btn-artist', 'n_clicks'),
        ],
        [
            State('artist-checklist', 'value'),
            State('model-artist', "data"),
            State("modal-artist", "style"),
            State("modal-state-artist", "data"),
        ],
        prevent_initial_call=True,
    )
    def handle_load_button_artist(load_clicks, checked_values, train_data_artist, style, is_open):
        if not checked_values:
            return dash.no_update, checked_values, dash.no_update, dash.no_update
        
        for val in checked_values:
            train_data_artist.append({"id": val[0], "name": val[1]})

        print(train_data_artist)
        
        output_list = [
            html.Div(
                className="span-output-artist",
                children=[
                    html.Span(dic['name'], className='item-name'),
                ]
            ) for dic in train_data_artist
        ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]


        return output_list, train_data_artist, {"display": "none"}, False,



    @dash_app1.callback(
        [
            Output("output-container-artist", "children", allow_duplicate=True),
            Output("artist-checklist", "value", allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
        ],
        [Input("delete-btn-artist", "n_clicks")],
        [State('model-artist', "data")],
        prevent_initial_call="initial_duplicate"
    )
    def handle_delete_artist(*args):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['value']

        # Clear the output and checklist
        if triggered:
            return [], [], []


    # 콜백 설정
    @dash_app1.callback(
        [Output("modal-info-artist", "style"), 
        Output("modal-state-info-artist", "data"),
        Output("output-container-artist-info", "children"),],

        [Input({"type":"open-modal-btn-info-artist", "index":ALL}, "n_clicks")]
        + [ Input("close-modal-btn-info-artist", "n_clicks")],

        [State("modal-info-artist", "style"), 
        State("modal-state-info-artist", "data")],
    )
    def toggle_modal_artist_info(*args):

        def get_value(d, key, default='N/A'):
            value = d.get(key, default)
            # 확인: value가 nan인지 확인
            if isinstance(value, float) and math.isnan(value):
                return default
            return value
        
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0] if ctx.triggered else None

        open_clicks = triggered['value']
        close_clicks = args[-3]
        is_open = args[-1]

        if open_clicks and (not is_open): 

            json_string = triggered['prop_id'].split(".")[0]
            artist_id = json.loads(json_string)['index']


            # Flask API URL
            url = f'http://localhost:5000/artists/{artist_id}'


            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                artist = response.json()  # JSON 형식으로 응답 데이터 파싱

                output_list = [
                    html.Div([
                            html.Div(get_value(artist, "name", default='N/A'), className="value-name"),
                            html.Div(get_value(artist, "birth", default='N/A'), className="value-birth"),
                            html.Div(get_value(artist, "debut", default='N/A'), className="value-debut"),
                            html.Div(get_value(artist, "activity", default='N/A'), className="value-activity"),
                            html.Div(get_value(artist, "artist_type", default='N/A'), className="value-type"),
                            html.Div(get_value(artist, "gender", default='N/A'), className="value-gender"),
                            html.Div(get_value(artist, "genre", default='N/A'), className="value-agency"),
                            html.Div(get_value(artist, "agency", default='N/A'), className="value-genre"),
                    ]) 
                ]
                
                return {"display": "flex"}, True, output_list     
            
            except requests.RequestException as e:
                return {"display": "flex"}, True, [] 



        
        if close_clicks and is_open: 
            return {"display": "none"}, False, [] 
        
        return {"display": "none"}, False, []


    # 콜백 설정

    @dash_app1.callback(
        [Output("modal-add-artist", "style"), 
         Output("modal-state-add-artist", "data")],
        
        [Input("open-modal-btn-add-artist", "n_clicks"), 
         Input("close-modal-btn-add-artist", "n_clicks"),
         Input("add-btn-artist", "n_clicks"),
         Input({'type': "input-artist", 'index': ALL}, 'value')],
        
        [State("modal-add-artist", "style"), 
         State("modal-state-add-artist", "data")],
    )
    def toggle_modal_artist_add(open_clicks, close_clicks, add_clicks, input_values, style, is_open):
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

        if ("open-modal-btn-add-artist" in triggered) and (not is_open): 
            return {"display": "flex"}, True     
        
        if ("close-modal-btn-add-artist" in triggered) and is_open: 
            return {"display": "none"}, False 
        
        if ("add-btn-artist" in triggered) and is_open: 
            keys = ['artist_id', 'name', 'birth', 'debut', 'activity', 'artist_type', 'gender', 'artist_genre', 'agency']
            data = {keys[i]: v for i, v in enumerate(input_values)}
            
            try:
                url = "http://localhost:5000/artists"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                # 요청이 성공했는지 확인
                if response.status_code == 201:
                    response_data = response.json()  # JSON 데이터 파싱
                    artist_info = response_data['artist']  # 응답에서 artist 정보 추출
                    artist_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {artist_message}")
                    print(f"Added Artist - ID: {artist_info['artist_id']}, Name: {artist_info['name']}")
                else:
                    print(f"Failed to add artist. Status code: {response.status_code}")
            
            except requests.RequestException as e:
                print(f"Error sending data: {e}")
    
            return {"display": "none"}, False
        
        return dash.no_update, dash.no_update


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
        State('model-artist', 'data'),
        State('value-song', 'data')],
            # 모든 score-input의 value를 Input으로 사용
        prevent_initial_call=True
    )
    def update_output_score(input_values_activae, input_values_streaming, input_values_listener, complete_clicks, style, is_open, data_artist, data_song):
        def create_graph(output_activae, data_artist, data_song): 
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
            return dash.no_update, dash.no_update, dash.no_update, create_graph([0, 0, 0, 0, 0], [], {})
        

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
            return output, {"display": "none"}, False, 0, create_graph(output_activae, data_artist, data_song) 
        
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