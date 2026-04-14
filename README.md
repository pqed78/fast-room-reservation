# 📅 Premium Meeting Room Reservation System

> **Zero-Build, High-Efficiency, Single-Server Solution**
> 
> 복잡한 빌드 과정 없이, 단 하나의 파이썬 파일만으로 구동되는 초경량 웹 기반 회의실 예약 시스템입니다. React의 현대적인 UI와 FastAPI의 강력한 성능을 결합하여 별도의 프론트엔드 구축 작업(npm) 없이 즉시 배포 및 실행이 가능합니다. 특히 프리미엄 오피스에 걸맞은 높은 수준의 UX/UI를 제공합니다.

---

## ✨ Key Features

### 💎 Premium Glassmorphism UI
* **Dynamic Room Themes**: 각 회의실의 특성에 맞는 고유 테마 컬러(원탁회의실: Amber, 행정쪽: Emerald, 반대쪽: Indigo)가 버튼과 모달 등에 동적으로 적용됩니다.
* **Glassmorphism Aesthetic**: 반투명 요소와 블러 효과를 극대화한 글래스모피즘 표면 처리가 되어있으며, 페이드 인/슬라이드 업 요소의 마이크로 애니메이션으로 매우 고급스러운 조작감을 제공합니다.
* **Built-in Background Server**: AI 모델로 생성된 고화질 오피스 블러 이미지를 FastAPI를 통해 서빙하여, 단일 파일 생태계를 유지하면서도 압도적인 몰입감을 제공합니다.

### 🚀 Zero-Config Architecture
* **No Build Step**: `npm install`이나 `npm run build` 과정이 필요 없습니다. React 18, Tailwind CSS, Babel, Lucide Icons를 모두 CDN 방식으로 연동하여 서버 실행과 동시에 프론트엔드가 즉시 구동됩니다.
* **Single-File Backend**: 모든 백엔드 로직과 HTML 문자열, CSS, JS가 `main.py` 파일 하나에 응축되어 있어 배포 유지보수가 극도로 용이합니다.

### 🏢 Deep Room Management & Time Logic
* **Room-Specific Calendars**: 3개의 분리된 회의실을 지원합니다. 초기 랜딩 페이지에서 회의실을 골라 진입하며, 캘린더는 철저히 해당 회의실 데이터로만 독립되어 동작합니다.
* **Strict Time Validation**: 시작 시간뿐만 아니라 **종료 시간(End Time)** 설정 기능이 추가되었습니다. 종료 시간이 시작 시간보다 앞설 수 없도록 클라이언트 JS 단에서 유효성을 엄격하게 검증합니다.

### 💾 Persistent Data Storage
* **JSON-based Persistence**: `reservations.json` 파일을 사용하여 무거운 데이터베이스 설치 없이도 모든 예약(방 정보, 사용자, 시간 범위) 내역을 Pydantic으로 안전하게 검증하고 영구 저장합니다.

### 🕰️ Interactive Dashboards
* **Real-time Widgets**: 상단 UI 공간에 실시간으로 초 단위로 동작하는 **아날로그 시계**와 직관적인 디지털 날짜/시간 위젯이 탑재되어 있습니다.

---

## 🛠️ Tech Stack

**Backend**
* ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
* ![FastAPI](https://img.shields.com/badge/FastAPI-005571?style=flat-square&logo=fastapi)
* ![uv](https://img.shields.io/badge/uv-Package_Manager-brightgreen?style=flat-square)
* ![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=flat-square)

**Frontend**
* ![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
* ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC?style=flat-square&logo=tailwind-css)
* ![Lucide Icons](https://img.shields.io/badge/Lucide_Icons-UI-blue?style=flat-square)
* ![Babel](https://img.shields.io/badge/Babel-JS_Transpiler-F9DB61?style=flat-square&logo=babel)

---

## 🚀 Getting Started

이 프로젝트는 `uv`를 사용하여 매우 간단하게 실행할 수 있습니다. 

### Prerequisites
* Python 3.10 이상
* **[uv](https://github.com/astral-sh/uv)** (Python 패키지 및 런타임 관리 도구)

### Installation & Execution

1. **저장소 클론**
   ```bash
   git clone https://github.com/your-username/premium-meeting-room.git
   cd premium-meeting-room
   ```

2. **단일 명령어로 서버 실행**
   ```bash
   uv run main.py
   ```

3. **시스템 접속**
   웹 브라우저를 열고 `http://localhost:8000`으로 접속하시면 즉시 모든 기능을 체험할 수 있습니다.

---

## 📂 Project Structure

```text
.
├── main.py              # 전체 백엔드 로직 + FastAPI + React 프론트엔드 UI 통합본
├── reservations.json    # 예약 데이터 파일 (첫 예약 시 자동으로 생성됨)
├── bg.png               # 고화질 프리미엄 오피스 블러 배경 이미지 (FastAPI 서빙)
└── README.md            # 본 설명서 파일
```

---

## 📜 License
This project is licensed under the MIT License.

---
*Designed for simplicity, efficiency, and aesthetic excellence.*