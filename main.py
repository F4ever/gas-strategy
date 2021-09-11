import functools

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from web3 import Web3
import plotly.graph_objects as go


web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/b11919ed73094499a35d1b3fa338322a"))


@functools.lru_cache()
def get_price_stats():
    last_block = 'latest'
    gas_prices = []
    requests_num = 50

    # 2 weeks will be fetched
    # 45 * 1024 block / 13 seconds = 1 week
    for i in range(requests_num):
        stats = web3.eth.fee_history(1024, last_block)
        last_block = stats['oldestBlock'] - 2

        gas_prices = stats['baseFeePerGas'] + gas_prices

    return gas_prices, list(range(stats['oldestBlock'], stats['oldestBlock'] + (1024 + 1) * requests_num))


def calc_gas_percentile(gas_prices, block_nums, percentile, block_in_past):
    x, y = [], []

    for block_num in block_nums:
        if block_num - block_nums[0] < block_in_past:
            continue

        x.append(block_num)

        current_block_position = block_num - block_nums[0]
        y.append(calc_percentile(gas_prices[current_block_position - block_in_past: current_block_position], percentile))

    return x, y


def calc_percentile(values_list, percentile):
    import numpy as np
    a = np.array(values_list)
    return np.percentile(a, percentile)


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.P("Percentile"),
    dcc.Input(
        id='percentile',
        type='number',
        min=0,
        max=100,
        value=20
    ),
    html.P("Block in pass"),
    dcc.Input(
        id='blocks_count',
        type='number',
        value=1000
    )
])


@app.callback(
    Output("graph", "figure"),
    [Input("percentile", "value"), Input("blocks_count", "value")]
)
def customize_width(percentile, blocks_count):
    gas_prices, block_nums = get_price_stats()

    x1, y1 = block_nums[blocks_count:], gas_prices[blocks_count:]
    x2, y2 = calc_gas_percentile(gas_prices, block_nums, percentile, blocks_count)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x1,
            y=y1,
            name='Current gas price',
            line=dict(color='firebrick')
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x2,
            y=y2,
            name='Recommended price',
            line=dict(color='blue', width=2)
        )
    )

    return fig


app.run_server(debug=True)
