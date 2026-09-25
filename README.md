# muse-skills

[win4r/MuseAI-Skills](https://github.com/win4r/MuseAI-Skills) 的技能阅读副本。上游是 [muse.ai](https://muse.ai) / Hatch 个人 Agent 环境的非官方快照。这个仓库只留下技能、产品说明、技能开关和运行时脚本。

它不是 Muse 官方仓库，也不是安装包。技能正文保持原样，里面的命令和 `/opt/hatch/...` 路径属于那个运行时。把 Markdown 拷走不会带上账户、OAuth 或 CLI。

分析见 [ANALYSIS.md](ANALYSIS.md)。完整索引见 [catalog/INDEX.md](catalog/INDEX.md)。

## 和上游快照的差别

上游把三类材料叠在同一棵目录里。

| 原路径 | 这里 | 原因 |
| --- | --- | --- |
| `opt/hatch/skills` | `skills/` | 68 个技能和 4 个别名，这是要读的部分 |
| `home/hatch/docs` | `docs/` | 给 Agent 看的产品边界 |
| `home/hatch/config` | `config/` | 推理档位和 31 个连接器开关 |
| `opt/hatch/runtime-cell` | `runtime/` | cell 启动和渠道可见性，只作结构参考 |
| `opt/hatch/bin`、`opt/hatch-image` | 不收录 | Linux 二进制、Bun、Codex 和一份 npm。读技能用不到，原仓库用 Git LFS 存放 |

## 目录

```
skills/     技能正文、manifest、eval、参考资料
docs/       产品说明
config/     skills.yaml、home.yaml
runtime/    原 cell 脚本
catalog/    生成的索引
scripts/    重建索引
```

## 怎么读一个技能

1. 看 `SKILL.md` 开头的 `description`。那是触发条件，不是功能广告。
2. 有 `manifest.yaml` 时，读 `actions` 里的 `default`。组的默认值和单个方法的 `default` 可以不同。Gmail 的写入组默认是 `ask`，草稿却是 `allow`，发送仍是 `ask`。
3. 有 `eval/` 时，把它当成场景说明。它不是这份仓库跑过的测试结果。
4. `metadata.includeInPrompt: true` 的技能会进常驻提示。其余技能靠描述按需加载。

重建索引：

```bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
```

## 来源

上游没有许可证。技能和文档的文字来自该快照，这里只改了目录布局，并补了索引和分析。不要把「在这个仓库里看得到」理解成「可以随便再授权，或已经能独立运行」。
