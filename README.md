<div align="center">
  <br />
  <strong>[ 🇰🇷 한국어 (Korean) ](#-한국어-버전)</strong> &nbsp;|&nbsp; <strong>[ 🇺🇸 English ](#-english-version)</strong>
  <br />
  <br />
</div>

<hr>

## 🇰🇷 한국어 버전

# 📅 Premium Meeting Room Reservation System

> **Zero-Build, High-Efficiency, Single-Server Solution**
> 
> 복잡한 빌드 과정 없이, 단 하나의 파이썬 파일만으로 구동되는 초경량 웹 기반 회의실 예약 시스템입니다. React의 현대적인 UI와 FastAPI의 강력한 성능을 결합하여 별도의 프론트엔드 구축 작업(npm) 없이 즉시 배포 및 실행이 가능합니다. 특히 프리미엄 오피스에 걸맞은 높은 수준의 UX/UI를 제공합니다.

### ✨ 특장점 (Key Features)

#### 💎 프리미엄 글래스모피즘 UI
* **다이내믹 룸 테마**: 각 회의실의 특성에 맞는 고유 테마 컬러(원탁회의실: Amber, 행정실쪽: Emerald, 반대쪽: Indigo)가 버튼과 모달 등에 동적으로 적용됩니다.
* **글래스모피즘 미학**: 반투명 요소와 블러 효과를 극대화한 표면 처리가 되어있으며, 부드러운 트랜지션 및 마이크로 애니메이션으로 매우 고급스러운 조작감을 제공합니다.
* **AI 생성 배경 이미지 제공**: AI 모델로 생성된 고화질 오피스 블러 이미지를 자체 백엔드(FastAPI) 포트를 통해 서빙하여, 압도적인 몰입감을 줍니다.

#### 🚀 무설정 아키텍처 (Zero-Config)
* **빌드 단계 생략 (No Build Step)**: `npm install`이나 `npm run build` 과정이 전혀 필요 없습니다. React 18, Tailwind CSS, Babel을 모두 CDN 방식으로 연동하여 서버 실행 즉시 프론트엔드가 렌더링됩니다.
* **단일 파일 백엔드 (Single-File Backend)**: 모든 API 로직과 렌더링용 HTML 템플릿 코드 전체가 `main.py` 파일 단 하나에 포함되어 유지보수가 극도로 용이합니다.

#### 🏢 효율적인 회의실 및 시간 관리
* **개별 회의실 캘린더**: 3개의 분리된 독립된 캘린더를 지원하며 랜딩 화면에서 클릭하여 진입합니다. 예약이 겹치지 않게 철저히 독립적으로 관리됩니다.
* **엄격한 시간 검증 (EndTime Validation)**: 시작 시간에 맞춰 종료 시간(End Time)을 필수로 기입해야 하며, 시간 역전 시 자바스크립트를 통한 철저한 예외 처리를 제공합니다.

#### 💾 영구 데이터 저장
* **DB Free Persistence**: 무거운 데이터베이스 앱이나 Docker 컨테이너 설치 없이, Pydantic으로 철저히 검증된 데이터 포맷을 가벼운 로컬 텍스트 파일(`reservations.json`) 스키마에 영구 저장합니다.

### 🛠️ 개발 스택 (Tech Stack)

* **Backend**: Python 3.10+, FastAPI, uv (런타임 패키지 매니저), Pydantic
* **Frontend**: React 18 (CDN), Tailwind CSS (CDN), Lucide Icons, Babel

### 🚀 사용 방법 (Getting Started)

이 프로젝트는 최신 파이썬 패키지 매니저 `uv`와 PEP 723 스펙을 사용하므로, 깃허브에서 클론 받은 후 **아무것도 추가로 설치하실 필요가 없습니다!**

```bash
git clone https://github.com/pqed78/fast-room-reservation.git
cd fast-room-reservation

# 단일 명령어로 필요한 패키지 다운 및 서버 즉시 자동 실행 
uv run main.py
```
이후 웹 브라우저를 열고 `http://localhost:8000`으로 접속하시면 즉시 모든 기능을 체험할 수 있습니다.

---

<br /><br /><br />

## 🇺🇸 English Version

# 📅 Premium Meeting Room Reservation System

> **Zero-Build, High-Efficiency, Single-Server Solution**
> 
> An ultra-lightweight, web-based meeting room reservation system powered by just a single Python file, without complex build processes. Combining modern React UIs with robust FastAPI performance, you can instantly deploy and run the app with absolutely no frontend build scaffolding (no node_modules, no npm).

### ✨ Key Features

#### 💎 Premium Glassmorphism UI
* **Dynamic Room Themes**: Distinct theme colors (Amber, Emerald, Indigo) are dynamically applied to UI components based on the room you select.
* **Glassmorphism Aesthetic**: Achieves high-end transparency and blur effects, complete with sophisticated fade/slide-up micro-animations for an elegant user experience.
* **Built-in Background Serving**: Provides an immersive atmosphere with an AI-generated blurred premium office background, served seamlessly via FastAPI.

#### 🚀 Zero-Config Architecture
* **No Build Step**: Forget about `npm install` or `npm run build`. Leveraging React 18, Tailwind CSS, and Babel purely via CDN, the entire frontend is instantly integrated the moment the server boots up.
* **Single-File Backend**: Experience ultimate operational ease. All backend logics, API abstractions, and HTML/CSS/JS frontend templates are elegantly combined into one single `main.py` file.

#### 🏢 Deep Room Management & Time Logic
* **Room-Specific Calendars**: Manage dependencies over 3 different meeting rooms. Users enter a specific room from a beautiful landing page, unlocking an independent calendar specific to that room.
* **Strict Time Validation**: Enhanced with **End Time** implementations featuring strict client-side validation logic prohibiting reversed timestamp assignments.

#### 💾 Persistent Data Storage
* **JSON-based Persistence**: Safely stores all reservation transactions implicitly inside a lightweight local file schema (`reservations.json`) leveraging robust `Pydantic` validations, completely eliminating the overhead of classic relational database constraints.

### 🛠️ Tech Stack

* **Backend**: Python 3.10+, FastAPI, uv (Runtime config manager), Pydantic
* **Frontend**: React 18 (CDN), Tailwind CSS (CDN), Lucide Icons, Babel

### 🚀 Getting Started

This project uses the modern Python package manager `uv` alongside PEP 723 script metadata. Wait, this means **you don't even have to manually install any packages!**

```bash
git clone https://github.com/pqed78/fast-room-reservation.git
cd fast-room-reservation

# One pure command dynamically resolves dependencies and fires up the server 
uv run main.py
```
Open a web browser and visit `http://localhost:8000` to dive right into the experience.

---

## 📂 Project Structure

```text
.
├── main.py              # The Heart Core (Backend + React Frontend integrated)
├── reservations.json    # Auto-generated lightweight storage
├── bg.png               # AI-generated aesthetic background serving target
└── README.md            # This Documentation
```

## 📜 License
This project is licensed under the MIT License.