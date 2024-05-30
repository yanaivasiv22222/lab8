from dataloader.coinbaseloader import CoinbaseLoader, Granularity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import os
import yaml
import logging.config

def setup_logging(path='logger.yml', level=logging.INFO, env_key='LOG_CONFIG'):
    path = os.getenv(env_key, path)
    if (os.path.exists(path)):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

def main():
    loader = CoinbaseLoader()
    df_1 = loader.get_historical_data("btc-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)
    df_2 = loader.get_historical_data("gmt-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)

    # do some analysis
    df_1['SMA20'] = df_1['close'].rolling(window=20).mean()
    df_1['SMA50'] = df_1['close'].rolling(window=50).mean()

    df_2['SMA20'] = df_2['close'].rolling(window=20).mean()
    df_2['SMA50'] = df_2['close'].rolling(window=50).mean()

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.set_figwidth(14)
    fig.set_figheight(7)

    ax1.plot(df_1.close, label='Ціна закриття')
    ax1.plot(df_1.SMA20, label='SMA 20 днів')
    ax1.plot(df_1.SMA50, label='SMA 50 днів')
    #ax1.title('Аналіз ціни BTC')
    #ax1.xlabel('Дата')
    #ax1.ylabel('Ціна закриття')
    #ax1.legend()
    ax1.grid()

    ax2.plot(df_2.close, label='Ціна закриття')
    ax2.plot(df_2.SMA20, label='SMA 20 днів')
    ax2.plot(df_2.SMA50, label='SMA 50 днів')
    #ax2.title('Аналіз ціни GMT')
    #ax2.xlabel('Дата')
    #ax2.ylabel('Ціна закриття')
    #ax2.legend()
    ax2.grid()

    plt.show()

    df = pd.merge(df_1, df_2, left_index=True, right_index=True)
    cm = df[['close_x', 'close_y']].corr()
    sns.heatmap(cm, annot=True)
    plt.show()

    df_1['LR'] = np.log(df_1.close/df_1.close.shift(1))
    plt.plot(df_1.LR)
    plt.grid()
    plt.show()

    print(f"volatility: {df_1.LR.std():0.4f}")

    df_2['LR'] = np.log(df_2.close/df_2.close.shift(1))
    plt.plot(df_2.LR)
    plt.grid()
    plt.show()

    print(f"volatility: {df_2.LR.std():0.4f}")

if __name__ == "__main__":
    setup_logging()
    main()