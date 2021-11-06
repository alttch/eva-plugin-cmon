# eva-plugin-cmon

Controller status monitor plugin for [EVA ICS](https://www.eva-ics.com/)

Monitors connected controllers status in SFA and pushes measurements into an
external InfluxDB.

Measurements look like:

```
remote_uc:uc/NAME connected=1
remote_lm:lm/NAME connected=1
```

## Plugin installation and configuration

Download **cmon.py** and put it to *EVA_DIR/runtime/plugins*

To configure the plugin, exec:

```shell
eva sfa edit plugin-config
```

Configuration options: look header inside **cmon.py**
