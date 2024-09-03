from dash import html, dcc


def streaming_pred(): 
    return html.Div(children=[

            # 상단바 컴포넌트
            create_navbar(),

            # 데이터 입력 컴포넌트 
            create_data_insert(),
            
            html.Hr(className='hr-data-insert'),  # 기본 가로선 추가

            # 메인 시각화 컴포넌트 
            create_example_graph(),
            
            # ===== 모달 ===== 
            # [ 이전 기록 불러오기 ]
            create_modal_previous_record(),
            
            # [ 가수 리스트 ]
            create_modal_artist_list(),

            # [ 곡 리스트 ]
            create_modal_song_list(),

            # [ 음원 성적 입력 ]
            create_modal_score(),

            # ===== 상태 변수 =====
            # 상태 저장 컴포넌트
            create_store(),

        ])





# ===== 상단바 컴포넌트 =====
def create_navbar():
    return html.Div(
        className="navbar",
        children=[
            html.Div(
                className="navbar-title",
                children="MF",
            ),
            html.Div(
                className="navbar-dashboard-title",
                children="~ 대시보드 제목 ~",
            )
        ],
    )

# ===== 데이터 입력 컴포넌트 =====
def create_data_insert():  
    return html.Div(
        className="data-insert",
        children=[

            # 입력값 저장, 이전 기록 불러오기 버튼 
            html.Div(
                className="button-container",
                children=[
                    html.Button('입력값 저장', className='button-1'),

                    # 버튼을 클릭하여 모달을 열도록 설정
                    html.Button("이전 기록 불러오기", id="open-modal-btn-previous", className="btn-open-modal-previous"),
                ]
            ),

            # 가수 정보 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("가수 정보", className="text-artist"),
                    html.Button('+', id="open-modal-btn-artist", className='button-plus'),
                    html.Div(id='output-container-artist', className='output-container-artist')
                ]
            ),

            # 곡 정보 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("곡 정보", className="text-song"),
                    html.Button('+', id="open-modal-btn-song", className='button-plus'),
                    html.Div(id='output-container-song')
                ]
            ),

            # 음원 성적 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("음원 성적", className="text-score"),
                    html.Button('+', id="open-modal-btn-score", className='button-plus'),
                    html.Div(id='output-container-score', className='output-container-score')
                ]
            ),


            # 예측 버튼 
            html.Div(
                className="button-container-pred",
                children=[
                    html.Button('예측', className='button-pred'),
                ]
            ), 

            ])

# ===== 메인 시각화 컴포넌트 =====
def create_example_graph(): 
    return html.Div(
            id="output-container-graph",
            className="container-graph")

# ===== 모달창 컴포넌트 =====
# 모달1 - [ 이전 기록 불러오기 ]
def create_modal_previous_record(): 
    return  html.Div(
                className="modal-previous",
                id="modal-previous",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-previous",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("이전 기록 불러오기", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-previous", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="곡 ID를 입력해주세요.", className="search-input"),
                                    html.Button("🔍", className="btn-search")
                                ] 
                            ),
                            # 새로운 중앙 컨텐츠: 인덱스와 리스트
                            html.Div(
                                className="modal-content",
                                children=[
                                    # 인덱스 헤더
                                    html.Div(
                                        className="index-header",
                                        children=[
                                            html.Span("선택", className="index-check"),
                                            html.Span("곡 ID", className="index-id"),
                                            html.Span("제목", className="index-title"),
                                            html.Span("저장날짜", className="index-date"),
                                        ]
                                    ),
                                    # 데이터 리스트 항목 (샘플 데이터)
                                    html.Div(
                                        className="data-list",
                                        children=[
                                            html.Div(
                                                className="data-item",
                                                children=[
                                                    dcc.Input(type="checkbox", className="data-checkbox"),  # 체크박스 추가
                                                    html.Span("001", className="data-id"),
                                                    html.Span("샘플 곡", className="data-title"),
                                                    html.Span("2024-08-29", className="data-date"),
                                                ]
                                            ),
                                            # 여기에서 추가 항목을 더 넣을 수 있습니다.
                                        ]
                                    )
                                ]
                            ),                           
                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("삭제", className="btn-delete"),
                                    html.Button("불러오기", className="btn-load")
                                ]
                            )
                        ]
                    )
                ]
            )

# 모달2 - 아티스트 목록 모달창 
def create_modal_artist_list(): 

    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    artist_data = {
        '000001': ['이름 1', '1999-02-15'],
        '000002': ['이름 2', '1997-06-10'],
        '000003': ['이름 3', '1980-11-22']
    }

    return  html.Div(
                className="modal-list",
                id="modal-artist",
                children=[
                    
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-list",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 목록", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-artist", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="아티스트 ID를 입력해주세요.", className="search-input"),
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
                                            html.Span("아티스트 ID", className="index-artist-id"),
                                            html.Span("이름", className="index-name"),
                                            html.Span("생년월일", className="index-birth"),
                                            html.Span("정보", className="index-0"),
                                        ]
                                    ),
                                    # 데이터 리스트 항목 (샘플 데이터)
                                    html.Div([
                                            dcc.Checklist(
                                                id='artist-checklist',  # ID를 추가합니다.
                                                className='checklist',
                                                options=[
                                                    {   
                                                        "label": html.Div([
                                                            html.Span(key, className="data-artist-id"),
                                                            html.Span(artist_info[0], className="data-artist-name"),
                                                            html.Span(artist_info[1], className="data-artist-birth"),
                                                            html.Button("👀", id=f"open-modal-btn-info-artist-{key}", className="btn-more")
                                                        ], style={'display': 'flex'}),
                                                        "value": key,
                                                    }
                                                    for key, artist_info in artist_data.items()
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
                                    html.Button("아티스트 정보 추가", id="open-modal-btn-add-artist", className="btn-delete"),
                                    html.Button("불러오기", id='load-btn-artist', className="btn-load")
                                ]
                            ),

                            create_modal_artist_info(),
                            create_modal_artist_add()

                        ]
                    )
                ]
            )

# 모달2-1 - 아티스트 정보 모달창 
def create_modal_artist_info(): 
    return  html.Div(
                className="modal-info",
                id="modal-info-artist",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-info",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 정보", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-info-artist", className="btn-close-modal")
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
                                                    html.Div("아티스트 ID", className="index-artist-id-info"),
                                                    html.Div("이름", className="index-name-info"),
                                                    html.Div("생년월일", className="index-birth-info"),
                                                    html.Div("데뷔일", className="index-debut-info"),
                                                    html.Div("활동년대", className="index-activity-info"),
                                                    html.Div("유형", className="index-type-info"),
                                                    html.Div("성별", className="index-gender-info"),
                                                    html.Div("주장르", className="index-artist-genre-info"),
                                                    html.Div("소속사", className="index-agency-info"),
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                id='output-container-artist-info',
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

# 모달2-2 - 아티스트 추가 모달창 
def create_modal_artist_add(): 
    return  html.Div(
                className="modal-add",
                id="modal-add-artist",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-add",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 추가", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-add-artist", className="btn-close-modal")
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
                                                    html.Div("아티스트 ID", className="index-artist-id-info"),
                                                    html.Div("이름", className="index-name-info"),
                                                    html.Div("생년월일", className="index-birth-info"),
                                                    html.Div("데뷔일", className="index-debut-info"),
                                                    html.Div("활동년대", className="index-activity-info"),
                                                    html.Div("유형", className="index-type-info"),
                                                    html.Div("성별", className="index-gender-info"),
                                                    html.Div("주장르", className="index-artist-genre-info"),
                                                    html.Div("소속사", className="index-agency-info"),
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                className="value-column",
                                                children=[
                                                    dcc.Input(className="input-artist-id", type="text"),
                                                    dcc.Input(className="input-name", type="text"),
                                                    dcc.Input(className="input-birth", type="text"),
                                                    dcc.Input(className="input-debut", type="text"),
                                                    dcc.Input(className="input-activity", type="text"),
                                                    dcc.Input(className="input-type", type="text"),
                                                    dcc.Input(className="input-gender", type="text"),
                                                    dcc.Input(className="input-artist-genre", type="text"),
                                                    dcc.Input(className="input-agency", type="text"),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            
                            # 푸터: 삭제 버튼과 불러오기 버튼
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

# 모달4 - 성적 입력 모달창 
def create_modal_score(): 
    return  html.Div(
                className="modal-score",
                id="modal-score",
                children=[ 
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-score",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("음원 성적 입력", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-score", className="btn-close-modal")
                                ]
                            ),


                            html.Div(
                                className="modal-content-score",
                                children=[
                                    html.Div(
                                        className="score-set",
                                        children=[
                                            html.Span(f"{i+1}일", className="score-index"),  # 인덱스 표시
                                            dcc.Input(id={"type": "score-input-activae", "index": f"{i+1}-1"}, type="text", className="score-input", placeholder=f"일 감상자수"),  # 첫 번째 인풋
                                            dcc.Input(id={"type": "score-input-streaming", "index": f"{i+1}-1"}, type="text", className="score-input", placeholder=f"누적 스트리밍수"),  # 두 번째 인풋
                                            dcc.Input(id={"type": "score-input-listener", "index": f"{i+1}-1"}, type="text", className="score-input", placeholder=f"누적 감상자수"),  # 세 번째 인풋
                                        ]
                                    ) for i in range(30)  # 30개의 세트를 생성
                                ]
                            ),


                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("완료", id='complete-btn-score', className="btn-complete")
                                ]
                            )
                        ] 
                    )
                ]
            )                   

# ===== 상태 저장 컴포넌트 =====
def create_store():
    return html.Div(
        children=[
            dcc.Store(id='modal-state-previous', data=False),
            dcc.Store(id='modal-state-artist', data=False),
            dcc.Store(id='modal-state-info-artist', data=False),
            dcc.Store(id='modal-state-add-artist', data=False),
            dcc.Store(id='modal-state-song', data=False),
            dcc.Store(id="modal-state-info-song", data=False),
            dcc.Store(id='modal-state-add-song', data=False),
            dcc.Store(id='modal-state-score', data=False),
            
            dcc.Store(id='value-artist', data=[]),
            dcc.Store(id='value-song', data={}),
            dcc.Store(id='value-score', data={})
        ]
    )
