# 카메라 테스트 도구

# 1. 목적(Goal Statement)

- **궁극적 목표**: 주어진 사용 시나리오(조명·속도·지연·비용 등)에 적합한
• 카메라 **센서 모델**(현재 후보: AR0114, AR0234, OV9782)
• **이미지 파이프라인 파라미터**(fps, 노출, 게인, ISP 옵션 …)
을 자동 추천하고, 실제 캡처·지표평가를 거쳐 “합격/조정”을 명확히 알려 주는 도구를 만든다.

# 2. 범위 & 비범위

| 포함(Scope) | 제외(Out) |
| --- | --- |
| • 센서 스펙 DB 구축 & 질의 <br>• 시나리오→센서·파라미터 매핑 로직 <br>• 캡처·지표·리포트 자동화 CLI <br>• 합격선(Threshold) 설정 & FAIL 알람 | × 딥러닝 모델 훈련/배포 <br>× 로봇 제어 및 실주행 코드 <br>× GUI (1차 버전은 CLI·Markdown 리포트) |

# 3. 대표 사용 시나리오(Use-Case Table)

| ID | 파라미터(예) | 성공 기준 |
| --- | --- | --- |
| UC-MOVE-1 | 실내 60 Hz LED, 로봇 1.2 m/s, 30 fps 플래닝 | • 노출 ≤ 3 ms, 모션블러 ≤ 2 px <br>• 프레임-간 ΔL ≤ 3 % |
| UC-MAP-1 | 저속 매핑(정지 또는 0.1 m/s), 해상도 우선 | • 해상도 ≥ 1.5 Mpx <br>• SNR ≥ 30 dB |
| UC-LOW-LIGHT | 70 lux, 야간 점검, LED 라이트 없음 | • mAP 감소 ≤ 10 % vs 300 lux |

# 4. 기능 요구(Functional Requirements)

| FR-ID | 설명 |
| --- | --- |
| FR-01 | YAML 시나리오 파일을 입력 받아 요구 조건 파싱 |
| FR-02 | 센서 DB에서 조건 매칭 → 우선순위 랭킹 (가중치 방식) |
| FR-03 | 선택 센서에 대해 파라미터 프로파일(노출·FPS·게인·ISP) 생성 |
| FR-04 | SDK 제어로 이미지를 캡처하고 데이터셋 저장 |
| FR-05 | 모션블러, 플리커, SNR, mAP 등 지표 계산 & 합격 판정 |
| FR-06 | Markdown + PDF 리포트 자동 생성, CI 결과 코멘트 첨부 |

# 5. 비기능 요구(Non-Functional)

- **토큰 효율**: 전체 설계 ≤ 6 K tokens — LLM 프롬프트 1-패스 가능
- **확장성**: 센서·지표·시나리오 항목을 YAML 스키마 수정만으로 추가
- **재현성**: `scenario.yaml + seed` 만 있으면 동일 결과 재생산
- **호환성**: Python 3.10+, Linux(Ubuntu 20.04 이상), Docker optional

# 6. 시스템 개요(아키텍처 스케치)

graph TD
A[scenario.yml] --> B(Scenario Parser)
B --> C{Sensor Selector}
C -->|ranked list| D[Parameter Generator]
D -->|cfg.json| E[Capture Runner]
E -->|imgs| F[Metric Analyzer]
F -->|csv| G[Report Builder]

# 7. 데이터 모델

## 7.1 Sensor DB (CSV → JSON or SQLite)

| id | model | res_x | res_y | max_fps | anti_band | dr_dB | iface | est_cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7.2 Scenario YAML 스키마

```yaml
scenario_id: UC-MOVE-1
env:
  light_freq: 60      # Hz
  illuminance: 300    # lux
robot:
  speed_mps: 1.2
pipeline:
  max_latency_ms: 50
priority: ["motion_blur", "latency", "cost"]
```

# 8. 주요 모듈 & API

| Module | 파일 | 핵심 함수 | I/O |
| --- | --- | --- | --- |
| scenario | [scenario.py](http://scenario.py/) | `load(path) → dict` | YAML |
| selector | [select.py](http://select.py/) | `rank(scen, db) → list[SensorScore]` | dict |
| paramgen | [param.py](http://param.py/) | `generate(sensor, scen) → cfg` | JSON |
| capture | [capture.py](http://capture.py/) | `run(cfg) → dataset_id` | imgs |
| metric | [metric.py](http://metric.py/) | `evaluate(ds, scen) → csv` | csv |
| report | [report.py](http://report.py/) | `make(ds, csv, scen) → md/pdf` | md/pdf |

# 9. 지표 & 합격선(초안)

| Metric | 도구 | Pass |
| --- | --- | --- |
| motion_blur_px | cv2 + edge MTF | ≤ 2 |
| frame_delta_L% | NumPy | ≤ 3 % |
| SNR_dB | skimage | ≥ 20 |
| mAP_rel | PyTorch eval | ≥ 90 % baseline |

# 10. CLI 예시

```bash
tool test ./scenarios/uc_move_1.yml --auto
# → outputs ./runs/uc_move_1/report.pdf (PASS)

```

# 11. 로드맵(Phase Milestones)

| 단계 | 목표 | 산출물 |
| --- | --- | --- |
| P-1 | Sensor DB v0, Scenario parser, Selector MVP | CSV, rank-CLI |
| P-2 | Capture Runner + Metric Analyzer | dataset, csv |
| P-3 | Report Builder, CI workflow 템플릿 | md/pdf, GitHub Actions |
| P-4 | GUI or API server (optional) | Web dashboard |
