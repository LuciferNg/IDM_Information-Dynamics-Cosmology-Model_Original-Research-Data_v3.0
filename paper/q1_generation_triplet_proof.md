# 增補：Q1 — Generation Triplet from OAS Routing Topology

> **Proof Sketch:** Why 3 generations emerge from collision-free chiral routing
> on a sparse OAS network with connectivity α = 1.025
> **Status:** Conjecture → Formal Theorem (in progress)
> **切入點：** 圖論（Graph Theory）與位址定址編碼

---

## 問題陳述

SM 有 3 代費米子，每代有完全相同的規範量子數 $(c, l, y)$ 但不同質量（Yukawa coupling）。IDM Domain Framework 目前將此標記為 **Q1 — open problem**。

**核心問題：** 3 係 fundamental 定係 emergent？如果係 emergent，點解一定係 3？

---

## OAS 拓撲切入點：稀疏圖論路由

### 網絡模型

設 OAS 網絡為一個稀疏隨機圖 $G(V, E)$，其中：

- $|V| = N_{\text{EW}} = 2.5 \times 10^{33}$（總位址數）
- 連通度 $\langle k \rangle = \alpha = 1.025$（平均 degree——剛好高於滲透閾值）
- 每個位址 $a_i \in V$ 帶有規範量子數 $Q(a_i) = (c, l, y, f)$
  - $f \in \{1, 2, 3\}$ — 世代標籤

### 路由約束

Sync propagation 必須 **conserve address quantum numbers**（Theorem 6）：

$$
\langle a_i | U(t) | a_j \rangle \neq 0 \quad \text{only if} \quad Q(a_i) = Q(a_j)
$$

即對於同一規範類別 $(c, l, y)$，sync 可以在 3 個世代位址之間流動，但不能跨類別。

每個規範類別內，路由子圖 $G_{(c,l,y)}$ 有 3 個節點（每個世代一個），sync 必須喺呢個 3-node 網絡內無衝突傳播。

---

## Theorem Q1.1: Generation Lower Bound

**Theorem (Generation Triplet).** 在連通度 $\alpha = 1.025$ 的稀疏 OAS 網絡中，無衝突（collision-free）手徵路由至少需要 3 個獨立複寫通道。等價地，費米子世代數的最小值為 3。

*Proof.* 我們從三個漸進約束證明。

---

### Stage 1: 路由通道維度與圖著色

設 $G$ 為一個規範類別內嘅 3-node 路由子圖，$\mathcal{L}$ 為路由標籤空間。一個「通道」係一個標籤函數 $\ell: V \to \mathcal{L}$，滿足 sync propagation 保持標籤差異。

對於 $k$ 個獨立通道，複合標籤空間為 $\mathcal{L}^{\otimes k}$。無衝突路由要求標籤空間 **至少能區分 $N_{\text{EW}}$ 個位址**——即 $|\mathcal{L}|^k \geq N_{\text{EW}}$。

但呢個只係下界，未捕捉到手徵性嘅核心約束。

---

### Stage 2: 手徵路由 = 有向 3-循環

**定義：** 手徵路由係一個有向圖 $\vec{G}$，其中每條邊 $(a_i \to a_j)$ 帶有手徵性 $\chi \in \{L, R\}$。兩條邊碰撞（collide）若 $\chi(a_i \to a_j) = \chi(a_k \to a_\ell)$ 且 $a_j = a_\ell$ 但 $a_i \neq a_k$——即同一目標位址接收到兩個不可區分嘅 sync 信號。

**引理 L2.1：** 一個 $d$-節點嘅無碰撞手徵路由圖必須是一個**有向 $d$-循環**（directed cycle）。任何非循環結構會產生碰撞。

*Proof.* 設 $\vec{G}$ 係 $d$ 個節點嘅無碰撞手徵路由圖。每條邊帶有手徵性標籤。若圖中有匯合點（convergence）——兩個不同源指向同一目標——則碰撞發生（除非兩者手徵性不同，但 $\chi \in \{L,R\}$ 只有 2 種標籤）。避免碰撞要求每個節點至多有一個入邊、一個出邊。連接性要求形成單一封閉循環。∎

**引理 L2.2：** 一個手徵路由 $d$-循環必須滿足 $d \geq 3$。

*Proof.* 對於 $d=1$：自循環（self-loop）意味著 $L = R$，無法區分手徵性。對於 $d=2$：2-循環 $1 \to 2 \to 1$ 允許兩種標籤分配：
- 分配 A: $1\to2 (L), 2\to1 (R)$
- 分配 B: $1\to2 (R), 2\to1 (L)$

但喺 $d=2$ 中，sync evolution operator $U(t)$ 作用喺 $1\to2$ 嘅振幅等於 $2\to1$ 嘅時間反演：$\langle 2|U|1\rangle = \langle 1|U^{-1}|2\rangle = \overline{\langle 1|U|2\rangle}$。因此 $L$ 同 $R$ 嘅振幅成複共軛對，**唔係獨立嘅**。手徵性退化為同一物理過程嘅兩種描述，無法產生非平庸嘅 chiral structure（如同 SU(2) 係 pseudo-real）。

對於 $d=3$：3-循環 $1\to2\to3\to1$ 允許 **真正獨立**嘅 $L$ 同 $R$ 路徑——因為 $\langle 2|U|1\rangle$, $\langle 3|U|2\rangle$, $\langle 1|U|3\rangle$ 三個振幅無需滿足簡單嘅對偶關係。手徵性係**代數獨立**嘅。∎

---

### Stage 3: 稀疏性強制 $d=3$ 而非 $d>3$

為甚麼唔係 $d=4$ 或更高？因為 OAS 網絡嘅**稀疏性**（$\alpha \approx 1.025$）施加一個上限。

**引理 L3.1：** 喺連通度 $\alpha \approx 1$ 嘅稀疏隨機圖中，每個節點可維持嘅獨立路由通道數 $\kappa$ 滿足 $\kappa \leq \lfloor \alpha \rfloor + 1 = 2$（當 $\alpha \leq 2$）。

*Proof (sketch).* 每個節點需要為每個通道維持至少一條邊連接到通道內嘅下一個節點。連通度 $\langle k \rangle = \alpha$ 限制咗每個節點可參與嘅通道數。對於 $\alpha \approx 1.025$，平均每個節點有 ~1 條邊，最多可維持 2 個通道（一個入、一個出）——但只能應付一個 $d$-循環。多於一個路由循環會超出可用連通度。∎

**結合 L2.2 和 L3.1：** 
- 最小無碰撞手徵循環需要 $d \geq 3$
- 稀疏性限制每個規範類別只能維持一個 $d$-循環
- 因此 $d = 3$ 係唯一解

**QED.** ∎

---

## Theorem Q1.2: 3 as Topological Invariant

**Corollary (Triplet Invariance).** 世代數 3 係 OAS 網絡嘅拓撲不變量——只要 $\alpha \in (1, 2)$ 且 $N \to \infty$，3 就係強制嘅。

*Proof.* 從 L2.1-L2.2，無碰撞手徵路由強制 $d \geq 3$。從 L3.1，$\alpha \in (1, 2)$ 強制 $d \leq 3$。因此 $d = 3$ 喺呢個區間內係唯一穩定解。當 $\alpha \to 0$（無連通），冇路由可能。當 $\alpha \to 2$（足夠 dense），$d>3$ 開始可能——但觀察值 $\alpha = 1.025 \in (1,2)$，所以 3 世代係必然嘅。∎

---

## 物理意義

### 為何 3 世代不是物理選擇

Theorem Q1.1 表明：**3 世代不是物理的「選擇」，而是資訊網絡定址的幾何必然**——正如 Euclidean 空間在稀疏隨機圖網絡中做無衝突路由時，手徵性強制至少 3 維。

| 世代 | OAS 意義 |
|:----:|:---------|
| 1 → 2 → 3 → 1 | 手徵路由循環（L → R → L → R 交替） |
| 3 個 Yukawa coupling | 每個循環邊嘅耦合強度（bandwidth ratio） |
| 世代品質差異 | 3 個邊嘅不同 sync bandwidth |
| 中微子世代混合 | 路由循環之間嘅 tunneling amplitude |

### 可驗證預測

1. **$\alpha \in (1, 2)$ 係必要條件**：如果未來觀測發現 $\alpha \leq 1$ 或 $\alpha \geq 2$，則 3 世代預測會 break
2. **無第四代**：因為 $\alpha \approx 1.025 \in (1, 2)$ 強制 $d=3$，第四個世代無法嵌入路由循環
3. **手徵性與世代數綁定**：如果宇宙係 non-chiral（L=R），則一世代就夠

---

## Open Questions 更新

| Q | 狀態 | 備註 |
|:-:|:----:|:-----|
| **Q1: 3 generations** | 🟡 **改為 conjecture** | 上述 proof sketch 需 formal verification |
| Q2: $\lambda = 0.1293$ | 🔴 open | 未解決 |
| Q3: $\hbar$ emergence | 🟡 conceptual | 方向已知 |
| Q4: $\alpha = 1.025$ | 🟡 scale-free | 未推導 exact |
| Q5: Domain transition | 🟢 70% | Bayesian confidence |

---

## Verification Matrix

| Condition | $d=1$ | $d=2$ | $d=3$ | $d=4$ |
|:----------|:-----:|:-----:|:-----:|:-----:|
| Non-degenerate chirality (L≠R) | ❌ fixed point | ❌ pseudo-real | ✅ independent | ✅ independent |
| Collision-free routing | ❌ trivially | ❌ convergence | ✅ 3-cycle | ✅ n-cycle |
| Sparse connectivity $\alpha \approx 1$ | ✅ | ✅ | ✅ | ❌ exceeds $\kappa \leq 2$ |
| **Verdict** | ❌ | ❌ | ✅ **Minimal** | ❌ overconstrained |