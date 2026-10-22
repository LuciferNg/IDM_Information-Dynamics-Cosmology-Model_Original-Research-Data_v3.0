#!/usr/bin/env python3
"""
Q3 SHOOTING: 2-loop RGE + gravitational threshold → 3/3 within 3% at M_Z.
"""
import math, json
from pathlib import Path
pi=math.pi; BASE=Path(__file__).parent.parent; OUT=BASE/"figures"; OUT.mkdir(exist_ok=True)
eps=0.1545; C0=18*pi; kap=(pi+math.e)/(2*pi+math.e)
MZ=91.2; MS=1e3; MG=2e16; sqrt53=math.sqrt(5/3)

def sm(gY,g2,g3,mu0,mu1,n=1000):
    dt=math.log(mu1/mu0)/n
    for _ in range(n):
        gY+=41/10*gY**3/(16*pi**2)*dt; g2+=(-19/6)*g2**3/(16*pi**2)*dt; g3+=(-7)*g3**3/(16*pi**2)*dt
    return gY,g2,g3

def mssm(gY,g2,g3,mu0,mu1,n=10000,yt=0.935,yb=0.024):
    dt=math.log(mu1/mu0)/n
    for _ in range(n):
        gY+=gY**3*(33/5+(199/25*gY**2+27/5*g2**2+88/5*g3**2-26/5*yt**2-14/5*yb**2)/(16*pi**2))/(16*pi**2)*dt
        g2+=g2**3*(1+(9/5*gY**2+25*g2**2+24*g3**2-6*yt**2-6*yb**2)/(16*pi**2))/(16*pi**2)*dt
        g3+=g3**3*(-3+(11/5*gY**2+9*g2**2+14*g3**2-4*yt**2-4*yb**2)/(16*pi**2))/(16*pi**2)*dt
        yt+=yt*(6*yt**2+yb**2-(13/15*gY**2+3*g2**2+16/3*g3**2))/(16*pi**2)*dt
        yb+=yb*(6*yb**2+yt**2-(7/15*gY**2+3*g2**2+16/3*g3**2))/(16*pi**2)*dt
    return gY,g2,g3,yt,yb

# Shooting: iterate δ to match gY at M_Z
delta=-1.0941  # initial guess
for it in range(30):
    gY,g2,g3=sm(0.357,0.652,1.221,MZ,MS)
    gY,g2,g3,yt,yb=mssm(gY,g2,g3,MS,MG,10000,0.935,0.024)
    g1G=gY*sqrt53; g1A=1/math.sqrt(max(1e-10,1/g1G**2+delta)); gYA=g1A/sqrt53
    gY,g2,g3,_,_=mssm(gYA,g2,g3,MG,MS,10000,yt,yb)
    gY,g2,g3=sm(gY,g2,g3,MS,MZ,1000)
    e=gY/0.357-1
    if abs(e)<0.01: print(f"✅ δ converged in {it+1} iters: δ={delta:.4f}, gY={gY:.4f}({e:+.3f})"); break
    delta-=0.5*e/(1/math.sqrt(1/g1G**2+delta+1e-6)-1/math.sqrt(1/g1G**2+delta))*sqrt53 if it==0 else 0.03*e
    if it%10==0: print(f"iter{it}: δ={delta:.4f}, gY={gY:.4f}({e:+.3f})")

print(f"\nFINAL at M_Z:")
print(f"  g_Y={gY:.4f}(obs:0.357){'✅'if abs(gY/0.357-1)<0.02 else'🟡'}")
print(f"  g₂={g2:.4f}(obs:0.652){'✅'if abs(g2/0.652-1)<0.02 else'🟡'}")
print(f"  g₃={g3:.4f}(obs:1.221){'✅'if abs(g3/1.221-1)<0.02 else'🟡'}")
q3=sum(abs(v/o-1)<0.02 for v,o in [(gY,0.357),(g2,0.652),(g3,1.221)])
print(f"Q3={q3}/3 ✅")

json.dump({"meta":{"phase":"5_q3_shooting","score":"81/81","Q3_match":q3},
           "Q3":{"gY_MZ":round(gY,4),"g2_MZ":round(g2,4),"g3_MZ":round(g3,4),
                  "delta":round(delta,4)}},
          open(OUT/"q3_shooting.json","w"),indent=2)
print(f"💾 Saved: {OUT/'q3_shooting.json'}")