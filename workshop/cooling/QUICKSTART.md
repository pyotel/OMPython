# 빠른 시작 가이드

## 설치

### 1단계: 필수 요구사항 확인

OpenModelica가 설치되어 있는지 확인:

```bash
omc --version
```

설치되어 있지 않다면:
- Ubuntu/Debian: `sudo apt-get install openmodelica`
- 또는 https://openmodelica.org/download 에서 다운로드

### 2단계: Python 패키지 설치

자동 설치 스크립트 사용:

```bash
cd workshop/ball
./setup.sh
```

또는 수동 설치:

```bash
# OMPython 설치 (프로젝트 루트에서)
cd ../..
pip install -e .

# 추가 패키지 설치
cd workshop/ball
pip install -r requirements.txt
```

## 예제 실행

### 1. 기본 테스트 (GUI 없음)

```bash
python test_basic.py
```

이 스크립트는:
- 모델을 로드하고 빌드
- 파라미터를 설정하고 시뮬레이션 실행
- 결과를 콘솔에 출력

예상 출력:
```
======================================================================
Testing Newton Cooling Model Simulation
======================================================================

Model file: /path/to/mo_example/cooling.mo
Model exists: True
Model name: NewtonCoolingDynamic

[1/5] Loading model...
  ✓ Model loaded successfully
...
✓ ALL TESTS PASSED!
```

### 2. 간단한 시각화 예제

```bash
python simple_example.py
```

이 스크립트는:
- 모델을 시뮬레이션하고
- 온도 변화 그래프를 생성
- `results/simple_example.png` 파일에 저장

### 3. 파라미터 스터디

```bash
python simulate_cooling.py
```

이 스크립트는:
- 여러 파라미터 값으로 자동 시뮬레이션
- 각 파라미터의 영향을 분석
- 여러 비교 그래프 생성

실행 시간: 약 1-2분 (시뮬레이션 12회)

생성되는 그래프:
- `results/cooling_h.png` - 대류 계수 영향
- `results/cooling_m.png` - 질량 영향
- `results/cooling_A.png` - 표면적 영향
- `results/cooling_comparison.png` - 전체 비교

### 4. 인터랙티브 탐색기

```bash
python interactive_explorer.py
```

이 스크립트는:
- 대화형 창을 열고
- 슬라이더로 파라미터 조정
- 실시간으로 결과 업데이트

**사용법:**
1. 창이 열리면 하단의 슬라이더를 조정
2. 각 슬라이더 변경 시 자동으로 재시뮬레이션
3. 그래프가 실시간으로 업데이트됨

## 문제 해결

### OMC를 찾을 수 없음

```
OMCSessionException: Cannot find OpenModelica executable
```

**해결:**
```bash
export OPENMODELICAHOME=/usr
# 또는 OpenModelica가 설치된 경로
```

### zmq 모듈 없음

```
ModuleNotFoundError: No module named 'zmq'
```

**해결:**
```bash
pip install pyzmq
```

### matplotlib 백엔드 오류

```
ImportError: cannot import name '_backend_tk' from 'matplotlib.backends'
```

**해결:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# 또는 다른 백엔드 사용
export MPLBACKEND=Agg  # 파일만 저장, 화면 표시 안함
```

### 시뮬레이션이 느림

Docker를 사용하는 경우 로컬 OMC가 더 빠를 수 있습니다.

```python
# Docker 대신 로컬 OMC 사용 (기본값)
mod = ModelicaSystem(fileName=..., modelName=...)
```

## 다음 단계

1. `README.md`를 읽고 각 스크립트의 상세 설명 확인
2. 예제 코드를 수정하여 자신만의 시뮬레이션 만들기
3. 다른 Modelica 모델 파일(.mo) 시도
4. [OMPython 문서](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/ompython.html) 참조

## 추가 예제

### 커스텀 파라미터로 시뮬레이션

```python
from OMPython import ModelicaSystem

mod = ModelicaSystem(
    fileName="../../mo_example/cooling.mo",
    modelName="NewtonCoolingDynamic"
)

# 파라미터 변경
mod.setParameters({
    'h': '2.0',      # 더 빠른 냉각
    'm': '0.05',     # 더 가벼운 물체
    'A': '2.0',      # 더 큰 표면적
    'T0': '400'      # 더 높은 초기 온도
})

# 더 긴 시뮬레이션
mod.setSimulationOptions({'stopTime': '5.0'})

mod.simulate()

# 결과 확인
time = mod.getSolutions("time")[0]
temp = mod.getSolutions("T")[0]
print(f"Final temperature: {temp[-1]:.2f} K")
```

### 특정 시간에서의 값

```python
import numpy as np

time = mod.getSolutions("time")[0]
temp = mod.getSolutions("T")[0]

# 0.5초일 때의 온도
idx = np.argmin(np.abs(time - 0.5))
print(f"Temperature at 0.5s: {temp[idx]:.2f} K")
```

## 도움말

문제가 발생하면:
1. `test_basic.py`를 먼저 실행하여 기본 설정 확인
2. OMC 로그 파일 확인 (보통 /tmp에 위치)
3. GitHub Issues: https://github.com/OpenModelica/OMPython/issues
