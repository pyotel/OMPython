# Workshop - Newton Cooling Model Simulations

이 디렉토리는 OMPython을 사용하여 Modelica 모델을 로드, 시뮬레이션, 시각화하는 예제들을 포함합니다.

## 모델 설명

**NewtonCoolingDynamic** 모델은 뉴턴의 냉각 법칙을 구현한 열전달 시뮬레이션입니다.

### 주요 파라미터

- `T0` (K): 초기 온도 (기본값: 363.15)
- `h` (W/m²·K): 대류 냉각 계수 (기본값: 0.7)
- `A` (m²): 표면적 (기본값: 1.0)
- `m` (kg): 물체의 질량 (기본값: 0.1)
- `c_p` (J/K·kg): 비열 (기본값: 1.2)

### 모델 방정식

```
m * c_p * dT/dt = h * A * (T_inf - T)
```

## 사용 가능한 스크립트

### 1. simple_example.py - 기본 예제

가장 간단한 시뮬레이션 예제입니다. 모델을 로드하고, 파라미터를 설정하고, 시뮬레이션을 실행한 후 결과를 플롯합니다.

```bash
python workshop/simple_example.py
```

**기능:**
- 모델 로드 및 빌드
- 파라미터 확인 및 수정
- 시뮬레이션 실행
- 기본 그래프 생성

**출력:**
- `results/simple_example.png` - 온도 변화 그래프

---

### 2. simulate_cooling.py - 파라미터 스터디

여러 파라미터 값으로 시뮬레이션을 반복하여 각 파라미터의 영향을 분석합니다.

```bash
python workshop/simulate_cooling.py
```

**기능:**
- 다중 파라미터 값으로 자동 시뮬레이션
- 각 파라미터별 비교 그래프 생성
- 최종 온도 비교 차트

**파라미터 변화:**
- `h`: [0.5, 0.7, 1.0, 1.5] - 냉각 계수
- `m`: [0.05, 0.1, 0.2, 0.3] - 질량
- `A`: [0.5, 1.0, 1.5, 2.0] - 표면적

**출력:**
- `results/cooling_h.png` - h 변화에 따른 결과
- `results/cooling_m.png` - m 변화에 따른 결과
- `results/cooling_A.png` - A 변화에 따른 결과
- `results/cooling_comparison.png` - 전체 비교 차트

---

### 3. interactive_explorer.py - 인터랙티브 탐색기

실시간으로 파라미터를 조정하면서 시뮬레이션 결과를 확인할 수 있는 인터랙티브 도구입니다.

```bash
python workshop/interactive_explorer.py
```

**기능:**
- 슬라이더를 통한 실시간 파라미터 조정
- 파라미터 변경 시 자동 재시뮬레이션
- 결과 즉시 업데이트

**조정 가능한 파라미터:**
- Convection Coefficient (h): 0.1 ~ 2.0
- Mass (m): 0.01 ~ 0.5
- Surface Area (A): 0.1 ~ 3.0
- Initial Temperature (T0): 300 ~ 400 K

---

## 필수 요구사항

### Python 패키지

```bash
# OMPython 설치 (현재 디렉토리에서)
pip install -e ..

# 추가 패키지
pip install matplotlib numpy
```

### OpenModelica

OpenModelica Compiler (omc)가 시스템에 설치되어 있어야 합니다.

**설치 확인:**
```bash
omc --version
```

**설치 방법:**
- Ubuntu/Debian: https://openmodelica.org/download/download-linux
- Windows: https://openmodelica.org/download/download-windows
- macOS: https://openmodelica.org/download/download-mac

---

## 디렉토리 구조

```
workshop/
├── README.md                    # 이 파일
├── simple_example.py           # 기본 예제
├── simulate_cooling.py         # 파라미터 스터디
├── interactive_explorer.py     # 인터랙티브 탐색기
└── results/                    # 생성된 그래프들 (자동 생성)
    ├── simple_example.png
    ├── cooling_h.png
    ├── cooling_m.png
    ├── cooling_A.png
    └── cooling_comparison.png
```

---

## 사용 예제

### 기본 사용법

```python
from OMPython import ModelicaSystem

# 모델 로드
mod = ModelicaSystem(
    fileName="../mo_example/bouncingball.mo",
    modelName="NewtonCoolingDynamic"
)

# 파라미터 설정
mod.setParameters({'h': '1.0', 'm': '0.2'})

# 시뮬레이션 옵션
mod.setSimulationOptions({'stopTime': '2.0'})

# 시뮬레이션 실행
mod.simulate()

# 결과 추출
time = mod.getSolutions("time")[0]
temperature = mod.getSolutions("T")[0]
```

### 여러 파라미터 변경

```python
# 파라미터 딕셔너리로 여러 값 한번에 설정
mod.setParameters({
    'h': '1.5',
    'm': '0.15',
    'A': '1.2',
    'T0': '373.15'
})
```

### 사용 가능한 변수 확인

```python
# 모든 변수 확인
all_vars = mod.getSolutions()
print(all_vars)  # 변수 이름 튜플 출력

# 파라미터 확인
params = mod.getParameters()
for name, value in params.items():
    print(f"{name}: {value}")
```

---

## 트러블슈팅

### OMC를 찾을 수 없다는 오류

```
OMCSessionException: Cannot find OpenModelica executable
```

**해결방법:**
1. OpenModelica가 설치되어 있는지 확인
2. 환경변수 설정:
   ```bash
   export OPENMODELICAHOME=/usr
   ```

### 빌드 오류

```
ModelicaSystemError: XML file not generated
```

**해결방법:**
1. 모델 파일 경로 확인
2. 모델 이름이 정확한지 확인
3. OMC 로그 확인 (temp 디렉토리)

### 그래프가 표시되지 않음

**해결방법:**
- GUI 백엔드 설정:
  ```python
  import matplotlib
  matplotlib.use('TkAgg')  # or 'Qt5Agg'
  ```

---

## 추가 학습 자료

- [OMPython 문서](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/ompython.html)
- [OpenModelica 사용자 가이드](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/)
- [Modelica 언어 튜토리얼](https://mbe.modelica.university/)

---

## 라이센스

이 예제 코드들은 OMPython 프로젝트의 라이센스를 따릅니다 (BSD-3-Clause OR OSMC-PL-1.2 OR GPL-3.0).
