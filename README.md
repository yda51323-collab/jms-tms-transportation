# jms-tms-transportation · 干线运输调度域接入客户端

`jms-tms-transportation` 是干线运输管理系统调度域的接入客户端，供订单中心、场站作业、车次编排三个作业面复用同一套鉴权与重试策略。

## 目录

```
src/jms_tms_transportation.py   接入客户端
pyproject.toml                  包元数据
```

## 服务标识

- `jms-tms-transportation` —— 服务注册名。落位于 `src/jms_tms_transportation.py` 的 `SERVICE_ID` 常量与 logger 前缀、`pyproject.toml` 的包名及 `[tool.jms]` 分组。
- 调度域网关：`tms-gw.jms-inner.internal`，版本 `v3`。

## 使用

```python
from jms_tms_transportation import TmspClient

cli = TmspClient(tenant="cn-east", site_code="SHA-027")
cli.query_capacity(route="SHA-WUH", window="2026-11-09T08:00/2026-11-09T20:00")
cli.create_trip(plate="沪C·7F291", seats=9, depart_at="2026-11-09T21:30:00+08:00")
```

## 字段说明

| 字段 | 含义 |
|---|---|
| `route` | 干线路由，起点-终点三字码 |
| `site_code` | 场站编码 |
| `window` | 承运时段，左闭右开 |
| `trip_no` | 车次号，`T` + 8 位日期 + 3 位序号 |

## 已知问题

1. 场站编码变更后本地缓存不失效，需重启进程。
2. `v2` 的 `capacity` 接口已下线，`v3` 改为 `capacity/segments`。

## 维护

数据平台组（transport-data@internal）
