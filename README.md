# BITBANK

Exchange plugin for bt_api framework.

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitbank.svg)](https://pypi.org/project/bt_api_bitbank/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitbank.svg)](https://pypi.org/project/bt_api_bitbank/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitbank/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitbank/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitbank/badge/?version=latest)](https://bt-api-bitbank.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

This package provides **Bitbank exchange plugin for bt_api** for the [bt_api](https://github.com/cloudQuant/bt_api_py) framework. It offers a unified interface for interacting with **BITBANK** exchange.

### Features

- Exchange integration with bt_api
- REST API support
- Market data access
- Basic trading operations

### Installation

```bash
pip install bt_api_bitbank
```

Or install from source:

```bash
git clone https://github.com/cloudQuant/bt_api_bitbank
cd bt_api_bitbank
pip install -e .
```

### Quick Start

```python
from bt_api_bitbank import BitbankApi

# Initialize
feed = BitbankApi(api_key="your_key", secret="your_secret")

# Get ticker data
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### Supported Operations

| Operation | Status |
|-----------|--------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitbank.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitbank.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitbank |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitbank/issues |

### Requirements

- Python 3.9+
- bt_api_base >= 0.15

### Architecture

```
bt_api_bitbank/
├── src/bt_api_bitbank/     # Source code
│   ├── containers/     # Data containers
│   ├── feeds/          # API feeds
│   ├── gateway/       # Gateway adapter
│   └── plugin.py      # Plugin registration
├── tests/             # Unit tests
└── docs/             # Documentation
```

### License

MIT License - see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitbank/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitbank exchange plugin for bt_api**。它提供了与 **BITBANK** 交易所交互的统一接口。

### 功能特点

- bt_api交易所集成
- REST API支持
- 市场数据访问
- 基本交易操作

### 安装

```bash
pip install bt_api_bitbank
```

或从源码安装：

```bash
git clone https://github.com/cloudQuant/bt_api_bitbank
cd bt_api_bitbank
pip install -e .
```

### 快速开始

```python
from bt_api_bitbank import BitbankApi

# 初始化
feed = BitbankApi(api_key="your_key", secret="your_secret")

# 获取行情数据
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### 支持的操作

| 操作 | 状态 |
|------|------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitbank.readthedocs.io/ |
| 中文文档 | https://bt-api-bitbank.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitbank |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitbank/issues |

### 系统要求

- Python 3.9+
- bt_api_base >= 0.15

### 架构

```
bt_api_bitbank/
├── src/bt_api_bitbank/     # 源代码
│   ├── containers/     # 数据容器
│   ├── feeds/          # API 源
│   ├── gateway/        # 网关适配器
│   └── plugin.py       # 插件注册
├── tests/             # 单元测试
└── docs/             # 文档
```

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitbank/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com
