from dash import html
import dash_daq as daq

# ===== 메인 시각화 컴포넌트 =====
def create_example_graph(): 
    return html.Div(
                        children=[html.Div(className="model-btn-container",
                                           children=[
                                                        html.Button('xgb-하향', id='model-btn-1', className='button-1'),
                                                        html.Button("xgb-전체", id="model-btn-2", className="button-1"),
                                           ]),
                                    # daq.ToggleSwitch(
                                    #     id="toggle-graph",
                                    #     label='그래프 보기',
                                    #     labelPosition='bottom'
                                    # ),
                                    html.Div(id="output-container-graph", className="container-graph"),
                                    html.Div(id="output-container-table", className="container-table")
                                ]
                    )