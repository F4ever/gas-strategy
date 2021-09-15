## Motivation
To keep our stacking protocol working we should deposit keys with ether to contract.
Now for each key that we deposit, we spend around 60,000 gas. For all the time we spent 175.6 ETH.  
[Deposit history](https://dune.xyz/embeds/107033/216851/03d8d3ce-3bf3-45b9-bdb1-bddaf797786d)

We want to spend less money for each key and do deposit at least once every day, so we can wait a bit for the gas price to go down.

## Possible solution
One of the solutions to the problem is to count the 20 percentile for the previous couple of days.  
I calculate two values:
- 20 percentile for 1 day
- 20 percentile for 4 days
And the minimum of them becomes the recommended price.

Gas cost more actively affects 1 day percentile, so if the gas drops sharply, then during the day we will use the reduced recommended price.
If gas cost will increase a lot for one day - 4 day percentile will not let the recommended price rise sharply, so we will wait for couple days for better prices.

There is a sandbox to play with percentile and gas fee: [Recommended gas fee](https://github.com/F4ever/gas-strategy).

## Depositor bot
[Depositor source code](https://github.com/lidofinance/depositor-bot)

## Plans
Provide deposit operations threw lido easy-tracks.  
Receive compensation for keys deposit.
