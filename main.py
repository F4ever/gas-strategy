import functools
import datetime

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from web3 import Web3
import plotly.graph_objects as go


web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/b11919ed73094499a35d1b3fa338322a"))


@functools.lru_cache()
def get_blocks_history():
    gas_stats = get_price_stats()
    prepared_stats = {block['block']: block['fee'] for block in gas_stats}
    return gas_stats, prepared_stats


def get_price_stats():
    last_block = 'latest'
    gas_prices = []

    # 2 weeks will be fetched
    # 45 * 1024 block / 13 seconds = 1 week
    for i in range(90):
        stats = web3.eth.fee_history(1024, last_block)
        last_block = stats['oldestBlock'] - 2

        gas_pirce = zip_gas(stats['baseFeePerGas'], stats['oldestBlock'])
        gas_pirce.reverse()

        gas_prices.extend(gas_pirce)

    return gas_prices


def zip_gas(gas_fees, last_block):
    current_block = last_block

    results = []

    for fee in gas_fees:
        results.append({
            'fee': fee,
            'block': current_block
        })

        current_block += 1

    return results


def get_percent(prepared_data, curr_block_num, blocks_count, percent):
    gas_fee = []

    for block in range(curr_block_num - blocks_count, curr_block_num):
        if block < 0:
            continue

        if block in prepared_data:
            gas_fee.append(prepared_data[block])

    gas_fee.sort()

    if not gas_fee:
        return 0

    return gas_fee[int(len(gas_fee) * percent)]


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.P("Percentile"),
    dcc.Slider(
        id='percentile',
        min=0,
        max=1,
        value=0.2,
        step=0.01
    ),
    html.P("Block in pass"),
    dcc.Input(
        id='blocks_count',
        type='number',
        value=4500
    )
])


@app.callback(
    Output("graph", "figure"),
    [Input("percentile", "value"), Input("blocks_count", "value")]
)
def customize_width(percentile, blocks_count):
    gas_stats, prepared_stats = get_blocks_history()

    x = []
    y1 = []
    y2 = []

    for index, stat in enumerate(gas_stats):
        # Show every 300 block ~ every 1 hour
        # Do not show chart if we dont have enough prev data
        if index % 300 == 0:
            # Not enough prev data
            percent = get_percent(prepared_stats, stat['block'], blocks_count, percentile)
            if percent:
                x.append(stat['block'])
                y1.append(stat['fee']/10**9)
                y2.append(percent/10**9)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y1,
            name='Current gas price',
            line=dict(color='firebrick', width=4)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y2,
            name='Recommended price',
            line=dict(color='blue', width=2)
        )
    )

    return fig


app.run_server(debug=True)
