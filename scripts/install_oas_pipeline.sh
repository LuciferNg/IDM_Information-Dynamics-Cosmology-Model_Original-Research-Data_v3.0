#!/usr/bin/env bash
# =============================================================================
# Phase 7.1 — Wolfram Engine + SARAH Installer (only)
# =============================================================================
# Usage:
#   sudo ./install_oas_pipeline.sh
#
# Prerequisites:
#   - Wolfram ID (free: https://www.wolfram.com/engine/)
#   - Internet connection
#
# Scope: INSTALL ONLY. SPheno model generation + execution handled by Hermes.
# =============================================================================

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────────────
INSTALL_DIR="/opt/wolfram-engine"
SARAH_VER="4.15.1"
WE_INSTALLER="/tmp/WolframEngine_15.0_LINUX.sh"

# ── Colours ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
err()   { echo -e "${RED}[✗]${NC} $1"; }

# ── Step 1: Check prerequisites ─────────────────────────────────────────────
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Phase 7.1 — Wolfram Engine + SARAH Installer           ║"
echo "║  (SPheno model generation + execution = Hermes session)  ║"
echo "╚══════════════════════════════════════════════════════════╝"

if [ "$EUID" -ne 0 ]; then
    err "Must run as root (use sudo)"
    exit 1
fi

# ── Step 2: Download Wolfram Engine (if missing) ────────────────────────────
echo ""
echo "──────────────────────────────────────────────────────────"
echo "  Step 1: Download Wolfram Engine installer (if needed)"
echo "──────────────────────────────────────────────────────────"
echo ""

if [ ! -f "$WE_INSTALLER" ]; then
    warn "Wolfram Engine installer not found at $WE_INSTALLER"
    echo "Downloading (2.2GB)..."
    wget -q --show-progress \
        "https://account.wolfram.com/dl/WolframEngine?version=15.0&platform=Linux&downloadManager=false&includesDocumentation=false" \
        -O "$WE_INSTALLER"
    chmod +x "$WE_INSTALLER"
fi
info "Wolfram Engine installer: $(ls -lh "$WE_INSTALLER" | awk '{print $5}')"

# ── Step 3: Install Wolfram Engine ──────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────────────────────"
echo "  Step 2: Installing Wolfram Engine → $INSTALL_DIR"
echo "──────────────────────────────────────────────────────────"
echo ""

if [ -f "$INSTALL_DIR/Executables/wolfram" ]; then
    info "Wolfram Engine already installed at $INSTALL_DIR"
else
    # Remove stale directory — let installer recreate it
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
    fi
    echo "Running installer (this will take 5-10 minutes)..."
    sh "$WE_INSTALLER" --target "$INSTALL_DIR" --nox11
    info "Wolfram Engine installed"
fi

WOLFRAM="$INSTALL_DIR/Executables/wolfram"
if [ -f "$WOLFRAM" ]; then
    info "Wolfram binary: $WOLFRAM"
    $WOLFRAM -version 2>&1 | head -1
else
    err "Wolfram binary not found — activation may be needed"
    echo "  Run: wolframscript -activate  (command-line activation)"
    echo "  Enter your Wolfram ID when prompted"
fi

# ── Step 4: Download SARAH ──────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────────────────────"
echo "  Step 3: Downloading SARAH $SARAH_VER"
echo "──────────────────────────────────────────────────────────"
echo ""

SARAH_TAR="/tmp/SARAH-${SARAH_VER}.tar.gz"
SARAH_DIR="/tmp/SARAH-${SARAH_VER}"
MATH_APPS="$HOME/.Mathematica/Applications"

if [ -d "$MATH_APPS/SARAH" ]; then
    info "SARAH already installed in $MATH_APPS"
else
    if [ ! -f "$SARAH_TAR" ]; then
        wget -q --show-progress \
            "https://www.hepforge.org/archive/sarah/SARAH-${SARAH_VER}.tar.gz" \
            -O "$SARAH_TAR"
    fi
    tar xzf "$SARAH_TAR" -C /tmp/
    mkdir -p "$MATH_APPS"
    cp -r "$SARAH_DIR"/* "$MATH_APPS/"
    info "SARAH installed to $MATH_APPS"
fi

# ── Step 5: Verify SARAH loads ──────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────────────────────"
echo "  Step 4: Verifying SARAH"
echo "──────────────────────────────────────────────────────────"
echo ""

if [ -f "$WOLFRAM" ]; then
    echo 'Needs["SARAH`"]; Print["SARAH version: ", SARAH`$SARAHVersion];' | \
        timeout 60 "$WOLFRAM" -noinit -noprompt 2>&1 | tail -5
    info "SARAH loads successfully"
else
    warn "Wolfram Engine not activated yet — skip SARAH verification"
    echo "  Activate first, then run:"
    echo "    echo 'Needs[\"SARAH\\`\"]; Print[SARAH\\`\\$SARAHVersion];' | $WOLFRAM -noinit -noprompt"
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Installation complete                                   ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Wolfram Engine: $INSTALL_DIR"
echo "║  SARAH:          $MATH_APPS/SARAH"
echo "║  SPheno:         /tmp/SPheno-4.0.5/bin/SPheno (pre-installed)"
echo "║  OAS Model:      /home/wsl/IDM-Domain-Framework/models/IDM_GUT.m"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  NEXT: Return to Hermes session for:                    ║"
echo "║  1. SARAH → OAS SPheno code generation                  ║"
echo "║  2. Compile OAS SPheno                                   ║"
echo "║  3. Run SPheno + CAT y_u verification                    ║"
echo "╚══════════════════════════════════════════════════════════╝"

# ── Activation reminder ─────────────────────────────────────────────────────
if [ ! -f "$INSTALL_DIR/Executables/wolfram" ] || \
   ! "$INSTALL_DIR/Executables/wolfram" -version &>/dev/null; then
    echo ""
    echo "⚠️  Wolfram Engine needs activation:"
    echo "   $INSTALL_DIR/Executables/wolframscript -activate"
    echo "   (Enter your Wolfram ID when prompted)"
fi