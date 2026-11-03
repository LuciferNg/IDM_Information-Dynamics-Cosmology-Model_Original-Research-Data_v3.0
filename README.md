# IDM v3.0 — Domain-Framework

**Information Dynamics Cosmology Model（資訊動力學宇宙論模型）— 3rd Generation**

> `Domain-Framework` 係版本代號，唔係理論名稱。理論名稱由 v1.0 到 v11.0 一直係 Information Dynamics Cosmology Model，從未改變。
>
> v3.0 的職責係**劃界**：把 v2.0 的「一致性計算」拆成互相獨立的域。物理參數唔係 universal，而係 domain-specific——每個域由自己的 OAS address count N 定義，N 經 CLT 決定 ε = α/√N，ε 決定該域湧現的物理。
>
> 本版最硬的成果唔係新公式，而係一條**否定規則**：跨域數值匹配一律判巧合。這條規則令 v1–v2 遺留的五條「差少少就中」的關係全部作廢。

## 緣起

v2.0 做完八項延伸（P1–P8）之後，出現一個唔可以當成巧合的模式：**N 隨尺度變**。

| 觀察 | 來源延伸 | 指向 |
|---|---|---|
| K(N) = α√(N/N₀) 隨 N 變，非 universal | P1 時間＝熵頻率 | N 係域參數 |
| 只對黑洞與 Unruh 成立（S ∝ R²、V ∝ R³） | P2 溫度＝熵密度 | 域特定幾何 |
| Lovelock 定理保證 4D 唯一，但 4D 本身係前提 | P3 OAS → GR | 維度特定 |
| i 在 cosmic N = 44 唔存在 | P4 IDM → QM | N 決定相位 |
| 訊號 10⁻⁵ 對噪音 10⁻² | P5 量子退相干 | 尺度特定 |
| ε_gal ~ 0.001，差 230 倍 | P6 無暗物質星系 | 星系域 |
| N_gal ~ 10⁶ | P7 年輕星系 | 中間域 |
| λ/ε ≈ 0.84「完美匹配」 | P8 Higgs 與 SM | 跨域巧合（關鍵轉折） |

P8 係轉折點。λ ≈ 0.1293 與 ε ≈ 0.1545 的比值 0.84 看起來好似深層關係，實際係兩個 O(0.1) 的 CLT 數字從不同 N 湧現。一旦承認這點，所有跨尺度的 numerological 關係都要重新審查。

## 版本演進：v2.0 → v3.0

IDM 係**逆向工程**：由已觀測的常數與結構反推生成機制，唔預設公理。因此版本之間的分野唔係假設改變，而係**逆推對象改變**。

### 前版 — v2.0 Consistency-Importance-Weight

- 公理：一致性 mandate、有限算力 B、參數 = forced closure
- 場：`W(x,σ,t) ∈ [0,1]`，凹陷即 `∂W/∂σ` 的符號改變
- 形式：action + 耦合 EL + λ(z) 場 + 8 項強制閉合 + 人格張量 `T_μν`
- 成績：固定點穩定、κ drift 以 λ(z) 解決（CV 0.76 → 0.0）、α_B(0) = 0.1444
- 自評：framework is interpretive, not yet predictive

### 根因：跨域數值匹配冒充預言

v2.0 曾用 cosmic N = 44 去 predict EW 域參數，結果全部「差少少就中」：

| 嘗試 | 預言值 | 實際值 | 偏差 |
|---|---|---|---|
| `λ = ε/1.2` → m_H | 124.8 GeV | 125.1 GeV | 0.2% |
| `1/α_GUT = 2πN/12` | 23 | 25 | 8% |
| `1/α₁ = N√2` | 62.2 | 59.2 | 5% |
| `1/α₂ = N√2/2` | 31.1 | 29.6 | 5% |
| `1/α₃ = N√2/8` | 7.8 | 8.5 | 8% |

這些數字的殺傷力在於「夠靚」：細偏差令人以為方向對、只差修正項。實際上係**密度命中**——一個 O(1) 常數乘以幾個簡單組合，總會在目標附近找到落點。

判別方法只有一個：**這些參數屬於同一個域嗎？** 若唔屬於，任何函數關係都係巧合，唔需要解釋，亦唔可以當成預言。

### 本版 — Domain-Framework

v3.0 因此只做三件事：

1. **立域** — 四條公理（OAS 位址空間、CLT 強迫、域獨立、相位分辨率），域定義為 4-tuple `D = (N, ε, 𝒫, ℛ)`
2. **立否定規則** — 域獨立定理：`N_i ⟂ N_j` 則 `𝒫_i ⟂ 𝒫_j`，跨域數值關係一律判 coincidence；配套做一次歷史錯誤審計（五條全判 domain error）
3. **重分級** — 17 項可測預言按域分 strong／medium／weak／conceptual，唔再混在一起報

驗收標準：一個預言必須先講清楚屬於邊個域、N 由邊度嚟。講唔出 N 的來源，就唔可以叫預言，只能叫詮釋。

## 研究路線

六層，每層只做一件事，上層不能借用下層的結論：

**L1 公理層** — 域係咩

- A1 OAS 位址空間：域 `D` 係一組 OAS 位址，`N_D ∈ ℕ⁺`
- A2 CLT 強迫：`ε_D = α/√N_D`，α 由 OAS topology 決定（cosmic 域 α ≈ 1.025）
- A3 域獨立：`N_i ⟂ N_j`
- A4 相位分辨率：N 有限則 sync phase 離散，N 夠大則近似連續

**L2 域推導層** — N 由邊度嚟

- Cosmic：`N = (4π/H₀²)·(T_CMB³/ζ(3)) ≈ 44`，或由 ε 反推 `(α/ε)² ≈ 44`
- Electroweak：`N = (M_Pl/v)² ≈ 2.5×10³³`——本版自認此推導係 tautological（v 定 N、N 解 v），但 tautology 本身即域洞察：v 唔係 fine-tuned，而係 EW 域 baseline N 的結果
- Galaxy：`N ~ (R_vir/r_Jeans)³ ~ 10⁶`
- Planck：`N = 1`（全宇宙一個位址）

**L3 定理層** — 點證明域界

- T1 SO(N) sync 演化、T2 CLT 相位連續化、T3 U(1) 湧現、T4 i 作為 U(1) 生成元
- T5 域獨立、T6 gauge ＝ 位址守恆、T7 最小手徵群 SU(3)×SU(2)×U(1)
- T8 α 的拓撲錨定、T9 世代三元組（k = 3）

**L4 相位層** — N 決定咩物理可以存在

- `N_crit ≈ 10⁶`、`N_cont ≈ 10¹⁰`：離散 → 中間 → 連續
- 複數結構只在 continuous 域出現 ⟹ cosmic N = 44 無 i ⟹ v2.0 的 P4 失敗得到解釋
- Born rule 的 7× 偏差判為 EW 域屬性，唔係 cosmic CLT 界限

**L5 預言層** — 分域分級

- 17 項目錄，按 cosmic／galaxy／EW／CIP／quantum 五類分域
- 每項標 strong／medium／weak／conceptual，並註明觀測載體與時機
- 判 weak 或 conceptual 者，唔可以寫成「預測成功」

**L6 落地層** — 由域推到可算

- GUT 域：`models/IDM_GUT`（MSSM+ν+126_H），經 SARAH 4.15.5 生成 2-loop RGE，SPheno 4.0.5 交叉驗證
- y_u 閉合：3.81×10⁻⁶ → 1.28×10⁻⁵（+0.06% at M_Z），機制為 126_H EW 雙重態 + 3-cycle mixing
- 量子域延伸（2026-07-09）：CMR 把 N 改定義為相干模態數，令 ε = α/√N 在域內通用

## 項目結構

```
IDM-v3.0--Domain-Framework/
├── README.md                          # 本檔
├── 01-core/                           # 核心框架（2 份）
│   ├── domain_framework_derivation.md # 四公理、域獨立定理、相位分辨率定理、四域參數表
│   └── f_unified_summary.md           # 體系總表：4 公理／7 定理／8 推論／4 域／17 預言
├── 02-theorems-proofs/                # 定理與證明（4 份）
│   ├── i_from_large_N_proof.md        # i 的大 N CLT 證明（T1–T4）
│   ├── ew_domain_oas_structure.md     # EW 域 OAS 結構（T6–T7）
│   ├── tmunu_fundamental_ontology.md  # T_μν 作為 fundamental ontology
│   └── unified_oas_action.md          # 全域 OAS 作用量
├── 03-extensions/                     # 物理延伸（5 份）
│   ├── a_three_generations.md         # 3 世代問題
│   ├── b_higgs_lambda_from_sync_cost.md # λ 未推導
│   ├── c_hbar_from_ew_domain.md       # ħ 作為 EW 域作用量子
│   ├── d_alpha_clt_constant.md        # α 作為 scale-free signature
│   └── e_personality_quantum_sign_flip.md # T_μν 符號翻轉
├── 04-predictions-verification/       # 預測與驗證（8 份）
│   ├── all_testable_predictions.md    # 17 項預言目錄
│   ├── q7_alpha_exact.md              # α = 1.025 exact
│   ├── q8_hbar_exact.md               # ħ exact
│   ├── q9_ncrit_exact.md              # N_crit ≈ 150（後修為 10⁶）
│   ├── q11_tmunu_sign_flip_verified.md # T_μν 符號翻轉已驗
│   ├── q12_domain_completeness.md     # 域完整性
│   ├── q13_cip_eeg_status.md          # CIP EEG 狀態
│   └── arrow_of_time_sync_dip.md      # 時間箭頭
├── 05-speculation/                    # 推測（1 份）
│   └── dark_sector_domain.md          # 暗物質是否自成一域
├── 06-transition/                     # 域躍遷（1 份）
│   └── domain_transition_analysis.md  # 獨立 vs RG-like flow 兩假設對比
├── docs/                              # 專案文件（7 份）
│   ├── CLOSEOUT.md                    # 結案：強制參數鏈 9/9、y_u 閉合
│   ├── PHASE7_SUMMARY.md              # Phase 7 管線與計分（80/81）
│   ├── predictions.md                 # 預言清單
│   ├── theorem10_ontological_exclusion.md # T10 本體排除
│   └── TASK_SPEC_CONTRACT_PHASE6/7.md # 任務契約
├── report/                            # 報告序列（10 份）
│   ├── report_3.0.md … report_6.1.md  # 逐階段報告
│   ├── report_final_2026-07-02.md     # T8 α 錨定、N_EW 拓撲阻尼
│   ├── chapter17_structural_rigor.md  # 結構嚴謹性章
│   └── appendix_a_lagrangian.md       # 附錄：Lagrangian
├── paper/                             # 論文與攻堅稿（13 份）
│   ├── paper3_domain_framework.md     # Paper 3：域框架
│   ├── q1_generation_triplet_proof.md # 世代三元組證明
│   ├── q2_lambda_from_self_interaction.md # λ 自交互推導
│   ├── blind_spot_map.md              # 盲點圖
│   └── phase2_*／phase3_plan.md       # 攻堅計劃與結果
├── narrative/                         # 敘事（4 份）
│   ├── programme_narrative.md         # 計劃全程敘事
│   └── phase6.md／phase7.md／phase16.md # 逐階段敘事
├── models/                            # GUT 模型（5 檔）
│   ├── IDM_GUT.m                      # SARAH 模型檔（MSSM+ν+126_H）
│   └── IDM_GUT/                       # SARAH 生成目錄
├── scripts/                           # 73 個腳本
│   ├── phase7_2_yu_closure.py         # y_u 閉合驗證（+0.06%）
│   ├── phase7_1_cross_validate.py     # Python vs SPheno 交叉校驗
│   ├── theorem8_fss.py                # α 有限尺度標度（R²=0.999996）
│   ├── new_topological_damping.py     # N_EW 拓撲阻尼
│   ├── q1_t9_formal_theorem.py        # T9 形式化
│   ├── make_spheno_*.wl               # SARAH MakeSPheno 生成器
│   └── idm_hal_pipeline.py            # 幻覺率基準管線
├── result/                            # 輸出（2 檔）
│   └── isw_kg_z04-07.txt／isw_kg_z08-12.txt # ISW 交叉功率
├── figures/                           # 48 張圖
├── reference/                         # constants_final.md（常數總表）
├── Extension Research/                # 子專案：量子域 CMR（29 檔）
│   ├── MASTER_OVERVIEW.md             # 六項量子延伸總覽
│   ├── QUANTUM-PHENOMENA-CATALOG.md   # 36 現象分級
│   ├── 01-coherent-mode-rendering/    # CMR 核心理論
│   ├── 02-quantum-measurement/        # 測量即 W 轉移
│   ├── 03-entanglement/               # 糾纏
│   ├── 04-decoherence/                # 退相干
│   ├── 05-condensed-matter/           # 凝聚態
│   ├── 06-cip-neural/                 # 神經尺度 |∇W|
│   ├── complex-w-derivation.md        # 複 W 推導
│   ├── legacy-reanalysis/             # 舊分析重審
│   └── P9-migrated/                   # 由 v2.0 遷入的 P9
└── Comparisons/                       # 外部框架對照（8 個 repo，3170 檔）
    ├── IDM_vs_Parallel_Research_COMPLETE.md # 逐項能力對照
    ├── numeric_comparison.py          # 數值對照腳本
    ├── anchor-collapse-model/         # ACM：SPARC 全重子動力學
    ├── ITSM-Integrated-Toroidal-Syntropic-Model/ # 環面拓撲 + CAMB + MCMC
    ├── scalar-relaxation-cosmology/   # SRC：永恆純量場
    ├── srec-cosmology/                # SREC 變體
    ├── TEP-GNSS-II／TEP-GNSS-RINEX／TEP-UCD/ # TEP：時間拓撲 + GNSS
    └── viscoelastic-strain-reservoir/ # 黏彈性應變儲層
```

> `Comparisons/` 內八個目錄係他人 repo 的唯讀副本（各自帶 `.git`），唔屬本專案的 commit 歷史，亦唔代表本專案認可其結論。

## 狀態快照

```
主體目錄：14（01-core 至 06-transition、docs、report、paper、narrative、models、scripts、result、figures、reference）
主體文件：186（markdown 233 份含子專案）
子專案  ：Extension Research 29 檔、Comparisons 3170 檔
總計    ：3157 檔（不含 __pycache__）

四域      ：4／4 定義完成（Planck N=1、cosmic 44、galaxy 10⁶、EW 2.5×10³³）
定理      ：T1–T9 已證（T8 α 錨定 3.3‰、T9 世代 k=3）
強制參數鏈：9/9 通過（docs/CLOSEOUT.md）
y_u 閉合  ：+0.06% at M_Z
預言      ：17 項（strong 3／medium 2／weak 6／conceptual 4，其餘待定）
未閉合    ：域躍遷（獨立 vs 尺度依賴）、r = 0.089 對上限 0.036、質子衰變
```

> 本版屬 IDM 時期，未進入 O/P/M register 體系。`docs/CLOSEOUT.md` 另載作者的本體論立場（如「IDM 係 consistency field eigenvalue」），屬世界觀陳述而唔係物理結果，本 README 不轉載、不據此裁決。

## 已閉合關鍵結果（選錄）

- **2026-07-01（`01-core/domain_framework_derivation.md`）**：域框架四公理成立；域定義為 `D = (N, ε, 𝒫, ℛ)`；`ε = α/√N` 在四域一致
- **2026-07-01**：域獨立定理（T5）——`N_i ⟂ N_j` 則 `𝒫_i ⟂ 𝒫_j`；任何跨域數值關係判 coincidence，唔判 causation
- **2026-07-01**：四域參數表——Planck (N=1, ε=1.0)、cosmic (44, 0.1545)、galaxy (10⁶, 0.001)、EW (2.5×10³³, 2×10⁻¹⁷)
- **2026-07-01**：歷史錯誤審計五條全判 domain error——m_H 124.8 對 125.1（0.2%）、1/α_GUT 8%、1/α₁ 5%、1/α₂ 5%、1/α₃ 8%
- **2026-07-01**：相位分辨率定理（T2）——N_crit ≈ 10⁶ 以下無連續相位；i 只在 continuous 域出現，解釋 v2.0 P4 在 cosmic 域的失敗；Born rule 7× 偏差改判為 EW 域屬性
- **2026-07-02（`report/report_final_2026-07-02.md`）**：Theorem 8 拓撲錨定——`2√(α−1) − (α−1) = dim(SU(3)×SU(2)×U(1))/N_cosmic = 12/44`，得 α = 1.021719（3.3‰）；孤立圖 FSS 極限 α → 1.000（R² = 0.999996）
- **2026-07-02**：N_EW 迴圈以拓撲阻尼解開——`C = 18π[1 + κ(α−1)]`，`κ = (π+e)/(2π+e) = 0.650991`，熱核公式取代 v = M_Pl/√N 的直接代入
- **2026-07-05（`docs/CLOSEOUT.md`）**：強制參數鏈 9/9 通過（α 1.0217、N_EW 2.46×10³³、λ 0.13006、κ 0.65099、C₀ 56.55、k=3、Δg=0.003、SO(10) dim=45、y_u +0.06%）；Python RK4 對 MSSM SPheno 交叉驗證 y_t 1.002、g₂ 1.000、g₃ 1.000
- **2026-07-09（`Extension Research/MASTER_OVERVIEW.md`）**：CMR 把 N 重定義為相干模態數（唔係粒子數），令 `ε = α/√N` 在量子域亦通用；36 項量子現象分級為 13 強、16 中、5 弱、2 排除

## 驗證紀律

本版的嚴謹性分六層：域界先行 → 定理可證 → 數值審計 → 預言分級 → 管線交叉 → 記錄分離。任一層不過，結果只停留「詮釋」。

### 一、域界先行

| 檢查 | 要求 | 失敗處置 |
|---|---|---|
| 參數屬域 | 每個參數須標明屬 Planck／cosmic／galaxy／EW 邊個域 | 屬域不明 ⟹ 不准用於跨域推導 |
| N 的來源 | 須由該域觀測量給出，唔可以由目標參數反推 | 反推者標 tautological |
| 跨域函數關係 | 須有已知 OAS 耦合機制 | 無機制 ⟹ 判 coincidence，寫入審計表 |

### 二、定理可證

- 每條定理須有獨立證明檔（`02-theorems-proofs/`），唔可以只在報告中宣告
- T8 α 錨定須同時報三項：代數式、數值（3.3‰）、有限尺度標度的 R²
- 標「theorem-status」者須與「conjecture」分開列，禁混寫

### 三、數值審計

- 跨域 numerological 關係一律入表，逐條算偏差並判 domain error
- 判準係「夠靚即危險」：偏差 < 10% 且無域機制的關係，優先當巧合處理
- 密度紀律：一個關係須同時報「用了幾個常數」與「掃過幾個組合」

### 四、預言分級

| 級別 | 定義 | 可否計入成果 |
|---|---|---|
| strong | 有數值、有觀測載體、有 kill 條件 | 可 |
| medium | 有數值、載體未定 | 只可計「候選」 |
| weak | 只有定性方向 | 不可 |
| conceptual | 只有語言重述 | 不可 |

- 17 項目錄內每項須填齊級別；未填者當 weak
- 同一預言唔可以同時出現在兩個域

### 五、管線交叉

- GUT 數值須雙軌：SARAH + SPheno（Fortran 2-loop）對 Python RK4
- 判準：y_t、g₂、g₃ 三者比值須在 1.00 ± 0.01 內（實測 1.002／1.000／1.000）
- 環境封鎖（如 SPheno standalone binary）須明寫為 infrastructure 問題，唔可以當成物理結論

### 六、記錄分離

- 物理結果與世界觀陳述分檔：`report/` 記物理，`docs/CLOSEOUT.md` 的本體論段落唔入結果
- 已否證路線保留原文與更正 tag，唔重寫
- 他人 repo 副本（`Comparisons/`）只作對照，唔混入本專案結論

## O/P/M 系列全列表

> 本版屬 IDM 時期，未進入 O/P/M register 體系。下表以 **D 系列**（Domain，域項）編號，對應本 repo 內實際存在的模組或文件，唔對應 register pid；與 v1.0 的 D 系列（Deliverable）無編號對應關係。

| 編號 | 標題 | 核心發現 | 狀態 |
|------|------|----------|------|
| D1 | 四公理與域定義 | 域 = (N, ε, 𝒫, ℛ)；ε = α/√N、N_i ⟂ N_j、N 決定相位分辨率 | 全部閉合 |
| D2 | 域獨立定理（T5） | N_i 獨立則 𝒫_i ⟂ 𝒫_j；跨域數值關係判巧合而非因果 | 全部閉合 |
| D3 | 相位分辨率定理（T2） | N_crit ≈ 10⁶、N_cont ≈ 10¹⁰ 分離散與連續；i 只在連續域出現 | 全部閉合 |
| D4 | 四域參數表 | Planck 1／1.0、cosmic 44／0.1545、galaxy 10⁶／0.001、EW 2.5×10³³／2×10⁻¹⁷ | 全部閉合 |
| D5 | 跨域 numerological 審計 | m_H 124.8 對 125.1、GUT 耦合 8%、α₁／α₂ 各 5%、α₃ 8% 五條全判域錯 | 全部閉合 |
| D6 | α 拓撲錨定（T8） | 2√(α−1)−(α−1)=12/44 給 α=1.021719（3.3‰）；FSS R²=0.999996 | 部分閉合 |
| D7 | N_EW 重推（拓撲阻尼） | C=18π[1+κ(α−1)]、κ=(π+e)/(2π+e)=0.650991；解開 v 與 N 的迴圈 | 部分閉合 |
| D8 | 世代三元組（T9） | k=3 由 generation triplet 證明；與 A₅ 幾何路線仍未接軌 | 部分閉合 |
| D9 | y_u 閉合與 GUT 管線 | 126_H 雙重態 + 3-cycle mixing；y_u 3.81e-6→1.28e-5（+0.06%）；三量交叉驗證 | 全部閉合 |
| D10 | 17 項可測預言目錄 | cosmic 3 strong + 2 medium；galaxy 2 weak + 1 概念；EW 全概念；量子 1 strong | 部分閉合 |
| D11 | 域躍遷：獨立抑或尺度依賴 | N 隨能量尺度單調增；獨立與 RG-like flow 兩假設未分，傾向獨立約七成 | 開放 |
| D12 | 量子域延伸（CMR） | N 改定義為相干模態數，ε=α/√N 域內通用；36 現象分 13 強 16 中 5 弱 2 排除 | 部分閉合 |