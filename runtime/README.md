# runtime

这些文件来自上游快照的 `opt/hatch/runtime-cell`。它们描述 Linux cell 如何启动，以及如何按渠道决定哪些技能可见。

`skill-scopes.conf` 是生成文件。里面不少目录名并不在本仓库的 `skills/` 里。不要把这份列表当成当前技能树的目录。

这里没有 rootfs，也没有 daemon 二进制。不要在本机执行 `launch-daemon.sh`。
