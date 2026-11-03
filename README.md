# class-skills

데이터 분석과 판단 강의에서 쓰는 Claude Code / Codex 스킬 11개. 질문을 세우고, 데이터를 점검하고, 비교하고, 판단을 돕는 한 장을 만들 때까지의 순서와 기준을 적어 두었다.

실습 데이터는 가상의 생활용품 가게 하루상점이다. 실제 고객 데이터는 넣지 않는다.

## 쓰는 법: 링크를 AI에게 준다

Claude Code나 Codex에게 이 저장소 링크를 주고 맡긴다.

```
https://github.com/thinknod/class-skills 의 data-check 스킬을 읽어 보고, 이 실습 폴더의 .claude/skills/에 설치해 줘.
```

설치한 뒤에는 이름으로 부른다.

```
data-check 스킬로 주문_정리본.csv를 점검해 줘.
```

직접 넣으려면 폴더째 복사한다.

```bash
git clone https://github.com/thinknod/class-skills.git
# Claude Code
mkdir -p .claude/skills && cp -R class-skills/skills/data-check .claude/skills/
# Codex
mkdir -p .agents/skills && cp -R class-skills/skills/data-check .agents/skills/
```

Claude 앱(웹, 데스크톱)은 스킬 폴더 하나를 zip으로 묶어 맞춤 › 스킬 › 업로드로 올린다. zip을 열면 스킬 폴더가 바로 나와야 한다.

넣기 전에 SKILL.md와 scripts/를 읽어 본다. 무엇을 실행하는지 알고 쓴다.

## 스킬

### 분석: 사실 만들기

| 스킬 | 하는 일 |
|---|---|
| [data-check](skills/data-check) | 계산 전에 구조, 결측, 중복, 기간 경계, 지표 정의를 점검하고, 처리 방법은 사람에게 묻는다 |
| [describe-compare](skills/describe-compare) | 얼마나, 어떻게 변했나, 어디서 빠지나, 누가 다른가. 비율은 합계로, 유의성은 '우연인가'까지만 |
| [chart-request](skills/chart-request) | 비교 한 문장을 차트 하나로. 제목은 결론 문장, 실패 유형 여덟 가지를 스스로 점검 |
| [compare-baseline](skills/compare-baseline) | 비교 기준을 먼저 밝히고, 평균만이 아니라 분포와 집단을 본다 |
| [analysis-report](skills/analysis-report) | 질문, 정의, 발견, 근거, 한계를 한 장으로. 원인 판단과 제안은 쓰지 않는다 |

### 판단: 결정에서 확인까지

| 스킬 | 하는 일 |
|---|---|
| [decision-frame](skills/decision-frame) | 누가, 언제까지, 무엇 중에서 결정하나를 한 줄로. 빈 칸은 묻는다 |
| [question-design](skills/question-design) | 분석 질문 10개로 넓히고 세 조건으로 둘만 남긴다 |
| [rival-explanations](skills/rival-explanations) | 설명을 셋 이상 세우고, 맞다면 보여야 할 것을 먼저 쓴 뒤 확인한다 |
| [insight-report](skills/insight-report) | 결정, What, So what, Now what, 가정과 한계를 한 장으로 |
| [effect-check](skills/effect-check) | 전후 비교만 하지 않고 비교집단부터 찾아 효과를 확인한다 |

### 화면

| 스킬 | 하는 일 |
|---|---|
| [one-page-dashboard](skills/one-page-dashboard) | 결정 한 줄, KPI, 추세, 비교를 한 장 HTML로. 화면 숫자를 계산과 대조한다 |

내기 전 설득력 점검은 따로 있다: [persuasion-check](https://github.com/thinknod/persuasion-check)

강의에서 함께 쓰는 공개 스킬(Anthropic data 플러그인 등)의 링크는 [class.thinknod.ai/skills](https://class.thinknod.ai/skills)에 모아 두었다.

## 라이선스

MIT
