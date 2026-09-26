# AGENTS.md

win4r/MuseAI-Skills 快照的阅读副本，只收技能、产品说明、配置和运行时脚本（映射见 README）。

- `skills/`、`docs/`、`config/`、`runtime/` 保持上游原文，不改写、不翻译；`/opt/hatch/...` 路径属于原运行时，不要“修正”。
- `catalog/` 是生成物：改了 `skills/` 后跑 `python3 scripts/build_catalog.py`，提交前 `python3 scripts/build_catalog.py --check` 必须通过。
- `ANALYSIS.md` 里的数字来自 catalog 脚本清点；技能数量变化时一并更新。
