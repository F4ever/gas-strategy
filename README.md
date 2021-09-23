# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/> Gas recommended price

## Start
```bash
pip install -r req.txt
export INFURA_PROJECT_ID=...
python main.py
```

Go to http://127.0.0.1:8050/

Wait for 2 minutes to download data and prepare chart

## Params
Days to fetch - How many blocks fetch from mainnet to build chart  
Percentile (min 0, max 100)  
Blocks in past - How many previous blocks to use for the percentile  


## Output 
![Gas chart](./plot_example.png)  

If recommended price is higher than Current gas fee, it's time to deposit keys.
