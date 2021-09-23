## Proposal to use a bot to deposit keys and ether to contract.

Hello everyone!

As you know, to keep our stacking protocol working we should deposit keys and ether to deposit contract.
For now, we don't have any automatic solution, so sometimes we do not deposit keys for few days or more. 
We also spend quite a lot of gas at not the best prices. (so far we have spent about 86 ethers)

## Solution

The main idea is to control gas fee and make a deposit when the gas fee is quite low. So we can wait for a good gas fee for several days.

So we need a strategy to calculate recommended fee:

## Strategy

One of them is to count the 20 percentile for the previous couple of days.  
We calculate two values:
- 20 percentile for 1 day
- 20 percentile for 4 days
And the minimum of them becomes the recommended fee.

If current fee is lower than recommended fee we submit transactions.

## Details

Will this work?

I wrote a small script that looks at historical data and plots charts with recommended price, percentile for 1 day and percentile for 4 days. And got this:  

<img src="https://github.com/F4ever/gas-strategy/blob/master/plot_example.png" alt="Gas fee chart">
  
You can play with sandbox and change percentile and/or period used to calculate percentile:  
[Gas strategy proposal](https://github.com/F4ever/gas-strategy)

Why I used two period for percentile?

My thoughts were that gas fee more actively affects 1 day percentile and if gas fee is high for a day, recommended fee will rise slowly.
But if the cost of gas will be quite low, then thanks to the 1-day percentile recommended price will go down quite fast.

## Implementation

Here is the source of the depositor bot: [Depositor source code](https://github.com/lidofinance/depositor-bot)

## Compensation

After launching the bot, we must compensate ether for the gas spent to dev team.  
For now, it equals to 86.16048979433397 ether. Here is [query](https://dune.xyz/queries/162545) in Dune to calculate fee.

Here is dev team wallet's address: `0x48F300bD3C52c7dA6aAbDE4B683dEB27d38B9ABb`.
