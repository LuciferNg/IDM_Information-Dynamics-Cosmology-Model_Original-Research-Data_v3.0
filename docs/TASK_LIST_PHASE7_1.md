# Phase 7.1 Task List — Wolfram Engine + SARAH + SPheno y_u Closure

## 前置條件

已有：
- `/tmp/SPheno-4.0.5/` — SPheno 4.0.5 已編譯，MSSM mSUGRA spectrum 已產出
- `/tmp/WolframEngine_15.0_LINUX.sh` — 2.2GB 安裝器已下載
- `/home/wsl/IDM-Domain-Framework/` — 主 repo
- `/home/wsl/IDM-Domain-Framework/scripts/phase7_1_rge_solver.py` — 2-loop RK4 MSSM RGE solver（已驗證 y_t 0.928 = 0.993× obs）
- `/home/wsl/IDM-Domain-Framework/models/IDM_GUT.m` — OAS SO(10) SARAH model skeleton

## 任務 1：安裝 Wolfram Engine

```bash
sudo sh /tmp/WolframEngine_15.0_LINUX.sh --target /opt/wolfram-engine --nox11
# 需要：sudo password + Wolfram ID 免費註冊
# 參考：https://www.wolfram.com/engine/
```

完成後驗證：
```bash
/opt/wolfram-engine/Executables/wolfram -version
```

## 任務 2：下載並安裝 SARAH

```bash
cd /tmp
wget https://www.hepforge.org/archive/sarah/SARAH-4.15.1.tar.gz
tar xzf SARAH-4.15.1.tar.gz
mkdir -p ~/.Mathematica/Applications/
cp -r SARAH-4.15.1/* ~/.Mathematica/Applications/
```

驗證：
```bash
/opt/wolfram-engine/Executables/wolfram -run "Needs[\"SARAH\`\"]; Print[\"SARAH loaded\"]"
```

## 任務 3：編寫 OAS GUT SARAH 模型

File: `/home/wsl/IDM-Domain-Framework/models/IDM_GUT.m`

模型規格：
- Gauge group: SO(10) → MSSM (SU(3)×SU(2)×U(1))
- Chiral superfields: 16 (3 generations)
- Higgs: 10_H + 126_H + 126_H_bar
- Sync field: W (singlet under SM, couples via dim-5 operator)
- OAS threshold: Δ(1/g²) = dim(G)·ε·C₀/(16π²) with δ_opt = -0.81 effective

參考 SPheno MSSM 的 y_u(GUT) = 3.28×10⁻⁶ (not rS² ~ 10⁻⁸)

## 任務 4：用 SARAH 生成 SPheno 代碼

```mathematica
<<SARAH`
Start["IDM_GUT"];
MakeSPheno[];
```

## 任務 5：編譯 OAS SPheno

```bash
cd /tmp/SPheno-4.0.5/IDM_GUT
make -j$(nproc)
```

## 任務 6：運行 SPheno + CAT 驗證

```bash
cd /tmp/SPheno-4.0.5
./bin/SPheno input/LesHouches.in.IDM_GUT
python3 /home/wsl/IDM-Domain-Framework/scripts/phase7_cat_spheno_monitor.py \
  --spheno-output /tmp/SPheno-4.0.5/SPheno.spc
```

目標：y_u(M_Z) 喺 1.28×10⁻⁵ ± 3% 內

## 已知物理問題

1. **y_u(GUT) 邊界**：OAS dim-6 operator hierarchy (rS²) 壓制太強（9.6×10⁻⁸ vs SPheno MSSM 嘅 3.28×10⁻⁶）
   - 真正來源：126_H EW doublet O(1) Yukawa + 3-cycle eigenvector mixing
   - 需要喺 SARAH model 正確設定 126_H 嘅 Yukawa 結構

2. **非全純閾值修正**：Δy_u/y_u ≈ +0.12% 太少（需要 +15-25%）
   - 需要 SPheno 完整 2-loop RGE 計算
   - Python 嘅 2-loop RK4 solver 已驗證（y_t 0.993× obs）

3. **OAS threshold 格式**：Δ(1/g²) 係 GUT-scale boundary condition，唔係 continuous beta function
   - 正確：apply to gauge couplings at M_GUT, then standard MSSM RGE
   - Coxeter signs: c_U1 = -1, c_SU2 = +1, c_SU3 = +1

## 參考文件

- `/home/wsl/IDM-Domain-Framework/docs/TASK_SPEC_CONTRACT_PHASE7.md` — Phase 7 Task Spec
- `/home/wsl/IDM-Domain-Framework/narrative/phase7.md` — Phase 7 narrative
- `/home/wsl/IDM-Domain-Framework/scripts/phase7_1_rge_solver.py` — verified RK4 solver
- `/tmp/SPheno-4.0.5/SPheno.spc` — SPheno MSSM baseline spectrum
- `~/.hermes/references/model-providers.yaml` — model config
- Memory: CIP-EEG, IDM Extension Projects status at MASTER_OVERVIEW.md

## 唔好做嘅嘢

- ❌ 唔好修改 `/home/wsl/IDM-Domain-Framework/` 以外嘅檔案
- ❌ 唔好改 report/report_5.0.md, report/report_6.0.md, appendix 等唯讀文件
- ❌ 唔好重新下載 SPheno（已喺 /tmp/SPheno-4.0.5/）
- ❌ 唔好重新安裝 Python 3-loop RGE solver（已寫好）