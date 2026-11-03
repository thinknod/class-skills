# -*- coding: utf-8 -*-
"""비교에 자주 쓰는 계산 두 가지. 표준 라이브러리만 쓴다.

  python3 stats.py prop <성공1> <전체1> <성공2> <전체2>
      두 비율, 차이(%p와 %), 두 비율 z검정 p값(양측), 차이의 95% 범위
  python3 stats.py dist <파일.csv> <열> [--dedup 키열] [--month YYYY-MM] [--date 일자열] [--bins 경계,경계,...]
      평균, 중앙값, 구간별 비중 (원 단위 경계, 하한 포함)
"""
import csv, sys, math, argparse, statistics


def prop(a):
    s1, n1, s2, n2 = map(float, a)
    p1, p2 = s1 / n1, s2 / n2
    p = (s1 + s2) / (n1 + n2)
    se0 = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se0 if se0 else float("inf")
    pv = math.erfc(abs(z) / math.sqrt(2))
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    lo, hi = (p1 - p2) - 1.96 * se, (p1 - p2) + 1.96 * se
    print(f"비율 1: {p1:.1%} ({s1:,.0f}/{n1:,.0f})  비율 2: {p2:.1%} ({s2:,.0f}/{n2:,.0f})")
    print(f"차이: {(p1 - p2) * 100:+.1f}%p  (비율 2 대비 {(p1 / p2 - 1) * 100 if p2 else float('nan'):+.1f}%)")
    print(f"z = {z:.2f}, p = {pv:.2g}" + ("  (p < 0.001)" if pv < 0.001 else ""))
    print(f"차이의 95% 범위: {lo * 100:+.1f}%p ~ {hi * 100:+.1f}%p")
    print("읽는 법: p가 작으면 '이 차이는 우연으로 보기 어렵다'까지. 원인이라는 뜻은 아니다")


def dist(a):
    ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("col")
    ap.add_argument("--dedup"); ap.add_argument("--month"); ap.add_argument("--date", default="일자"); ap.add_argument("--bins")
    o = ap.parse_args(a)
    with open(o.path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if o.dedup:
        seen, keep = set(), []
        for r in rows:
            if r[o.dedup] not in seen:
                seen.add(r[o.dedup]); keep.append(r)
        print(f"{o.dedup} 중복 제거: {len(rows) - len(keep):,}행 뺌"); rows = keep
    if o.month:
        rows = [r for r in rows if r[o.date].startswith(o.month)]
    v = [float(r[o.col]) for r in rows if r[o.col] != ""]
    print(f"n = {len(v):,}  평균 {statistics.mean(v):,.0f}  중앙값 {statistics.median(v):,.0f}  합계 {sum(v):,.0f}")
    if o.bins:
        b = [float(x) for x in o.bins.split(",")]
        edges = [float("-inf")] + b + [float("inf")]
        for lo, hi in zip(edges, edges[1:]):
            n = sum(1 for x in v if lo <= x < hi)
            name = (f"~{hi / 1e4:g}만" if lo == float("-inf") else f"{lo / 1e4:g}만~" if hi == float("inf") else f"{lo / 1e4:g}~{hi / 1e4:g}만")
            print(f"  {name}: {n / len(v):.0%} ({n:,})")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("prop", "dist"):
        print(__doc__); sys.exit(1)
    (prop if sys.argv[1] == "prop" else dist)(sys.argv[2:])
