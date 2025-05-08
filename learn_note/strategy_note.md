# 策略定制笔记

> 这篇笔记用于记录如何定制一个策略

## FT 的策略要素

FT 并不能加载未完成的蜡烛图.(最新的蜡烛图)

自定义指标: user_data/strategies/sample_strategy.py 中包括了很多自定义指标. 也可以按需要加入新的.

最小蜡烛数量

某些指标的启动阶段不稳定, 应将此设置为策略计算稳定指标所需的最大蜡烛图数量
startup_candle_count

### 最低投资回报率
```python
minimal_roi = {
    "40": 0.0,
    "30": 0.01,
    "20": 0.02,
    "0": 0.04
}

```

 dict 键（冒号左侧）是自交易开始以来经过的分钟数，值（冒号右侧）是百分比。
上述配置意味着：
- 每当达到4%的利润时退出
- 达到2%利润时退出（20分钟后生效）
- 达到1%利润时退出（30分钟后生效）
- 交易无亏损时退出（40分钟后生效）
计算包括费用。

如何设置为蜡烛条数: 
```python
class AwesomeStrategy(IStrategy):

    timeframe = "1d"
    timeframe_mins = timeframe_to_minutes(timeframe)
    minimal_roi = {
        "0": 0.05,                      # 5% for the first 3 candles
        str(timeframe_mins * 3): 0.02,  # 2% after 3 candles
        str(timeframe_mins * 6): 0.01,  # 1% After 6 candles
    }
```

### 做空 short

1. 必须在配置中设置 can_short = True
2. 必须在期货市场中(现货无效)
3. 在策略方法函数中设置 enter_short = 1

### 元数据字典 metadata

类似于跨越函数的上下文(context)
例如 metadata['pair'] (返回当前交易的货币对)
详见: 
https://www.freqtrade.io/en/stable/strategy-advanced/#storing-information-persistent

### 加载策略文件

默认情况下，freqtrade 将尝试从(默认).py内的所有文件加载策略。userdiruser_data/strategies

可以在运行交易时(dry-run or live)中指定交易策略
```
freqtrade trade --strategy AwesomeStrategy
```

可以通过这个命令查看全部可用的策略
`freqtrade list-strategies`

### Informative Pairs 
同时分析非交易对的数据，作为辅助决策的参考指标

informative_pairs

### 不要使用未来函数导致前瞻偏差




## 社区策略库
https://github.com/freqtrade/freqtrade-strategies
已经下载到本地: community-strategies