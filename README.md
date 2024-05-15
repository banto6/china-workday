# China Workday

适用于中国节假日的工作日插件。

## 安装

方法1：下载并复制`custom_components/china-workday`文件夹到HomeAssistant根目录下的`custom_components`文件夹即可完成安装

方法2：已经安装了HACS，可以点击按钮快速安装 [![通过HACS添加集成](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=banto6&repository=china-workday&category=integration)

## 配置

配置 > 设备与服务 >  集成 >  添加集成 > 搜索`china workday`

或者点击: [![添加集成](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=china-workday)

## 调试
在`configuration.yaml`中加入以下配置来打开调试日志。

```yaml
logger:
  default: warn
  logs:
    custom_components.china-workday: debug
```


## 数据来源
- https://github.com/NateScarlet/holiday-cn