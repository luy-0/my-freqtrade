# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,  # @informative decorator
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
from technical import qtpylib


class Simple_SMA_Cross_strategy(IStrategy):
    """
    This is a strategy template to get you started.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/
 
    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy
    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_entry_trend, populate_exit_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*

    你可以:
    - 重命名类名 (不要忘记更新 class_name)
    - 添加任何你想要构建策略的方法
    - 添加任何你需要的库来构建策略
    你必须保持:
    - 在 "Do not remove these libs" 部分中的库
    - 方法: populate_indicators, populate_entry_trend, populate_exit_trend
    你应该保持:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    # 中文: 策略接口版本 - 允许新的策略接口版本.
    # 检查文档或示例策略以获取最新版本.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    # 最佳时间框架用于策略.
    timeframe = "5m"

    # Can this strategy go short?
    # 这个策略可以做空
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    # 为策略设计的最低ROI.
    # 如果配置文件中包含 "minimal_roi", 此属性将被覆盖.
    minimal_roi = {
        "0": 1
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    # 为策略设计的最佳止损.
    # 如果配置文件中包含 "stoploss", 此属性将被覆盖.
    stoploss = -1

    # Trailing stoploss
    # 跟踪止损
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    # 仅在新的蜡烛上运行 "populate_indicators()".
    process_only_new_candles = True

    # These values can be overridden in the config.
    # 这些值可以在配置文件中重写.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    # 策略在产生有效信号之前需要的最小蜡烛数量
    startup_candle_count: int = 30

    # Strategy parameters
    # 策略参数
    buy_rsi = IntParameter(10, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        # 定义额外的, 用于缓存的配对/时间间隔组合.
        # 这些配对/时间间隔组合是非交易性的, 除非它们也在白名单中.

        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return [("BTC/USDT", "5m")]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        添加技术指标到数据框中：
        - 快速SMA(5周期)
        - 慢速SMA(50周期)
        """
        dataframe['fma'] = ta.SMA(dataframe, timeperiod=5)  # 快速移动平均线
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=50)  # 慢速移动平均线

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
         """
        当FMA(5)上穿SMA(50)时买入
        """
         dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['fma'], dataframe['sma']))  # FMA上穿SMA
            ),
            'enter_long'] = 1  # 设置买入信号

         return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
         """
        当FMA(5)下穿SMA(50)时卖出
        """
         dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['fma'], dataframe['sma']))  # FMA下穿SMA
            ),
            'exit_long'] = 1  # 设置卖出信号
         return dataframe