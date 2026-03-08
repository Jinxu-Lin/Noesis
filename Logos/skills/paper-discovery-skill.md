# Skill: Paper Discovery (论文发现与筛选) — Phase 0

## 触发场景
研究者设定或更新研究方向后，手动触发。定期执行以发现新发表的论文。

## 输入
- 研究方向配置文件 `research-directions.md`（位于知识库目录）
  - 包含：研究主题、核心关键词、扩展关键词、种子论文列表、关注的作者、目标venue列表
- `reading-queue.md`（如已存在，避免重复添加）
- 知识库索引 `kb-index.md`（如已存在，避免与已读论文重复）

## 执行流程

### Step 1: 解析研究方向
读取 `research-directions.md`，提取：
- 搜索关键词（核心 + 扩展）
- 种子论文 ID（用于引用链追踪）
- 目标 venue 列表（用于质量过滤）
- 已关注作者列表

### Step 2: 多策略论文发现
按以下策略并行搜索：

**策略 A: 关键词搜索**
- 使用 arXiv API 搜索: `http://export.arxiv.org/api/query?search_query=...`
- 使用 Semantic Scholar API 搜索: `https://api.semanticscholar.org/graph/v1/paper/search?query=...`
- 关键词组合：核心关键词 × 扩展关键词
- 时间范围：首次执行搜索近2年，后续执行搜索上次执行以来的新论文
- 每次搜索返回按相关性排序的结果

**策略 B: 引用链追踪**（首次执行或有新种子论文时）
- 对种子论文，通过 Semantic Scholar API 获取：
  - 引用了该论文的后续工作（forward citations）
  - 该论文引用的基础工作（backward references）
- 重点关注高引用的后续工作

**策略 C: 作者追踪**
- 通过 Semantic Scholar Author API 获取关注作者的最新发表

**策略 D: Venue 追踪**
- 搜索目标 venue 最新一届的论文列表

**策略 E: 争议与反面证据搜索**
- 使用 WebSearch 搜索："{研究方向} + negative results"、"{方法名} + failure analysis"、"{方法名} + replication"
- 搜索社区争论："{方法名} + limitations / criticism / debate"
- 目标：发现负面结果论文、复现失败报告、方法争议——这些往往揭示真正的瓶颈，比正面结果更有 Gap 价值
- 每个研究方向至少执行一次
- 发现的争议性论文即使没有顶会发表也应纳入（negative results 天然发表困难）

### Step 3: 去重与质量过滤

合并所有策略的结果，执行：

1. **去重**: 按论文 ID (arXiv ID / DOI / Semantic Scholar ID) 去重
2. **排除已读**: 与 `kb-index.md` 比对，排除已在知识库中的论文
3. **排除已排队**: 与 `reading-queue.md` 比对，排除已在队列中的论文
4. **质量过滤**:
   - 优先: 发表在目标 venue 的论文
   - 优先: 引用数较高的论文（考虑发表时间归一化）
   - 降权: 未经同行评审的低引用预印本

### Step 4: Tier 1 Quick Scan（快速扫描）

对过滤后的论文进行快速扫描，每篇仅阅读：
- Title
- Abstract
- Introduction（如可获取）
- Conclusion（如可获取）

对每篇论文评估：

| 维度 | 评分 1-5 | 说明 |
|------|---------|------|
| 研究方向相关性 | | 与设定的研究方向匹配程度 |
| 方法可复用性 | | 核心方法/组件是否有迁移到自身研究的潜力 |
| 知识库互补性 | | 是否填补 KB 中的空白（新方法/新视角/新数据集） |
| 隐式假设潜力 | | 是否存在可被质疑的假设（高价值 Gap 来源） |

**综合评分** = 各维度加权平均（相关性权重最高）

**决策阈值**:
- 综合评分 ≥ 4: 加入深读队列（高优先）
- 综合评分 3: 加入深读队列（普通优先）
- 综合评分 ≤ 2: 跳过，仅记录 metadata

### Step 5: 更新阅读队列

将通过 Quick Scan 的论文写入 `reading-queue.md`，每篇包含：
- 论文元信息（标题、作者、venue、年份、arXiv ID）
- Quick Scan 摘要（一句话总结 + 评分）
- 深读优先级（高 / 普通）
- 发现策略来源（关键词 / 引用链 / 作者追踪 / venue追踪）
- 状态：待读

### Step 5.5: Git 提交队列更新
```bash
git add reading-queue.md
git commit -m "kb: paper discovery [日期] — +[N]篇待读"
git push origin main  # 或当前分支，跨服务器场景需 push 以同步
```

### Step 6: 发现报告

向用户汇报本次发现结果：
- 搜索覆盖范围（时间段、关键词、venue）
- 发现论文总数 → 过滤后数量 → 通过 Quick Scan 数量
- 高优先深读论文列表（标题 + 一句话理由）
- 发现的潜在研究趋势或热点（如果从论文分布中观察到）

## AI Co-Author 关键行为
- 搜索策略要有创造性——不只是字面关键词匹配，要理解研究方向的语义并生成多样化查询
- Quick Scan 时重点关注"隐式假设潜力"——这是未来 Gap Discovery 的核心输入
- 主动识别论文集群中的研究趋势——哪些方向在升温、哪些在降温
- 发现与知识库中已有条目形成 cross-paper connection 的论文时，标注并提升优先级
- 对 Quick Scan 评分要诚实——不因数量压力而降低标准

## 输出
- `reading-queue.md`（更新）
- 发现报告（直接输出给用户）

## Exit Criteria
- [ ] 至少使用了 2 种以上发现策略
- [ ] 对该研究方向执行了至少一次"争议与反面证据"搜索（策略 E）
- [ ] 所有发现的论文都经过去重和质量过滤
- [ ] 通过 Quick Scan 的论文都有评分和一句话摘要
- [ ] reading-queue.md 已更新
- [ ] reading-queue.md 更新已 git commit（+ push，如多服务器场景）
- [ ] 向用户汇报了发现结果

## 完成后
提示用户：论文发现完成，阅读队列已更新。建议执行 `/paper-reading` 对高优先论文进行深度阅读。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
