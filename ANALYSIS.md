# muse-skills 分析

分析对象是整理后的这棵目录，不是上游那份带二进制的快照。数字来自 `python3 scripts/build_catalog.py` 对当前文件的清点。没有执行技能，没有连接外部账户。

## 结论

这是一套个人 Agent 的技能协议，不是应用源码。

一个技能通常由三层组成。`SKILL.md` 告诉模型何时动手、走哪条命令、失败时说什么。`manifest.yaml` 把同一能力拆成方法，并给每个方法默认的 `allow` 或 `ask`。`eval/` 记录希望覆盖的场景，不证明场景已经跑通。

68 个技能里，29 个标记为 `includeInPrompt: true`，会占常驻上下文。另外 39 个靠描述按需加载。37 个技能旁边有自己的 `manifest.yaml`。12 个技能带 `eval/`。`config/skills.yaml` 只声明了 31 个连接器为 `available`，而且这份声明只管本地配置，不管账户是否已经连上。

## 技能怎么分组

| 组 | 数量 | 在解决什么 |
| --- | --- | --- |
| 工作流与记忆 | 6 | 并行研究、目标、遗忘、技能编写、自我状态、数据库诊断 |
| 文档与产物 | 6 | Word、Markdown、PDF、幻灯片、表格，以及交付前验收 |
| 旅行与预订 | 7 | 行程研究和实时可订查询分开走 |
| 办公与知识库 | 16 | Gmail、Google、Outlook、Notion、Granola、Calendly |
| 社交与消息 | 6 | 读取内容和代发分开写 |
| 购物与金融 | 3 | 比价路由、Printify、Plaid 只读账户数据 |
| 健康与健身 | 6 | HealthKit、Health Connect、检验、Peloton、Withings |
| 图像、音频与视频 | 8 | 搜图、图库、语音、播客、Magic Moment |
| 设备与网络 | 6 | 本机缓存、穿戴设备、Hue、Tesla、Tailscale |
| Muse 产品操作 | 4 | 抢先体验、反馈、Idea、订阅状态 |

另有 4 个别名，用符号链接指向本体：`facebook` → `facebook-cli`，`meta-threads` → `threads`，`podcast` → `generate_podcast`，`voice-calls` → `voice-selector`。`voice-calls` 这个名字容易让人以为它能代打电话。它指向的是语音选择。

`skills/spaces/` 没有顶层 `SKILL.md`。里面是 Web artifact 的说明和模板。上游分析已经指出，构建用的 SDK 和 `space-sdk.tgz` 不在快照里。这个仓库同样没有它们。

## 权限不是一句「写入要问」

manifest 把动作分成组，组有 `default`，方法还可以覆盖。当前 37 份技能 manifest 里，`default: allow` 出现 83 次，`default: ask` 出现 26 次。这是标记次数，不是方法总数。

Gmail 是最清楚的例子。读取组默认 `allow`。写入组默认 `ask`。同组里的草稿、标已读、丢进垃圾箱覆盖成 `allow`。发送继承 `ask`，并带 `approval_phrase`。所以不能把「写入默认 ask」说成「每次写操作都会再问一次」。

`config/skills.yaml` 的键用下划线，目录用连字符。`messenger_read` 对不上目录名 `messenger`，索引里单独记了这条。其余 30 个键能直接对应到目录。没有出现在这份配置里的 37 个技能，主要是工作流、产物、旅行规划和产品操作。它们不靠这个开关文件启用。

## 渠道闸门比这份技能树更大

`runtime/skill-scopes.conf` 按渠道列出可以露出的技能目录。文件头写明它由另一份 manifest 生成，匹配不到渠道时什么都不放出。

这份列表里有 30 个名字不在 `skills/` 中，包括 Slack、Zoom、Shopify、Canva、Dropbox、Linear、QuickBooks。说明原系统的技能集合大于这个快照。看不见的技能不能从名字推断实现，也不能当成这里漏拷了文件。

`runtime/` 里的 shell 脚本描述 Linux cell 如何用 `systemd-nspawn` 启动、如何注入环境、如何按渠道挂出技能。脚本能说明调用方式。它们不能在这台机器上把系统跑起来，因为 rootfs、daemon 二进制和宿主 unit 都不在。

## 值得拿走的设计

1. 触发条件写在 frontmatter 的 `description` 里，正文只写做法。常驻和按需用 `includeInPrompt` 分开。
2. 人读的流程和机器读的权限分开。权限细到方法，而不是一个连接器一个总开关。
3. 研究、可订查询、付款分成不同技能。`travel-planning` 不直接下单，`booking` 和各供应商技能才碰交易。
4. 产物技能把「生成出来了」和「可以交付」拆开。`artifacts/testing` 负责后一步。
5. 遗忘被写成流程。`forget` 要处理副本和可能写回的后台任务，而不是删一条笔记就结束。
6. eval 场景会写下做不到的部分。FlightAware 的材料记录过路由和身份失败，并说明当时没有完成真实读取。那是历史诊断，不是当前接口仍故障的证据，也不是已经通过的证据。

## 不要从这份仓库推出的结论

- 技能列在这里，不表示对应账户已连接，也不表示 OAuth scope 已经授予。
- `status: available` 只是配置声明。
- 没有在这里跑过 eval，不能给任何技能打通过或不通过。
- 上游材料里的公司、模型和地区说法，这里没有核过。
- 删掉二进制是阅读上的取舍，不是对那些程序做了安全审计。
