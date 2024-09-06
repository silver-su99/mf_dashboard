from dash import html, dcc
from .artist import create_modal_artist_list
from .song import create_modal_song_list
from .score import create_modal_score
from .prediction import create_example_graph


def load_component(): 
    return html.Div(children=[

            # 상단바 컴포넌트
            create_navbar(),

            # 데이터 입력 컴포넌트 
            create_data_insert(),
            
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

            
            # 스크립트 추가
            dcc.Location(id="url", refresh=False),
            html.Script(src="/assets/scroll.js"),

        ])





# ===== 상단바 컴포넌트 =====
def create_navbar():
    return html.Div(
        id='navbar',
        className="navbar",
        children=[
            html.A(
                id='navbar-title',
                className="navbar-title",
                href="#",
                children="MF",
            ),
            html.Div(
                className="navbar-dashboard-title",
                    children=[
                                html.A("데이터 입력", href="#", className="link-class", id='link-class-1'),
                                html.A("예측 결과", href="#output-container-graph", className="link-class", id='link-class-2'),
                            ]
            )
        ],
    )

# ===== 데이터 입력 컴포넌트 =====
def create_data_insert():  
    return html.Div(
        id='data-insert',
        className="data-insert",
        children=[

            # 입력값 저장, 이전 기록 불러오기 버튼 
            html.Div(
                className="button-container",
                children=[
                    html.Button('입력값 저장', className='button-1'),

                    # 버튼을 클릭하여 모달을 열도록 설정
                    html.Button("이전 기록 불러오기", id="open-modal-btn-previous", className="button-1"),
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
                    html.Button('일감상자수 예측', className='button-pred'),
                ]
            ), 

            ])

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
            
            dcc.Store(id='value-song', data={}),
            dcc.Store(id='value-score', data={}),

            dcc.Store(id='model-artist', data=[]),

            dcc.Store(id='current-page-artist', data=1),
            dcc.Store(id='total-page-artist', data=100)
        ]
    )
