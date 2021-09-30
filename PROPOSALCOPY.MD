## Proposal to use a bot to deposit keys and ether to contract.

User's ether submitted to Lido smart contract is deposited to the Beacon chain staking via depositBufferedEther call on Lido smart contract. 
This operation requires significant amount of gas, making manual operations not as cost-efficient as possible.  

We propose to run and fund bot that will automate the deposits, implementing smart gas strategy suitable for task's constraints.
Along with this, we propose refunding dev team for gas spent on deposits so far (86.16 ETH)

## Problem

Protocol's APR is earned only on deposited ether - having big buffer hurts APR. 
It requires smart contract interaction to deposit ether. 
Deposit ether is gas-consuming, making it desirable to choose some form of optimal moment / gas price to:
1. not overspend;
2. don't have too much ether in the buffer for too long, hurting the protocol's apr;

## Proposed solution

Write bot that will track gas fee history and deposit buffered ether if conditions are met (gas fee, buffered ether, unused keys).

#### Gas strategy:

One of strategy we propose is to count the 20 percentiles for the previous couples of days and use one of them as recommended fee.

Calculate two values:
- 20 percentile for 1 day
- 20 percentile for 4 days

And the minimum of them becomes the recommended fee.

As soon as current fee is lower than recommended fee we allow submitting deposit transaction.

## Strategy details

Chart with 1-day & 4-days 20th percentiles:  
<img src="https://github.com/F4ever/gas-strategy/blob/master/plot_example.png" alt="Gas fee chart">
  
Script used to build a plot:
[Gas strategy proposal](https://github.com/F4ever/gas-strategy)

## Implementation

The proposed bot source code: [Depositor source code](https://github.com/lidofinance/depositor-bot)

## Compensation

Total ether spent by dev team on gas: 86.16 ETH.
Calculations: [https://dune.xyz/queries/162545](https://dune.xyz/queries/162545)
