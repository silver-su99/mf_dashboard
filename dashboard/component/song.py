from dash import html, dcc

# 모달3 - 곡 목록 모달창   
def create_modal_song_list(): 
    
    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    song_data = {
        '000001': ['제목 1', '2021-02-15'],
        '000002': ['제목 2', '2020-06-10'],
        '000003': ['제목 3', '2019-11-22']
    }

    return html.Div(
                className="modal-list",
                id="modal-song",
                children=[
                    
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-list",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 목록", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-song", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="곡 ID 또는 아티스트 ID를 입력해주세요.", className="search-input"),
                                    html.Button("🔍", className="btn-search")
                                ] 
                            ),
                            # 새로운 중앙 컨텐츠: 인덱스와 리스트
                            html.Div(
                                className="modal-content",
                                children=[
                                    # 인덱스 헤더
                                    html.Div(
                                        className="index-header-list",
                                        children=[
                                            html.Span("곡 ID", className="index-song-id"),
                                            html.Span("제목", className="index-subject"),
                                            html.Span("발매일", className="index-release"),
                                            html.Span("정보", className="index-0"),
                                        ]
                                    ),
                                    # 데이터 리스트 항목 (샘플 데이터)
                                    html.Div([
                                            dcc.Checklist(
                                                id='song-checklist',  # ID를 추가합니다.
                                                className='checklist',
                                                options=[
                                                    {   
                                                        "label": html.Div([
                                                            html.Span(key, className="data-song-id"),
                                                            html.Span(song_info[0], className="data-song-subject"),
                                                            html.Span(song_info[1], className="data-song-release"),
                                                            html.Button("👀", id=f"open-modal-btn-info-song-{key}", className="btn-more")
                                                        ], style={'display': 'flex'}),
                                                        "value": key,
                                                    }
                                                    for key, song_info in song_data.items()
                                                ],
                                                value=[],  # 초기값을 빈 리스트로 설정
                                                labelStyle={"display": "flex", "align-items": "center"}
                                                )
                                        ]
                                    )
                                ]
                            ),                           
                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("곡 정보 추가", id="open-modal-btn-add-song", className="btn-delete"),
                                    html.Button("불러오기", id='load-btn-song', className="btn-load")
                                ]
                            ),

                            create_modal_song_info(),
                            create_modal_song_add()

                        ]
                    )
                ]
            )

# 모달3-1 - 곡 정보 모달창 
def create_modal_song_info(): 
    return  html.Div(
                className="modal-info",
                id="modal-info-song",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-info",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 정보", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-info-song", className="btn-close-modal")
                                ]
                            ),
                            

                            html.Div(
                                className="modal-content-info",
                                children=[
                                    # 인덱스와 값을 포함하는 Flexbox 컨테이너
                                    html.Div(
                                        className="index-value-container",
                                        children=[
                                            # 인덱스 열
                                            html.Div(
                                                className="index-column",
                                                children=[
                                                    html.Div("곡 ID", className="index-song-id-info"),
                                                    html.Div("제목", className="index-subject-info"),
                                                    html.Div("발매일", className="index-release-info"),
                                                    html.Div("장르", className="index-genre-info"),
                                                    html.Div("앨범타입", className="index-type-info")
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                id='output-container-song-info',
                                                className="value-column",
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )

# 모달3-2 - 곡 추가 모달창 
def create_modal_song_add(): 
    return  html.Div(
                className="modal-add",
                id="modal-add-song",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-add",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 추가", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-add-song", className="btn-close-modal")
                                ] 
                            ),
                            
                            html.Div(
                                className="modal-content-info",
                                children=[
                                    # 인덱스와 값을 포함하는 Flexbox 컨테이너
                                    html.Div(
                                        className="index-value-container",
                                        children=[
                                            # 인덱스 열
                                            html.Div(
                                                className="index-column",
                                                children=[
                                                    html.Div("곡 ID", className="index-song-id-info"),
                                                    html.Div("제목", className="index-subject-info"),
                                                    html.Div("장르", className="index-genre-info"),
                                                    html.Div("발매일", className="index-release-info"),
                                                    html.Div("앨범타입", className="index-type-info")
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                className="value-column",
                                                children=[
                                                    dcc.Input(className="input-song-id", type="text"),
                                                    dcc.Input(className="input-subject", type="text"),
                                                    dcc.Input(className="input-genre", type="text"),
                                                    dcc.Input(className="input-release", type="text"),
                                                    dcc.Input(className="input-type", type="text"),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            
                            # 푸터: 추가 버튼 
                            html.Div(
                                className="modal-footer-add",
                                children=[
                                    html.Button("추가", className="btn-add"),
                                ]
                            ),
                        ]
                    )
                ]
            )