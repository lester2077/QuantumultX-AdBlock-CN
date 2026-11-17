# 合并规则

- AdBlock-Merged-Filter.list：合并 Splash-Killer.list、BlockHttpDNS.list、AdBlock-Lite.list，按完整规则去重，保留原顺序和策略。
- AdBlock-Merged-Rewrite.conf：合并 AdBlock-Splash.conf、AdBlock-Script-a.conf，合并 hostname；完全相同 URL 正则的拒绝规则让位于脚本，脚本声明放在前面。

list 用于分流规则，conf 用于 MITM 模块。不要同时启用其原始来源，避免重复规则。

注意：未将域名 REJECT 自动改为放行。域名拦截或较宽的重写拦截仍可能导致响应脚本拿不到服务器响应；按具体 App 的请求日志排查。脚本仍使用远程地址，需下载成功并启用模块与 MITM，证书需正确配置。未进行客户端流量实测。
