# J-Link Commander (JLink.exe / JLinkExe)
常用参数|说明
-|-
`-device`|指定目标设备名称
`-if`|指定接口类型：SWD, JTAG, FINE, cJTAG
`-speed`|设置通信速度（kHz），如：4000, auto, adaptive
`-autoconnect`|自动连接模式：0（禁用）、1（启用）
`-jtagconf`|JTAG配置参数
`-SelectEmuBySN`|通过序列号选择特定的J-Link设备
`-USB`|指定USB端口
`-IP`|通过IP连接J-Link
`-CommandFile`|执行命令脚本文件
`-ExitOnError <1\|0>`|错误时退出
`-NoGui <1\|0>`|禁用GUI模式

```shell{.line-numbers}
"无弹窗的打开jlink"
jlink -USB ?
jlink -nogui 1
```

# J-Link GDB Server (JLinkGDBServer / JLinkGDBServerCL)
常用参数|说明
-|-
`-device`|目标设备
`-if`|接口：SWD, JTAG
`-speed`|连接速度
`-port`|GDB服务器端口（默认2331）
`-swoport`|SWO端口（默认2332）
`-telnetport`|Telnet端口（默认2333）
`-select`|选择J-Link：USB=, IP=
`-endian <little\|big>`|字节序
`-noir`|不复位目标
`-noreset`|连接时不复位
`-nohalt`|连接后不停止CPU
`-silent`|静默模式
`-singlerun`|单次运行模式
`-strict`|严格模式
`-timeout`|超时设置

# J-Link SWO Viewer
参数|说明
-|-
`-device`|目标设备
`-cpufreq`|CPU频率（Hz）
`-swofreq`|SWO频率（Hz）






