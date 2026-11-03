# -*- coding: utf-8 -*-
"""대시보드 화면의 숫자를 계산 결과(json)와 대조한다. 표준 라이브러리만 쓴다.

  python3 verify_dashboard.py <대시보드.html> <대시보드_숫자.json>

- 화면에만 있는 숫자: html에 보이는 글자 속 숫자 중 json 어디에도 없는 것 (반올림 자리를 맞춰 비교)
- 빠진 KPI: json의 kpis[].value 중 화면에 없는 것
json 모양: {"kpis": [{"name": "...", "value": 73.8, ...}], ...} 나머지 키는 자유. 숫자는 어디에 있든 모두 근거로 본다
날짜(2026-10-01, 10/1), 연도, 오류 코드 같은 이름(E-AUTH-408), 12 이하 정수(% 없이)는 대조에서 뺀다. 차이(%p)처럼 json 두 값의 차이로 만든 숫자는 json에 그 값을 같이 넣는다
"""
import json, re, sys
from html.parser import HTMLParser


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out, self.skip = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("style", "script"): self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)


def leaves(o):
    if isinstance(o, bool): return
    if isinstance(o, (int, float)): yield float(o)
    elif isinstance(o, dict):
        for v in o.values(): yield from leaves(v)
    elif isinstance(o, list):
        for v in o: yield from leaves(v)


CODE = re.compile(r"[A-Za-z]+(?:-[A-Za-z0-9]+)+")   # 오류 코드(E-AUTH-408) 같은 이름
DATE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}|\d{4}년|\d{1,2}월|\d{1,2}일|\d{1,2}주")
NUM = re.compile(r"[-+−]?\d[\d,]*(?:\.\d+)?\s*(%p|%|배|건|명|원|만 원|백만 원)?")


def shown(text):
    text = DATE.sub(" ", CODE.sub(" ", text))
    for m in NUM.finditer(text):
        raw = m.group(0).replace("−", "-").replace("+", "")
        unit = m.group(1) or ""
        s = re.sub(r"[^\d.\-]", "", raw.replace(unit, ""))
        if not s or s in ("-", "."): continue
        v = float(s); dec = len(s.split(".")[1]) if "." in s else 0
        if unit == "" and dec == 0 and abs(v) <= 12: continue
        yield m.group(0).strip(), v, dec, unit


def match(v, dec, pool):
    for p in pool:
        for q in (p, p * 100, abs(p), abs(p) * 100):
            if round(q, dec) == round(abs(v), dec): return True
    return False


def main():
    html, js = sys.argv[1], sys.argv[2]
    t = Text(); t.feed(open(html, encoding="utf-8").read()); text = " ".join(t.out)
    data = json.load(open(js, encoding="utf-8")); pool = list(leaves(data))
    only = [(raw) for raw, v, dec, u in shown(text) if not match(v, dec, pool)]
    shown_vals = [(v, dec) for _, v, dec, _ in shown(text)]
    missing = []
    for k in data.get("kpis", []):
        val = k.get("value")
        if isinstance(val, (int, float)) and not any(round(val, d) == round(v, d) or round(val * 100, d) == round(v, d) for v, d in shown_vals):
            missing.append(f"{k.get('name')}: {val}")
    print(f"화면 숫자 {len(shown_vals)}개 · json 숫자 {len(pool)}개")
    print(f"화면에만 있는 숫자: {len(only)}개" + ("" if not only else " → " + ", ".join(sorted(set(only)))))
    print(f"화면에 없는 KPI: {len(missing)}개" + ("" if not missing else " → " + ", ".join(missing)))
    sys.exit(1 if only or missing else 0)


if __name__ == "__main__":
    main()
