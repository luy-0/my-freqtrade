# Freqtrade 笔记

## 快速开始与启动

使用 docker 进行启动.

测试文件夹位于 ft_userdata, 

## 常见操作

### 初始化测试环境

使用 docker-compose.yml 作为 docker 的启动配置.

``` shell
docker compose pull     # 根据 yml 文件拉取镜像
docker compose run --rm freqtrade create-userdir --userdir user_data    # 创建测试文件夹
docker compose run --rm freqtrade new-config --config user_data/config.json # 交互地创建配置

```

1. 这种方法运行的并不是基于本地代码,而是拉取的远程镜像.
2. 测试文件夹位于 ft_userdata
3. 配置位于 ft_userdata/user_data/config.json


### 运行机器人

```
docker compose up -d
```


### 下载数据

```
docker exec 8f84e7999aa3 freqtrade download-data --exchange binance --pairs BTC/USDT --data-format-ohlcv json
```     
1. docker 命令, 其中 8f84e7999aa3 为 container ID.
2. `freqtrade download-data --exchange binance --pairs BTC/USDT --data-format-ohlcv json` 这一段才是具体的指令. `download-data` 为子命令, 后面的为参数. `--data-format-ohlcv` 表示下载为 json 格式(默认 feather 格式)

### 简单策略编写

测试环节下, 策略位于 ft_userdata/user_data/strategies 中
