# 06 · M6 Features 五卡（SOURCE）

## 布局
- `.features`：padding 40px 0 60px，bg `--color-bg`。
- `h2.features__title`：margin `0 0 35px`，居中，`--font-display` 30px/500 ls .4px。文本 zh `为什么选择 MiMo Code`。
- `.features__list`：column，gap 43px，宽 1100px（max-width calc(100% - 80px)）居中。
- `.card`：relative，100%×360px，radius 4，overflow hidden。内部两个绝对定位层：`.card__painting`（overflow hidden，img object-fit cover）与 `.card__text`（331px 宽，column gap 10）。

## 五卡几何与配色（SOURCE，CSS 行值原样）
| 卡 | 底色 | painting | text |
|----|------|----------|------|
| 1 开箱即用顶尖模型 | `#efebe3` | left 0 top 0，573×360 | left 648 top 136 |
| 2 模型 Agent 协同 | `#f6f1ea` | left 527 top 0，573×360 | left 129 top 130 |
| 3 无限上下文 | `#efe8e3` | left 0 top 0，573×360 | left 645 top 114 |
| 4 自进化系统 | `#fbf2e9` | left 527 top 0，573×360 | left 122 top 107 |
| 5 Compose模式 | `#f5ede7` | left 0 top 0，**660×360** | left 670 top 112 |

规律：奇数卡画在左文在右，偶数卡文在左画在右；卡 5 画更宽（660）。

## 文本排版
- `h3`：`--font-mincho` 22px/500，line-height 1.447，色 ink。（卡 5 h3 字体同 mincho——有条冗余规则 `.card--5 .card__text h3{font-family:var(--font-mincho)}`，保留。）
- `p`：`--font-misans` 16px/**300**，line-height 1.447，色 `--color-ink-soft`。
- h3 打字机结构见 05b。

## 文案（zh，data-i18n key 见 08）
1. 开箱即用顶尖模型 / 无需登录，开箱即用，免费体验比肩 Claude Sonnet 4.6 级别多模态模型。
2. 模型 Agent 协同 / MiMo 模型与 Agent 协同优化，复杂编码任务一次搞定。
3. 无限上下文 / 知识自动沉淀，配合记忆整理。上百轮对话，也不丢失关键信息，智商始终在线。
4. 自进化系统 / 基于使用反馈持续学习与优化，模型能力、工具链、工作流随你的项目共同成长。越用越懂你，越用越顺手，打造专属智能开发伙伴。
5. Compose模式 / 一个人的专业开发团队，从想法到产品的工业级交付

## 还原要点
- 文本块绝对坐标是**从卡片左上角量的精确 px**，不要转成百分比。
- 图片 alt=""（纯装饰），pointer-events none。
- 卡片 DOM 顺序：卡 1/3/5 是 painting→text，卡 2/4 是 text→painting（与视觉左右对应，DOM 顺序影响移动端堆叠顺序 —— 移动端 painting `order:1` text `order:2` 强制统一）。
