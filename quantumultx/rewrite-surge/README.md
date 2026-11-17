# Surge 重写模块

在 Surge 的「模块」中安装对应的 .sgmodule 文件。AdBlock-All 是合集，选择合集或分项即可，避免重复安装。

需要 Surge iOS 5.9.1+ / Mac 5.5.1+，打开 Rewrite，配置并信任 MITM 证书。模块使用 %APPEND% 追加仓库 MITM 清单和原文件主机名，不替换现有列表；泛路径规则仅对 MITM 已覆盖的 HTTPS 主机生效。

转换方式：reject → URL Rewrite；reject-dict / reject-array / reject-200 / reject-img → Map Local，分别返回 {} / [] / 空文本 / 透明 GIF；脚本规则 → Script，保留原脚本地址和请求/响应阶段，开启 requires-body。

已逐条转换实际规则：Splash 112、Feed 108、Script 35、All 255。原文件 TOTAL 将 hostname 也计入 Script / All，因此分别标为 36 / 256。

原有外部依赖问题：什么值得买 smzdm_remove_ads.js 地址在转换时返回 404，相关规则需要可用的兼容脚本才能生效。其他外部脚本仍依赖上游维护；本次未修改脚本代码，未在 Surge 客户端进行流量实测。

参考：https://manual.nssurge.com/http/map-local.html
https://manual.nssurge.com/http/url-rewrite.html
https://manual.nssurge.com/scripting/overview.html
