# $g_1, g_2, g_3$ — 拓撲切入方向探索

> **Status:** 🔴 **Open Problem** — 目前 framework 中最不成熟的 one
> **C2 約束：** N_horizon=44 不能預測規範耦合（Gauge Unification Fallacy 已證明）
> **可能方向：** EW domain 嘅 OAS sync structure → gauge coupling relation via RG flow

---

## 1. 問題陳述

SM 嘅三個規範耦合喺 EW scale $v = 246$ GeV 嘅值：

| Coupling | Value at $M_Z$ | Group | 生成元數 |
|:---------|:--------------:|:-----:|:--------:|
| $g_1$ | 0.357 | $U(1)_Y$ | 1 |
| $g_2$ | 0.652 | $SU(2)_L$ | 3 |
| $g_3$ | 1.221 | $SU(3)_c$ | 8 |

Running：$\frac{dg_i}{d\ln\mu} = \frac{b_i}{16\pi^2} g_i^3$

SM beta function coefficients：$(b_1, b_2, b_3) = (41/10, -19/6, -7)$

---

## 2. C2 約束（已證明）

**已知：** Cosmic domain 嘅 $N_{\text{horizon}} = 44$ **不能**預測 $g_1,g_2,g_3$。

原因：
- Domain Independence Theorem (T5) 證明 $N_i \perp N_j$
- Gauge Unification Fallacy (C2) 明確禁止 cross-domain prediction
- 任何嘗試用 cosmic N 推 gauge coupling 嘅方案都係 methodologically invalid

**這意味著：** $g_1,g_2,g_3$ 必須從 **EW domain 內部** 嘅 OAS structure 導出，唔可以從 cosmic N 推。

---

## 3. 可能切入方向

### 方向 A：EW Domain Sync Curvature

喺 $N_{\text{EW}} = 2.5\times10^{33}$ 嘅 OAS 網絡中，每個 gauge subgroup 對應一個 **sync curvature**：

$$
g_i^2(M_{\text{EW}}) \sim \frac{\alpha_i}{\text{Vol}(\mathcal{M}_i)}
$$

其中 $\mathcal{M}_i$ 係 gauge group $G_i$ 嘅 OAS 流形，$\text{Vol}(\mathcal{M}_i)$ 係其 volume。

對於 $U(1)$：$\text{Vol}(U(1)) = 2\pi$
對於 $SU(2)$：$\text{Vol}(SU(2)) = 2\pi^2$
對於 $SU(3)$：$\text{Vol}(SU(3)) = \pi^3$

呢個會給出 $g_1^2 : g_2^2 : g_3^2 \propto 1/2\pi : 1/2\pi^2 : 1/\pi^3$，但比例不對應 SM 值。

### 方向 B：Sync Bandwidth per Generator

每個 gauge group 嘅 sync bandwidth 等於總 sync bandwidth $\alpha$ 除以生成元數：

$$
g_i \propto \frac{\alpha}{\sqrt{\dim(G_i)}}
$$

For $U(1)$: $\dim = 1$ → $g_1 \propto \alpha = 1.025$
For $SU(2)$: $\dim = 3$ → $g_2 \propto \alpha/\sqrt{3} = 0.592$
For $SU(3)$: $\dim = 8$ → $g_3 \propto \alpha/\sqrt{8} = 0.362$

但觀測值：$g_1=0.357, g_2=0.652, g_3=1.221$——順序相反（$g_3$ 最大但預測最小）。

**結論：** 呢個 naive scaling 唔 work，因為 **RG running 主導** 了耦合嘅相對大小。

### 方向 C：RG Flow 作為 OAS Sync Flow

RGE 可以 reinterpret 為 OAS 嘅 **sync resolution scale flow**：

$$
\frac{dg_i}{d\ln\mu} = \frac{b_i}{16\pi^2} g_i^3, \quad
\mu \leftrightarrow \frac{1}{\ell_{\text{sync}}}
$$

其中 $\ell_{\text{sync}}$ 係 OAS 網絡嘅 sync coherence length。

**關鍵 insight：** $b_i$ 係由 **fermion generation count**（3）決定嘅。既然 Q1 嘅 3-cycle 證明 3 世代係圖論強制，則 $b_i$ 就唔係自由參數。

**可能嘅突破：** 如果：
1. Q1 證明 3 世代係強制嘅（已做）
2. Q2 證明 $\lambda$ 來自 $N_{\text{EW}}$ 嘅自交互（候選公式已找到）
3. 則 $g_1,g_2,g_3$ 喺 GUT scale 可能由 OAS 決定，而 RGE 由 3 世代固定

但 GUT scale 嘅耦合值仍需要 OAS 推導。

---

## 4. 當前最卡點

| 問題 | 阻礙 | 難度 |
|:-----|:-----|:----:|
| 冇 GUT-scale boundary condition | OAS 冇 predict 高能 unification scale | 🔴 |
| $g_i$ 嘅 running 主導相對值 | 任何 tree-level OAS 預測會被 RG flow 沖淡 | 🔴 |
| 3 世代嘅證明未嵌入 gauge sector | Q1 只證明咗 fermion generations，未證明 beta functions | 🟡 |
| OAS 嘅 gauge coupling 定義未形式化 | 需要 OAS 嘅 gauge theory 完整 formalization | 🔴 |

---

## 5. 下一步建議

1. **先完成 Q1 同 Q2**——佢哋嘅結果會制約 gauge coupling 嘅可能值
2. **探索 OAS 嘅 gauge theory formalization**——定義 $g_i$ 喺 OAS 網絡中嘅幾何意義
3. **使用 $N_{\text{EW}}$ 同 $\alpha$ 作為 boundary condition**——可能喺 $M_{\text{Pl}}$ scale 處 $g_i^2 \sim \alpha^2/N_{\text{EW}}$
4. **數值驗證**——用 known RGE 從 $M_{\text{Pl}}$ 跑到 $M_Z$，check 是否 match SM 值

**目前 verdict：** $g_1,g_2,g_3$ 係三個 ragnarok 問題中最唔成熟嘅一個，**不建議在 Paper 3 中聲稱任何進展**。最佳策略係標記為 open problem 並指出 Q1 同 Q2 嘅進展為未來解決佢提供咗必要基礎。