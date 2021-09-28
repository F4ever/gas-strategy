## Proposal to use a bot to deposit keys and ether to contract.

As you know, to keep our stacking protocol working we should deposit keys and ether to deposit contract.
For now, we don't have any automatic solution.

We propose:
1. Run and fund bot that will deposit buffered ether to contract.
2. Make refund to the development team that deposited buffered ether to contract before.

## Problem

Ether is placed in buffer, and it must be deposited by calling smart contract. Until now, it was done manually.
Manual action requires attention, and we can save money if we deposit while the cost of gas is low.

## Strategy

The main idea is to control gas fee and create transaction when the gas fee is quite low.

One of strategy is to count the 20 percentile for the previous couple of days.  
We calculate two values:
- 20 percentile for 1 day
- 20 percentile for 4 days
And the minimum of them becomes the recommended fee.

If current fee is lower than recommended fee we submit transactions.

## Strategy details

I wrote a small script that looks at historical data and plots charts with recommended price, percentile for 1 day and percentile for 4 days. And got this:  

<img src="https://github.com/F4ever/gas-strategy/blob/master/plot_example.png" alt="Gas fee chart">
  
You can play with sandbox and change percentile and/or period used to calculate percentile:  
[Gas strategy proposal](https://github.com/F4ever/gas-strategy)

## Implementation

Here is the source for the depositor bot: [Depositor source code](https://github.com/lidofinance/depositor-bot)

## Compensation

Ether calculations that the development team spent to deposit ether: [https://dune.xyz/queries/162545](https://dune.xyz/queries/162545)
