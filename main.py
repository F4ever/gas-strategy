import functools
import os

import dash
import numpy
from dash import html, dcc
from dash.dependencies import Input, Output
from web3 import Web3
import plotly.graph_objects as go


INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))


@functools.lru_cache()
def get_price_stats(days):
    last_block = 'latest'
    gas_prices = []

    # 6 * 1024 block / 13 seconds ~ one day
    for i in range(6 * days):
        stats = web3.eth.fee_history(1024, last_block)
        last_block = stats['oldestBlock'] - 2

        gas_prices = stats['baseFeePerGas'] + gas_prices

    return [gas_price / 10**9 for gas_price in gas_prices], list(range((1024 + 1) * 6 * days))


def calc_gas_percentile(gas_prices, block_nums, percentile, block_in_past):
    x, y = [], []

    for block_num in block_nums:
        # Count percentile for each 70 block (15 minutes) to increase perf
        if block_num % 70 != 0:
            continue

        if block_num - block_nums[0] < block_in_past:
            continue

        x.append(block_num)

        current_block_position = block_num - block_nums[0]
        y.append(calc_percentile(gas_prices[current_block_position - block_in_past: current_block_position], percentile))

    return x, y


def calc_percentile(values_list, percentile):
    a = numpy.array(values_list)
    return numpy.percentile(a, percentile)


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.P("Days to fetch"),
    dcc.Input(
        id='days',
        type='number',
        min=0,
        value=8,
    ),
    html.P("Percentile"),
    dcc.Input(
        id='percentile',
        type='number',
        min=0,
        max=100,
        value=20
    ),
    html.P("Blocks count in past 1 (blue chart)"),
    dcc.Input(
        id='blocks_count_1',
        type='number',
        # 2 days
        value=6600
    ),
    html.P("Blocks count in past 2 (green chart)"),
    dcc.Input(
        id='blocks_count_2',
        type='number',
        # 2 days
        value=6600 * 4
    )
])


@app.callback(
    Output("graph", "figure"),
    [
        Input("days", "value"),
        Input("percentile", "value"),
        Input("blocks_count_1", "value"),
        Input("blocks_count_2", "value"),
    ]
)
def customize_width(days, percentile, blocks_count_1, blocks_count_2):
    gas_prices, block_nums = get_price_stats(days)

    x1, y1 = block_nums, gas_prices
    x2, y2 = calc_gas_percentile(gas_prices, block_nums, percentile, blocks_count_1)
    x3, y3 = calc_gas_percentile(gas_prices, block_nums, percentile, blocks_count_2)

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
            name='Recommended price 1 (default: 1 day)',
            line=dict(color='blue', width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x3,
            y=y3,
            name='Recommended price 2 (default: 4 days)',
            line=dict(color='green', width=2)
        )
    )

    return fig


app.run_server(debug=True)
