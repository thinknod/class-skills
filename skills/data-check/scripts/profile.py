# -*- coding: utf-8 -*-
"""CSV 한 파일을 점검한다. 표준 라이브러리만 쓴다. 고치지 않고 보고만 한다.

  python3 profile.py <파일.csv> [--key 열이름] [--date 열이름]

출력: 행 수, 열마다 빈칸, 완전히 같은 행, 키 중복(같은 키가 몇 번), 날짜 범위와 달마다 행 수,
숫자 열의 최솟값, 최댓값, 음수 개수, 가장 자주 나오는 최댓값(잘림이나 상한 의심)
"""
import csv, sys, argparse
from collections import Counter, defaultdict


def num(v):
    try:
        return float(v.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("--key"); ap.add_argument("--date")
    a = ap.parse_args()
    with open(a.path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head, body = rows[0], rows[1:]
    print(f"# {a.path}\n행 {len(body):,} · 열 {len(head)}: {', '.join(head)}\n")

    print("## 빈칸")
    for j, h in enumerate(head):
        n = sum(1 for r in body if j >= len(r) or r[j].strip() == "")
        if n:
            print(f"- {h}: {n:,}행 ({n / len(body):.2%})")
    print("- (빈칸 없는 열은 적지 않음)\n")

    print("## 중복")
    full = Counter(tuple(r) for r in body)
    dup_full = sum(c - 1 for c in full.values() if c > 1)
    print(f"- 완전히 같은 행: {dup_full:,}행 (남길 행 기준으로 셈)")
    if a.key:
        k = head.index(a.key)
        kc = Counter(r[k] for r in body)
        dup_keys = {key: c for key, c in kc.items() if c > 1}
        extra = sum(c - 1 for c in dup_keys.values())
        print(f"- {a.key} 중복: 키 {len(dup_keys):,}개, 넘치는 행 {extra:,}")
        if dup_keys:
            same = sum(1 for key in dup_keys if len({tuple(r) for r in body if r[k] == key}) == 1)
            print(f"  - 그중 행 전체가 같은 키: {same:,} / 값이 다른 키: {len(dup_keys) - same:,}")
            if a.date:
                d = head.index(a.date)
                months = Counter(r[d][:7] for r in body if kc[r[k]] > 1)
                print(f"  - 중복 행이 있는 달: {dict(sorted(months.items()))}")
    print()

    if a.date:
        d = head.index(a.date)
        ds = sorted(r[d] for r in body if r[d])
        print(f"## 기간\n- {ds[0]} ~ {ds[-1]}")
        m = Counter(x[:7] for x in ds)
        print("- 달마다 행 수: " + ", ".join(f"{k} {v:,}" for k, v in sorted(m.items())))
        days = sorted({x[:10] for x in ds})
        print(f"- 날짜 수: {len(days)}\n")

    print("## 숫자 열")
    for j, h in enumerate(head):
        vals = [num(r[j]) for r in body if j < len(r)]
        vals = [v for v in vals if v is not None]
        if len(vals) < len(body) * 0.9 or not vals:
            continue
        mx = max(vals)
        print(f"- {h}: 최소 {min(vals):,.0f} · 최대 {mx:,.0f} · 음수 {sum(v < 0 for v in vals):,} · 최댓값이 나온 횟수 {vals.count(mx):,}")
    print("\n(최댓값이 여러 번 똑같이 나오면 표시 상한이나 내보내기 잘림일 수 있다. 사람에게 확인)")


if __name__ == "__main__":
    main()
