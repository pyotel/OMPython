# Workshop Ball 디렉토리 인덱스

## 📁 파일 구조

```
workshop/ball/
├── README.md                    # 상세한 문서 및 사용법
├── QUICKSTART.md               # 빠른 시작 가이드 (한글)
├── INDEX.md                    # 이 파일
├── requirements.txt            # Python 패키지 의존성
├── setup.sh                    # 자동 설치 스크립트
├── .gitignore                  # Git 무시 파일 목록
│
├── test_basic.py              # 기본 테스트 (GUI 없음)
├── simple_example.py          # 간단한 예제 + 그래프
├── simulate_cooling.py        # 파라미터 스터디
├── interactive_explorer.py    # 인터랙티브 탐색기
│
└── results/                   # 생성된 결과 파일 (자동 생성)
    ├── simple_example.png
    ├── cooling_h.png
    ├── cooling_m.png
    ├── cooling_A.png
    └── cooling_comparison.png
```

## 🚀 빠른 시작

```bash
# 1. 설치
./setup.sh

# 2. 테스트
python test_basic.py

# 3. 예제 실행
python simple_example.py
```

## 📚 문서

- **QUICKSTART.md** - 빠른 시작 가이드 (초보자용, 한글)
- **README.md** - 전체 문서 (상세 설명, 한글)

## 🔧 스크립트 설명

| 스크립트 | 난이도 | 실행 시간 | 그래프 | 설명 |
|---------|--------|----------|--------|------|
| `test_basic.py` | ⭐ | 10초 | ❌ | 기본 동작 확인 |
| `simple_example.py` | ⭐⭐ | 15초 | ✅ | 기본 시뮬레이션 + 1개 그래프 |
| `simulate_cooling.py` | ⭐⭐⭐ | 1-2분 | ✅ | 12번 시뮬레이션 + 4개 그래프 |
| `interactive_explorer.py` | ⭐⭐⭐⭐ | 대화형 | ✅ | 실시간 파라미터 조정 |

## 📊 생성되는 그래프

### simple_example.py
- 온도 vs 시간 (단일 시뮬레이션)

### simulate_cooling.py
- **cooling_h.png** - 대류 계수(h) 변화: 0.5, 0.7, 1.0, 1.5
- **cooling_m.png** - 질량(m) 변화: 0.05, 0.1, 0.2, 0.3
- **cooling_A.png** - 표면적(A) 변화: 0.5, 1.0, 1.5, 2.0
- **cooling_comparison.png** - 모든 파라미터 최종 온도 비교

### interactive_explorer.py
- 실시간 업데이트되는 온도 그래프 (슬라이더로 조정)

## 🎯 학습 경로

### 1단계: 기초
```bash
python test_basic.py
```
- OMPython 기본 사용법 이해
- 모델 로드, 파라미터 설정, 시뮬레이션 실행

### 2단계: 시각화
```bash
python simple_example.py
```
- matplotlib를 이용한 결과 시각화
- 시뮬레이션 결과 추출 및 분석

### 3단계: 파라미터 스터디
```bash
python simulate_cooling.py
```
- 여러 파라미터 값으로 자동 시뮬레이션
- 파라미터가 시스템에 미치는 영향 분석

### 4단계: 인터랙티브 분석
```bash
python interactive_explorer.py
```
- 실시간 파라미터 조정
- 직관적인 시스템 이해

## 🔍 모델 정보

**모델 파일:** `../../mo_example/bouncingball.mo`
**모델 이름:** `NewtonCoolingDynamic`

**물리적 의미:**
- 뉴턴의 냉각 법칙을 구현
- 물체가 주변 환경과 열교환하며 냉각되는 과정 시뮬레이션

**주요 방정식:**
```
m * c_p * dT/dt = h * A * (T_inf - T)
```

**파라미터:**
- `h`: 대류 냉각 계수 (W/m²·K)
- `m`: 질량 (kg)
- `A`: 표면적 (m²)
- `c_p`: 비열 (J/K·kg)
- `T0`: 초기 온도 (K)

## 💡 팁

1. **처음 사용하는 경우:** `QUICKSTART.md` 먼저 읽기
2. **상세 정보 필요:** `README.md` 참조
3. **문제 발생:** `test_basic.py`로 기본 설정 확인
4. **빠른 테스트:** GUI 없는 `test_basic.py` 사용

## 🛠️ 요구사항

- Python 3.10+
- OpenModelica (omc)
- matplotlib, numpy, pyzmq 등 (requirements.txt 참조)

## 📞 도움말

- [OMPython 문서](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/ompython.html)
- [OpenModelica 포럼](https://forum.openmodelica.org/)
- [GitHub Issues](https://github.com/OpenModelica/OMPython/issues)
