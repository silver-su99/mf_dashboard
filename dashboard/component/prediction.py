from dash import html, dcc

# ===== 메인 시각화 컴포넌트 =====
def create_example_graph(): 
    return html.Div(
            id="output-container-graph",
            className="container-graph")