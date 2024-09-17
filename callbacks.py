from dash import html, dcc, Input, Output, State, ctx, ALL, MATCH, dash_table, callback_context
import dash
import requests
import json
import math
import plotly.graph_objs as go


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


    @dash_app1.callback(
        [
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
            Output('output-container-artist-checklist', 'children'),
            Output("output-container-page-info-artist", "children"),
            Output('current-page-artist', 'data'),
            Output("search-input-artist", "value", allow_duplicate=True)
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

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp, search_value

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

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp, search_value

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-artist' in triggered:
            return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update, ""
        
        return style, is_open, dash.no_update, dash.no_update, dash.no_update, search_value




    @dash_app1.callback(
        [
            Output('output-container-artist', 'children', allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
            Output("search-input-artist", "value", allow_duplicate=True)
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
            return dash.no_update, checked_values, dash.no_update, dash.no_update, ""
        
        for val in checked_values:
            train_data_artist.append({"id": val[0], "name": val[1]})
        
        output_list = [
            html.Div(
                className="span-output-artist",
                children=[
                    html.Span(dic['name'], className='item-name'),
                ]
            ) for dic in train_data_artist
        ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]


        return output_list, train_data_artist, {"display": "none"}, False, ""



    @dash_app1.callback(
        [
            Output("output-container-artist", "children", allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("search-input-artist", "value", allow_duplicate=True)
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
            return [], [], ""


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
                            html.Div(get_value(artist, "activity_year", default='N/A'), className="value-activity"),
                            html.Div(get_value(artist, "activity_type", default='N/A'), className="value-type"),
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
            keys = ['artist_id', 'name', 'birth', 'debut', 'activity_year', 'activity_type', 'gender', 'artist_genre_main', 'agency']
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




    @dash_app1.callback(
        [
            Output("modal-song", "style"),
            Output("modal-state-song", "data"),
            Output("output-container-song-checklist", "children", allow_duplicate=True),
            Output("output-container-page-info-song", "value", allow_duplicate=True),
            Output('current-page-song', 'data'),
            Output("search-input-song", "value", allow_duplicate=True)
        ],
        [
            Input("open-modal-btn-song", "n_clicks"),
            Input("close-modal-btn-song", "n_clicks"),
            Input("prev-button-song", "n_clicks"),
            Input("next-button-song", "n_clicks"),
            Input("search-input-song", "n_submit"),
            Input("btn-search-song", "n_clicks"),
            Input("search-input-song", "value")
        ],
        [
            State("modal-song", "style"),
            State("modal-state-song", "data"),
            State('current-page-song', 'data'),
            State('total-page-song', 'data')
        ],
            prevent_initial_call="initial_duplicate",

    )
    def handle_modal_and_update_output(open_clicks, close_clicks, prev_clicks, next_clicks, submit, search_clicks, search_value, style, is_open, current_page, total_page):
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            songs = data.get('songs', {})
            total = data.get('total', 0)
            total_page = -(-total // per_page)
            
            output_div = [
                dcc.Checklist(
                    id='song-checklist',
                    className='checklist',
                    options=[
                        {   
                            "label": html.Div([
                                html.Span(key, className="data-song-id"),
                                html.Span(get_value(song[0], default='N/A'), className="data-song-name"),
                                html.Span(get_value(song[1], default='N/A'), className="data-song-birth"),
                                html.Button("👀", id={"type":"open-modal-btn-info-song", "index":key}, className="btn-more")
                            ],  className='checklist-item'),
                            "value": [key] + song,
                        }
                        for key, song in songs.items()
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
        
        if 'prev-button-song' in triggered: 
            if current_page > 1:
               current_page_tmp -= 1    
             
        if 'next-button-song' in triggered: 
            if current_page < total_page:
                current_page_tmp += 1 

        if ('open-modal-btn-song' in triggered) or ('prev-button-song' in triggered) or ('next-button-song' in triggered):
            per_page = 10 
            url = f'http://localhost:5000/songs?page={current_page_tmp}&per_page={per_page}'
            
            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp, search_value

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')
        
        if ('search-input-song.n_submit' in triggered) or ('btn-search-song' in triggered):
            per_page = 10 

            if search_value.isdigit(): 
                url = f'http://localhost:5000/songs?page={current_page_tmp}&per_page={per_page}&song_id={search_value}'
            elif type(search_value) == str: 
                url = f'http://localhost:5000/songs?page={current_page_tmp}&per_page={per_page}&subject={search_value}'

            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp, search_value

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-song' in triggered:
            return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update, ""
        
        return style, is_open, dash.no_update, dash.no_update, dash.no_update, search_value


    @dash_app1.callback(
        [
            Output('output-container-song', 'children', allow_duplicate=True),
            Output('model-song', 'data', allow_duplicate=True),
            Output("modal-song", "style", allow_duplicate=True),
            Output("modal-state-song", "data", allow_duplicate=True),
            Output("search-input-song", "value", allow_duplicate=True)
        ],
        [
            Input('load-btn-song', 'n_clicks'),
        ],
        [
            State('song-checklist', 'value'),
            State('model-song', "data"),
            State("modal-song", "style"),
            State("modal-state-song", "data"),
        ],
        prevent_initial_call=True,
    )
    def handle_load_button_artist(load_clicks, checked_values, train_data_song, style, is_open):

        if not checked_values:
            return dash.no_update, checked_values, dash.no_update, dash.no_update, ""

        val = checked_values[-1]        
        train_data_song = {"song_id": val[0], "subject": val[1]}
        
        
        output_list = [
            html.Div(
                className="span-output-song",
                children=[
                    html.Span(train_data_song['subject'], className='item-subject'),
                ]
            ) 
        ] + [html.Button("X", id="delete-btn-song", className="delete-btn")]

        return output_list, train_data_song, {"display": "none"}, False, ""


    @dash_app1.callback(
        [
            Output("output-container-song", "children", allow_duplicate=True),
            Output('model-song', 'data', allow_duplicate=True),
        ],

        [Input("delete-btn-song", "n_clicks")],
        
        [State('model-song', "data")],

        prevent_initial_call="initial_duplicate"
    )
    def handle_delete_song(*args):
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
       
        [Input({"type":"open-modal-btn-info-song", "index":ALL}, "n_clicks")]
        + [ Input("close-modal-btn-info-song", "n_clicks")],
        
        [State("modal-info-song", "style"), 
        State("modal-state-info-song", "data")],
    )
    def toggle_modal_song_info(*args):

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
            song_id = json.loads(json_string)['index']


            # Flask API URL
            url = f'http://localhost:5000/songs/{song_id}'


            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                song = response.json()  # JSON 형식으로 응답 데이터 파싱

                output_list = [
                    html.Div([
                            html.Div(get_value(song, "song_id", default='N/A'), className="value-song-id"),
                            html.Div(get_value(song, "subject", default='N/A'), className="value-subject"),
                            html.Div(get_value(song, "release", default='N/A'), className="value-release"),
                            html.Div(get_value(song, "genre", default='N/A'), className="value-genre"),
                            html.Div(get_value(song, "album_type", default='N/A'), className="value-album-type"),
                            html.Div(get_value(song, "artist_name", default='N/A'), className="value-artist-name")
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
        [Output("modal-add-song", "style"), 
         Output("modal-state-add-song", "data")],
        
        [Input("open-modal-btn-add-song", "n_clicks"), 
         Input("close-modal-btn-add-song", "n_clicks"),
         Input("add-btn-song", "n_clicks"),
         Input({'type': "input-song", 'index': ALL}, 'value')],
        
        [State("modal-add-song", "style"), 
         State("modal-state-add-song", "data")],
    )
    def toggle_modal_song_add(open_clicks, close_clicks, add_clicks, input_values, style, is_open):
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

        if ("open-modal-btn-add-song" in triggered) and (not is_open): 
            return {"display": "flex"}, True     
        
        if ("close-modal-btn-add-song" in triggered) and is_open: 
            return {"display": "none"}, False 
        
        if ("add-btn-song" in triggered) and is_open: 
            keys = ['song_id', 'subject', 'release', 'genre', 'album_type', 'artist_id']
            data = {}
            for i, v in enumerate(input_values):
                if i == 3:
                    data[keys[i]] = ', '.join(v)
                else: 
                    data[keys[i]] = v 
            
            try:
                url = "http://localhost:5000/songs"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                # 요청이 성공했는지 확인
                if response.status_code == 201:
                    response_data = response.json()  # JSON 데이터 파싱
                    song_info = response_data['song']  # 응답에서 song 정보 추출
                    song_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {song_message}")
                    print(f"Added Artist - ID: {song_info['song_id']}, Name: {song_info['name']}")
                else:
                    print(f"Failed to add song. Status code: {response.status_code}")
            
            except requests.RequestException as e:
                print(f"Error sending data: {e}")
    
            return {"display": "none"}, False
        
        return dash.no_update, dash.no_update


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
        Output("output-container-graph", "children", allow_duplicate=True),
        Output({"type": "score-input-activae", "index": ALL}, "value")],

        [Input({"type": "score-input-activae", "index": ALL}, "value"),
        Input("complete-btn-score", "n_clicks")],

        [State("modal-score", "style"), 
        State("modal-state-score", "data"),
        State('model-artist', 'data'),
        State('model-song', 'data')],

        # 모든 score-input의 value를 Input으로 사용
        prevent_initial_call=True
    )
    def update_output_score(input_values_activae, complete_clicks, style, is_open, data_artist, data_song):
        def create_graph(output_activae, data_artist, data_song): 
            n = ', '.join([dic['name'] for dic in data_artist])
            s = data_song['subject']
            return dcc.Graph(
                    id='xgb-pred-graph',
                    className="xgb-pred-graph",
                    figure={
                        'data': [
                            {
                                'x': list(range(1, len(output_activae)+1)), 
                                'y': output_activae, 
                                'type': 'line', 
                                'name': '일감상자수',
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
            return dash.no_update, dash.no_update, dash.no_update, create_graph([0, 0, 0, 0, 0], data_artist, data_song), dash.no_update
        
        # 모든 인풋의 값을 받아옴
        output_activae = [v for v in input_values_activae if v]

        output = html.Div(
            children=[
                html.Span(f"Day {len(output_activae)}", className="item-score"),
                html.Span(f"일감상자수  |  {output_activae[-1]}", className="item-score"),
                html.Button("X", id="delete-btn-score", className="delete-btn")
            ]
        )

        if complete_clicks and output_activae: 

            return output, {"display": "none"}, False, 0, create_graph(output_activae, data_artist, data_song), input_values_activae
        
        return output, dash.no_update, dash.no_update, 0, create_graph(output_activae, data_artist, data_song), dash.no_update


    @dash_app1.callback(  
        [
            Output("output-container-graph", "children", allow_duplicate=True),
            Output("output-container-table", "children", allow_duplicate=True),
        ],

        [ 
            Input({"type": "score-input-activae", "index": ALL}, "value"),
            Input("pred-btn", "n_clicks") 
        ], 

        [   
            State('model-artist', 'data'), 
            State('model-song', 'data') 
        ],

        # 모든 score-input의 value를 Input으로 사용
        prevent_initial_call=True
    )
    def handle_predict_and_update_graph(input_values_activae, pred_clicks, data_artist, data_song):
        def create_graph(output_activae, preds_activae, data_artist, data_song): 
            
            s = data_song['subject']
            lst_names = [dic['name'] for dic in data_artist]
            n = ', '.join(lst_names)

            def create_data(preds_activae):
                import numpy as np 
                np_preds_activae = np.array(preds_activae)
                preds_activae_mean = list(np.mean(np_preds_activae, axis=0))

                if len(preds_activae) >= 2: 
                    d = [
                        {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae[idx][len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': f'일감상자수 예측값 ({lst_names[idx]})',
                        } for idx in range(len(preds_activae))
                    ] + \
                    [
                      {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae_mean[len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': f'일감상자수 예측값 (평균)',
                            'line': {
                                    'color': "rgba(255, 0, 0, 0.8)"  # 선 색깔을 빨간색으로 설정
                                        },
                        } 
                    ] + \
                    [go.Scatter(
                        x=[len(output_activae)],
                        y=[preds_activae_mean[len(output_activae)-1]],
                        mode='markers',
                        name="전 날 예측값",
                        marker={
                            'size': 7,
                            'symbol': 'square',  # 점 모양을 원으로 설정
                            'color': "rgba(255, 0, 0, 0.5)"      # 색상 설정
                        },
                    ) ]

                else:
                    d = [
                        {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae[0][len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': '일감상자수 예측값',
                            'line': {
                                    'color': "rgba(255, 0, 0, 0.8)"  # 선 색깔을 빨간색으로 설정
                                        },
                        } 
                         ] + \
                        [go.Scatter(
                        x=[len(output_activae)],
                        y=[preds_activae[0][len(output_activae)-1]],
                            mode='markers',
                            name="전 날 예측값",
                            marker={
                                'size': 7,
                                'symbol': 'square',  # 점 모양을 원으로 설정
                                'color': "rgba(255, 0, 0, 0.5)"      # 색상 설정
                            },
                        )] 
                return d

            return dcc.Graph(
                    id='xgb-pred-graph',
                    figure={
                        'data': create_data(preds_activae) +\
                            [ {
                                'x': list(range(1, len(output_activae)+1)), 
                                'y': output_activae, 
                                'type': 'line', 
                                'mode': 'lines+markers',  # 선과 점을 모두 표시
                                'name': '일감상자수',
                                'line': {
                                        'color': 'gray'  # 선 색깔을 빨간색으로 설정
                                        },
                            },
                        ],
                                            
                        'layout': {
                            'title': f"{n} - {s}",
                            "xaxis":{
                                'title': 'Days',
                                'tickmode': 'linear',  # 수동으로 설정
                                'tick0': 1,            # 첫 번째 틱 마크 위치
                                'dtick': 1             # 1단위로 틱 마크
                            },
                            'yaxis': {
                                'tickformat': ',d',  # 천 단위 구분 없이 정수 형태로 표시
                            'legend': {
                                'x': 1,            # x 좌표 (오른쪽으로 1)
                                'y': 1,            # y 좌표 (위쪽으로 1)
                                'xanchor': 'right', # x 기준점을 오른쪽으로 설정
                                'yanchor': 'top',   # y 기준점을 위쪽으로 설정
                            }

                            }
                        }
                    }
                )

        if not ctx.triggered:
            return dash.no_update, dash.no_update

        if pred_clicks: 
            # 모든 인풋의 값을 받아옴
            output_activae = [int(v) for v in input_values_activae if v]
            
            data = {
                "song_id": data_song['song_id'],
                "activaeUsers": output_activae,
            }

            # 요청, 응답 받아옴  
            # song_id, activaeUsers 를 요청값으로 보냄 
            try:
                url = "http://localhost:5000/predictions"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)


                if response.status_code in (201, 200):
                    response_data = response.json()  # JSON 데이터 파싱
                    preds_activae = list(response_data['pred_by_artist'].values())

                    table_dict = response_data['table_data'][0]
                    table_cols = response_data['table_data'][1]
                    
                    output_table = dash_table.DataTable(
                                                        data=table_dict, 
                                                        columns=table_cols,
                                                        page_size=11,  
                                                        style_table={'width': '50%'},  # 테이블의 너비를 50%로 설정
                                                        style_header={
                                                                        'backgroundColor': "#222222",  # 헤더의 배경색
                                                                        'color': 'white',           # 헤더의 텍스트 색
                                                                        'fontWeight': 'bold'        # 헤더 텍스트 굵게
                                                                     },
                                                        style_cell={'textAlign': 'center'},  # 셀의 텍스트 정렬
                                                        )

                else:
                    song_message = response_data.get('message')  # 응답에서 message 추출
                    print(f"Message: {song_message}")
                    print(f"Failed to add song. Status code: {response.status_code}")

            except requests.RequestException as e:
                print(f"Error sending data: {e}")

        
            return [ create_graph(output_activae, preds_activae, data_artist, data_song) ], [ output_table ]
        
        return dash.no_update, dash.no_update




    @dash_app1.callback(
        [
            Output("output-container-score", "children", allow_duplicate=True),
            Output({"type": "score-input-activae", "index": ALL}, "value", allow_duplicate=True),
        ],
        
        [Input("delete-btn-score", "n_clicks")],

        prevent_initial_call=True
    )
    def handle_delete_score(clicks_delete):
        # Clear the output and checklist
        if clicks_delete:
            return [], [None]*30
        


    @dash_app1.callback(
        [
            Output("modal-record", "style", allow_duplicate=True),
            Output("modal-state-record", "data", allow_duplicate=True),
            Output('output-container-record-checklist', 'children'),
            Output("output-container-page-info-record", "children"),
            Output('current-page-record', 'data'),
        ],
        [
            Input("open-modal-btn-record", "n_clicks"),
            Input("close-modal-btn-record", "n_clicks"),
            Input("prev-button-record", "n_clicks"),
            Input("next-button-record", "n_clicks"),
            Input("search-input-record", "n_submit"),
            Input("btn-search-record", "n_clicks"),
            Input("search-input-record", "value")
        ],
        [
            State("modal-record", "style"),
            State("modal-state-record", "data"),
            State('current-page-record', 'data'),
            State('total-page-record', 'data')
        ],
        prevent_initial_call="initial_duplicate",
    )
    def handle_modal_and_update_output_record(open_clicks, close_clicks, prev_clicks, next_clicks, submit, search_clicks, search_value, style, is_open, current_page, total_page):
        
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            records = data.get('records', {})
            total = data.get('total', 0)
            total_page = -(-total // per_page)
            
            output_div = [
                dcc.Checklist(
                    id='record-checklist',
                    className='checklist',
                    options=[
                        {   
                            "label": html.Div([
                                html.Span(key, className="data-record-id"),
                                html.Span(get_value(record[0], default='N/A'), className="data-record-subject"),
                                html.Span(get_value(record[1], default='N/A'), className="data-record-date"),
                            ],  className='checklist-item'),
                            "value": [key] + record,
                        }
                        for key, record in records.items()
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
        
        if 'prev-button-record' in triggered: 
            if current_page > 1:
               current_page_tmp -= 1    
             
        if 'next-button-record' in triggered: 
            if current_page < total_page:
                current_page_tmp += 1 

        if ('open-modal-btn-record' in triggered) or ('prev-button-record' in triggered) or ('next-button-record' in triggered):
            per_page = 10 
            url = f'http://localhost:5000/records?page={current_page_tmp}&per_page={per_page}'
            
            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')
        
        if ('search-input-record.n_submit' in triggered) or ('btn-search-record' in triggered):
            per_page = 10 

            if search_value.isdigit(): 
                url = f'http://localhost:5000/records?page={current_page_tmp}&per_page={per_page}&song_id={search_value}'
            elif type(search_value) == str: 
                url = f'http://localhost:5000/records?page={current_page_tmp}&per_page={per_page}&subject={search_value}'

            try:

                output_div, output_div_page = request_and_create_result(url)

                return {"display": "flex"}, True, output_div, output_div_page, current_page_tmp

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-record' in triggered:
            return {"display": "none"}, False, dash.no_update, dash.no_update, dash.no_update
        
        return style, is_open, dash.no_update, dash.no_update, dash.no_update



    @dash_app1.callback(
        [Output("confirm-add-record", "message"),
         Output("confirm-add-record", "displayed"),],
        
        [Input("add-btn-record", "n_clicks"),
        Input({"type": "score-input-activae", "index": ALL}, "value"),],

        [State('model-song', "data"),],

        prevent_initial_call="initial_duplicate"
    )
    def handle_add_record(add_clicks, activaeUsers, song_data):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id']
        if "add-btn-record" in triggered: 

                    # 모든 인풋의 값을 받아옴
            output_activae = [int(v) for v in activaeUsers if v is not None]

            data = {
                "song_id": song_data['song_id'],
                'subject': song_data['subject'],
                "activaeUsers": output_activae,
            }

            try:
                url = "http://localhost:5000/records"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                if response.status_code in (201, 200):
                    response_data = response.json()  # JSON 데이터 파싱
                    song_info = response_data['song']  # 응답에서 song 정보 추출
                    song_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {song_message}")
                    print(f"Added Record - ID: {song_info['song_id']}")
                    
                    return [f"{song_data['song_id']}-{song_data['subject']}: 입력값이 저장되었습니다."], True
                
                else:
                    print(f"Failed to add song. Status code: {response.status_code}")
                    return [f"{response.status_code} Error:: {song_data['song_id']}-{song_data['subject']}: 저장에 실패하였습니다."], True

            except requests.RequestException as e:
                print(f"Error sending data: {e}")

        return dash.no_update, False
    

    @dash_app1.callback(
        [
            Output('output-container-artist', 'children', allow_duplicate=True),
            Output('output-container-song', 'children', allow_duplicate=True),
            Output("output-container-score", "children", allow_duplicate=True),
            Output("model-song", "data", allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("modal-record", "style", allow_duplicate=True),
            Output("modal-state-record", "data", allow_duplicate=True),
            Output({"type": "score-input-activae", "index": ALL}, "value", allow_duplicate=True),
        ],
        [
            Input('load-btn-record', 'n_clicks'),
        ],
        [
            State('record-checklist', 'value'),
            State("modal-record", "style"),
            State("modal-state-record", "data"),

        ],
        prevent_initial_call=True,
    )
    def handle_load_button_record(load_clicks, checked_values, style, is_open):
        
        def make_list(lst):
            return lst + [None] * (30-len(lst))

        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id']

        if "load-btn-record" in triggered:

            if not checked_values:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
            val = checked_values[-1]        
            train_data_song = {"song_id": val[0], "subject": val[1]}

            # 여기서 얻은 song_id로 artist_id들을 불러오고, artist_id에 해당하는 name을 받아야 한다. 
            # song_id로 record 데이터, artist_name 응답받기 
            
            song_id = train_data_song['song_id']

            url = f'http://localhost:5000/records/{song_id}'

            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                record = response.json()  # JSON 형식으로 응답 데이터 파싱


                train_data_artist = [{"id":artist['artist_id'], "name": artist['name']} for artist in record['artists']]

                
                output_list_artist = [
                    html.Div(
                        className="span-output-artist",
                        children=[
                            html.Span(dic['name'], className='item-name'),
                        ]
                    ) for dic in train_data_artist
                ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]


                output_list_song = [
                    html.Div(
                        className="span-output-song",
                        children=[
                            html.Span(train_data_song['subject'], className='item-subject'),
                        ]
                    ) 
                ] + [html.Button("X", id="delete-btn-song", className="delete-btn")]

                output_list_score = html.Div(
                    children=[
                        html.Span(f"Day {len(record['activaeUsers'])}", className="item-score"),
                        html.Span(f"일감상자수  |  {record['activaeUsers'][-1]}", className="item-score"),
                        html.Button("X", id="delete-btn-score", className="delete-btn")
                    ]
                )

                return output_list_artist, output_list_song, output_list_score, train_data_song, train_data_artist, {"display": "none"}, False, make_list(record["activaeUsers"])
            
            except requests.RequestException as e:

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, [None]*30, [None]*30, [None]*30




