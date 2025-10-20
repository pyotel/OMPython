# Workshop - SMR Power Plant Simulations

이 디렉토리는 OMPython을 사용하여 SMR(Small Modular Reactor) 발전소 모델을 시뮬레이션하고 시각화하는 예제들을 포함합니다.

## 모델 설명

**SMR_PowerPlant** 모델은 소형 모듈형 원자로 발전소의 기본 동작을 시뮬레이션합니다.

### 주요 파라미터

- `Q_fission` (W): 핵분열 열출력 (기본값: 100 MW)
- `eff_thermal`: 열→전기 변환 효율 (기본값: 0.35 = 35%)
- `m_coolant` (kg): 냉각재 질량 (기본값: 500 kg)
- `Cp` (J/kg·K): 냉각재 비열 (기본값: 4200)
- `T_in` (K): 냉각재 입구 온도 (기본값: 300 K)
- `T_steam` (K): 증기 온도 (기본값: 550 K)
- `UA` (W/K): 열교환기 전달계수 (기본값: 50 kW/K)

### 주요 변수

- `T_core` (K): 노심 냉각수 온도
- `Q_transfer` (W): 냉각수 → 증기 열전달량
- `P_electric` (W): 전력 출력

### 모델 방정식

```
dT_core/dt = (Q_fission - Q_transfer) / (m_coolant * Cp)
Q_transfer = UA * (T_core - T_steam)
P_electric = Q_transfer * eff_thermal
```

## 사용 가능한 스크립트

### 1. test_basic.py - 기본 테스트

가장 기본적인 SMR 시뮬레이션 및 결과 검증.

```bash
python test_basic.py
```

**기능:**
- 모델 로드 및 빌드
- 파라미터 확인
- 시뮬레이션 실행
- 기본 결과 분석 (온도, 열전달, 전력 출력, 효율)

**출력:**
- 콘솔에 시뮬레이션 결과 출력

---

### 2. visualize_smr.py - 종합 시각화

SMR 운전의 다양한 측면을 시각화하는 포괄적인 분석.

```bash
python visualize_smr.py
```

**기능:**
- 포괄적인 4패널 플롯 (온도, 열전달, 전력, 효율)
- 에너지 흐름 다이어그램 (Sankey 스타일)
- 과도 응답 분석 (Transient analysis)

**생성되는 그래프:**
- `results/smr_comprehensive.png` - 4패널 종합 분석
- `results/smr_energy_flow.png` - 에너지 흐름도
- `results/smr_transient.png` - 과도 응답 분석

**실행 시간:** 약 15-20초

---

### 3. parameter_study.py - 파라미터 스터디

여러 파라미터의 영향을 체계적으로 분석.

```bash
python parameter_study.py
```

**기능:**
- 3개 주요 파라미터 스윕:
  - `UA`: 열교환기 성능 [30, 50, 70, 90 kW/K]
  - `eff_thermal`: 열효율 [0.25, 0.30, 0.35, 0.40]
  - `m_coolant`: 냉각재 질량 [300, 500, 700, 900 kg]
- 각 파라미터별 상세 분석
- 민감도 분석 (Sensitivity analysis)

**생성되는 그래프:**
- `results/param_study_UA.png`
- `results/param_study_eff_thermal.png`
- `results/param_study_m_coolant.png`
- `results/sensitivity_analysis.png`

**실행 시간:** 약 2-3분 (12회 시뮬레이션)

---

### 4. interactive_dashboard.py - 인터랙티브 대시보드

실시간 파라미터 조정 및 결과 확인.

```bash
python interactive_dashboard.py
```

**기능:**
- 4개 파라미터 실시간 조정 슬라이더
- 온도 및 전력 출력 실시간 업데이트
- 운전 상태 정보 표시

**조정 가능한 파라미터:**
- Fission Power (50~200 MW)
- Thermal Efficiency (0.20~0.45)
- Heat Exchanger UA (20~100 kW/K)
- Coolant Mass (200~1000 kg)

---

## 필수 요구사항

### Python 패키지

```bash
# OMPython 설치
cd ../..
pip install -e .

# 추가 패키지
cd workshop/smr
pip install -r requirements.txt
```

### OpenModelica

OpenModelica Compiler (omc)가 필요합니다.

**설치 확인:**
```bash
omc --version
```

---

## 디렉토리 구조

```
workshop/smr/
├── README.md                    # 이 파일
├── requirements.txt             # Python 패키지 의존성
├── .gitignore                   # Git 제외 파일
│
├── test_basic.py                # 기본 테스트
├── visualize_smr.py             # 종합 시각화
├── parameter_study.py           # 파라미터 스터디
├── interactive_dashboard.py     # 인터랙티브 대시보드
│
└── results/                     # 생성된 그래프들 (자동 생성)
    ├── smr_comprehensive.png
    ├── smr_energy_flow.png
    ├── smr_transient.png
    ├── param_study_*.png
    └── sensitivity_analysis.png
```

---

## 사용 예제

### 기본 사용법

```python
from OMPython import ModelicaSystem

# 모델 로드
mod = ModelicaSystem(
    fileName="../../mo_example/srm.mo",
    modelName="SMR_PowerPlant"
)

# 파라미터 설정
mod.setParameters({
    'Q_fission': '1.5e8',  # 150 MW
    'eff_thermal': '0.38'  # 38% 효율
})

# 시뮬레이션
mod.setSimulationOptions({'stopTime': '1000'})
mod.simulate()

# 결과 추출
time = mod.getSolutions("time")[0]
P_electric = mod.getSolutions("P_electric")[0]
```

### 여러 파라미터 변경

```python
mod.setParameters({
    'Q_fission': '2e8',     # 200 MW
    'eff_thermal': '0.40',  # 40% 효율
    'UA': '7e4',            # 70 kW/K
    'm_coolant': '700'      # 700 kg
})
```

---

## 물리적 의미

### 시스템 동작

1. **핵분열 반응**: `Q_fission` 만큼의 열이 발생
2. **노심 가열**: 냉각재가 노심에서 가열됨
3. **열교환**: 열교환기에서 증기로 열 전달 (`Q_transfer`)
4. **발전**: 증기 터빈으로 전기 생산 (`P_electric`)

### 에너지 흐름

```
Q_fission (100 MW)
    │
    ├─→ Core Loss (작음)
    │
    ├─→ Q_transfer (~100 MW)
    │   │
    │   ├─→ Steam Cycle Loss (~65 MW)
    │   │
    │   └─→ P_electric (~35 MW)
    └─→ Final Efficiency: ~35%
```

### 과도 응답

- 초기: 냉각수 온도가 급격히 상승
- 과도기: 열교환이 증가하며 안정화
- 정상 상태: 모든 값이 일정하게 유지

---

## 시뮬레이션 팁

### 1. 효율 최적화
- `UA` 증가 → 열교환 향상 → 전력 출력 증가
- `eff_thermal` 증가 → 직접적인 전력 출력 증가

### 2. 안정성 개선
- `m_coolant` 증가 → 온도 변화 완화
- 너무 작은 `m_coolant` → 과도한 온도 상승

### 3. 용량 조절
- `Q_fission` 조절로 발전소 출력 제어
- 일반적으로 25~300 MW 범위

---

## 트러블슈팅

### OMC를 찾을 수 없음

```
OMCSessionException: Cannot find OpenModelica executable
```

**해결방법:**
```bash
# Ubuntu/Debian
sudo apt install openmodelica

# 또는 환경변수 설정
export OPENMODELICAHOME=/usr
```

### 시뮬레이션이 수렴하지 않음

**해결방법:**
- `stepSize` 감소 (예: '0.5')
- `tolerance` 완화 (예: '1e-4')

---

## 참고 자료

- [OMPython 문서](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/ompython.html)
- [OpenModelica 사용자 가이드](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/)
- [SMR 기술 개요](https://www.iaea.org/topics/small-modular-reactors)

---

## 라이센스

이 예제 코드들은 OMPython 프로젝트의 라이센스를 따릅니다 (BSD-3-Clause OR OSMC-PL-1.2 OR GPL-3.0).
