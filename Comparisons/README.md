# Comparisons — IDM 與平行研究之對照

**IDM v3.0 Domain-Framework — 第三方模型對照目錄**

> 本目錄放兩類東西：**本專案產出的對照分析**（會上傳），與 **8 個第三方 repo 的本地 clone**（唔上傳）。
>
> 2026-11-03 起，第三方 repo 一律唔入庫 —— 它們各有自己的作者、授權與 commit 歷史，混入本 repo 只會造成 gitlink 與 `.gitignore` 互相干擾（過去 ITSM 曾出現 index 被清空、4,595 項假刪除的狀態）。

## 本專案產出（會上傳）

| 檔案 | 內容 |
|---|---|
| `IDM_vs_Parallel_Research.md` | 對照分析（精簡版） |
| `IDM_vs_Parallel_Research_COMPLETE.md` | 對照分析（完整版，含數值表） |
| `numerical_comparison.py` | 數值對照腳本 |

## 第三方 repo（唔上傳，需自行 clone）

| 目錄 | 上游 remote | 主題 |
|---|---|---|
| `anchor-collapse-model/` | `lesleyliuhaitao-ctrl/anchor-collapse-model` | Anchor collapse |
| `ITSM-Integrated-Toroidal-Syntropic-Model/` | `brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model` | 環面熵模型（ITSM） |
| `scalar-relaxation-cosmology/` | `warpXspeed/scalar-relaxation-cosmology` | 純量弛豫宇宙學 |
| `srec-cosmology/` | `warpXspeed/srec-cosmology` | SREC 宇宙學 |
| `TEP-GNSS-II/` | `matthewsmawfield/TEP-GNSS-II` | TEP GNSS 分析 II |
| `TEP-GNSS-RINEX/` | `matthewsmawfield/TEP-GNSS-RINEX` | TEP GNSS RINEX 數據 |
| `TEP-UCD/` | `matthewsmawfield/TEP-UCD` | TEP UCD |
| `viscoelastic-strain-reservoir/` | `warpXspeed/viscoelastic-strain-reservoir` | 黏彈性應變儲層 |

### 重建指令

```bash
cd Comparisons

for r in anchor-collapse-model ITSM-Integrated-Toroidal-Syntropic-Model \
         scalar-relaxation-cosmology srec-cosmology \
         TEP-GNSS-II TEP-GNSS-RINEX TEP-UCD viscoelastic-strain-reservoir; do
  case $r in
    anchor-collapse-model)                  url="https://github.com/lesleyliuhaitao-ctrl/$r.git" ;;
    ITSM-Integrated-Toroidal-Syntropic-Model) url="https://github.com/brendohxd/$r.git" ;;
    TEP-*)                                  url="https://github.com/matthewsmawfield/$r.git" ;;
    *)                                      url="https://github.com/warpXspeed/$r.git" ;;
  esac
  [ -d "$r" ] || git clone --depth 1 "$url" "$r"
done
```

## 上傳政策

```
會上傳   IDM_vs_Parallel_Research.md
         IDM_vs_Parallel_Research_COMPLETE.md
         numerical_comparison.py
         README.md（本檔）

唔上傳   Comparisons/*/  ← 全部第三方 repo（.gitignore 已排除）
```

理由：

1. **授權與歸屬** —— 第三方碼各有作者與授權條款，唔應由本 repo 轉載
2. **體積** —— ITSM 單一 repo 已 2,692 個 tracked 檔案
3. **gitlink 污染** —— 過去以 gitlink 形式追蹤但冇 `.gitmodules`，導致 clone 後得到空目錄，而本地 index 又與上游 commit 不同步
4. **可重建** —— 以上游倉庫為唯一真實來源，本目錄只記錄 URL 與重建指令

## 狀態快照

```
本專案檔          4（3 個分析檔 + 本 README）
第三方 repo       8（本地存在，唔上傳）
ITSM 狀態         2026-11-03 重新 clone：2,692 tracked、status clean、HEAD bac3ccb
```

## 驗證紀律

### 一、第三方碼唔改

clone 後唔修改、唔 commit、唔 push 回上游。任何對照需要的改動，寫在本專案的 `numerical_comparison.py` 或分析文件中。

### 二、版本要記錄

引用第三方結果時，記錄其 commit SHA 與日期，唔寫「最新版」。

### 三、對照要可重跑

`numerical_comparison.py` 必須能在有第三方 repo 的環境下直接跑出對照表。

## 檔案全列表

| 編號 | 標題 | 核心發現 | 狀態 |
|------|------|----------|------|
| C1 | IDM vs 平行研究（精簡） | 對照分析概要 | 部分閉合 |
| C2 | IDM vs 平行研究（完整） | 含數值表的完整對照 | 部分閉合 |
| C3 | 數值對照腳本 | numerical_comparison.py 可重跑 | 部分閉合 |
| C4 | 第三方 repo 隔離 | 8 個上游 repo 移出追蹤，改以 URL + 重建指令記錄 | 全部閉合 |