## Proposal to use a bot to deposit keys and ether to contract.

User's ether submitted to Lido smart contract is deposited to the Beacon chain staking via depositBufferedEther call on Lido smart contract. 
This operation requires significant amount of gas, making manual operations not as cost-efficient as possible.  

We propose to run and fund bot that will automate the deposits, implementing smart gas strategy suitable for task's constraints.
Along with this, we propose refunding dev team for gas spent on deposits so far (87,814,430,128,333,960,000 WEI; note that the number may have changed)

## Problem

Protocol's APR is earned only on deposited ether - having big buffer hurts APR.
Ether is deposited through the smart contract call (depostiBufferedEther on Lido smart contract 0xdcd90c7f6324cfa40d7169ef80b12031770b4325)
The ether deposit is a gas-intensive operation, so it should be done balancing gas expenses and the time ether sits in protocol buffer.

## Proposed solution

Implement and deploy a bot which would deposit buffered ether using the specified gas strategy.

#### Gas strategy:

The proposed strategy is to send deposit transactions once the current gas price is below both 1-day 20-th percentile & 4-days 20-th percentile.

## Strategy justification

Chart with 1-day & 4-days 20th percentiles (1 week long):  
<img src="https://github.com/F4ever/gas-strategy/blob/master/plot_example.png" alt="Gas fee chart">
  
Script used to build a plot:
[Gas strategy proposal](https://github.com/F4ever/gas-strategy)

## Implementation

The proposed bot source code: [Depositor source code](https://github.com/lidofinance/depositor-bot)

## Compensation

Dev team has been running the operation manually and has spent 87.81 ether.
Calculations: [https://dune.xyz/queries/162545](https://dune.xyz/queries/162545)
