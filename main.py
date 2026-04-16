# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "pydantic",
# ]
# ///

import uvicorn
import json
import uuid
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
from datetime import datetime

app = FastAPI()

DB_FILE = Path("reservations.json")

def load_db():
    if not DB_FILE.exists():
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

LOG_FILE = Path("activity.log")

def log_activity(action, res_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{now}] [{action}] 회의실: {res_data.get('roomName')}, 예약자: {res_data.get('userName')}, 일시: {res_data.get('date')} {res_data.get('time')}~{res_data.get('endTime')}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg)

class ReservationBase(BaseModel):
    date: str
    time: str
    endTime: str
    roomName: str
    userName: str
    password: str

class Reservation(ReservationBase):
    id: str

class ReservationOut(BaseModel):
    id: str
    date: str
    time: str
    endTime: str
    roomName: str
    userName: str

@app.get("/api/reservations", response_model=List[ReservationOut])
async def get_reservations():
    data = load_db()
    for d in data:
        d.pop("password", None)
    return data

@app.post("/api/reservations", response_model=ReservationOut)
async def create_reservation(res: ReservationBase):
    data = load_db()
    
    for existing in data:
        if existing.get("date") == res.date and existing.get("roomName") == res.roomName:
            if max(existing.get("time", ""), res.time) < min(existing.get("endTime", ""), res.endTime):
                raise HTTPException(status_code=400, detail="이미 예약된 시간입니다.")
                
    new_res = res.model_dump()
    new_res["id"] = str(uuid.uuid4())
    data.append(new_res)
    save_db(data)
    log_activity("신청", new_res)
    new_res.pop("password", None)
    return new_res

@app.delete("/api/reservations/{res_id}")
async def delete_reservation(res_id: str, password: str = ""):
    data = load_db()
    
    target = next((d for d in data if str(d.get("id")) == res_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Not found")
        
    correct_pw = target.get("password") or ""
    if correct_pw and password != correct_pw:
        raise HTTPException(status_code=401, detail="암호가 일치하지 않습니다.")
        
    log_activity("취소", target)
    filtered = [d for d in data if str(d.get("id")) != res_id]
    save_db(filtered)
    return {"status": "success"}

@app.get("/bg.png")
async def get_bg():
    if os.path.exists("bg.png"):
        return FileResponse("bg.png")
    return HTMLResponse(status_code=404)

# HTML Template (React, Babel, Tailwind, Lucide CDN 포함)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>프리미엄 회의실 예약 시스템</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Pretendard"', '"Inter"', 'sans-serif'],
                    },
                    animation: {
                        'fade-in': 'fadeIn 0.5s ease-out',
                        'slide-up': 'slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
                    },
                    keyframes: {
                        fadeIn: {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' },
                        },
                        slideUp: {
                            '0%': { transform: 'translateY(20px)', opacity: '0' },
                            '100%': { transform: 'translateY(0)', opacity: '1' },
                        }
                    }
                }
            }
        }
    </script>
    
    <!-- React & ReactDOM CDN -->
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    
    <!-- Babel CDN (JSX 변환용) -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" rel="stylesheet" />

    <style>
        body { margin: 0; padding: 0; background-color: #0f172a; overflow-x: hidden; }
        /* 스크롤바 커스텀 */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(203, 213, 225, 0.5); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.8); }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }
    </style>
</head>
<body class="text-slate-800">
    <!-- 배경 이미지 -->
    <div class="fixed inset-0 z-[-1] bg-cover bg-center transition-all duration-1000 ease-in-out" style="background-image: url('/bg.png'); filter: blur(5px) brightness(0.95); transform: scale(1.05);"></div>
    <div class="fixed inset-0 z-[-1] bg-gradient-to-br from-slate-900/40 to-slate-800/20"></div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        const getTheme = (room) => {
            switch (room) {
                case "원탁회의실": return { name: "원탁회의실", color: "amber", bg: "bg-amber-500", text: "text-amber-700", lightBg: "bg-amber-100/50", border: "border-amber-500", hover: "hover:bg-amber-50", ring: "focus:ring-amber-500", btnHover: "hover:bg-amber-600", shadow: "shadow-amber-500/30" };
                case "행정실쪽 회의실": return { name: "행정실쪽 회의실", color: "emerald", bg: "bg-emerald-500", text: "text-emerald-700", lightBg: "bg-emerald-100/50", border: "border-emerald-500", hover: "hover:bg-emerald-50", ring: "focus:ring-emerald-500", btnHover: "hover:bg-emerald-600", shadow: "shadow-emerald-500/30" };
                case "행정실 반대쪽 회의실": return { name: "행정실 반대쪽 회의실", color: "indigo", bg: "bg-indigo-500", text: "text-indigo-700", lightBg: "bg-indigo-100/50", border: "border-indigo-500", hover: "hover:bg-indigo-50", ring: "focus:ring-indigo-500", btnHover: "hover:bg-indigo-600", shadow: "shadow-indigo-500/30" };
                default: return { color: "slate", bg: "bg-slate-700", text: "text-slate-800", lightBg: "bg-slate-100/50", border: "border-slate-500", hover: "hover:bg-slate-50", ring: "focus:ring-slate-500", btnHover: "hover:bg-slate-800", shadow: "shadow-slate-500/30" };
            }
        };

        const AnalogClock = ({ time, themeText }) => {
            const seconds = time.getSeconds();
            const minutes = time.getMinutes();
            const hours = time.getHours();

            const secondDeg = seconds * 6;
            const minuteDeg = minutes * 6 + seconds * 0.1;
            const hourDeg = (hours % 12) * 30 + minutes * 0.5;

            return (
                <div className={`relative w-20 h-20 flex-shrink-0 rounded-full border-4 border-slate-700 bg-white/80 backdrop-blur-sm shadow-inner flex items-center justify-center transition-colors duration-500`}>
                    {/* 눈금선 로직 (간단 버전) */}
                    {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map(deg => (
                        <div key={deg} className="absolute w-[2px] h-2 bg-slate-200" style={{ transform: `rotate(${deg}deg) translateY(-32px)`}}></div>
                    ))}
                    <div className={`absolute w-3 h-3 rounded-full z-20 bg-slate-800`}></div>
                    <div className={`absolute w-1.5 rounded-full origin-bottom bg-slate-800 z-10 transition-transform duration-200`} style={{ height: '30%', bottom: '50%', transform: `translateX(-50%) rotate(${hourDeg}deg)` }}></div>
                    <div className={`absolute w-1 rounded-full origin-bottom bg-slate-600 z-10 transition-transform duration-200`} style={{ height: '40%', bottom: '50%', transform: `translateX(-50%) rotate(${minuteDeg}deg)` }}></div>
                    <div className={`absolute w-[2px] rounded-full origin-bottom bg-red-500 z-10 transition-transform duration-75`} style={{ height: '45%', bottom: '50%', transform: `translateX(-50%) rotate(${secondDeg}deg)` }}></div>
                </div>
            );
        };

        const CurrentTimeDisplay = ({ theme }) => {
            const [now, setNow] = useState(new Date());

            useEffect(() => {
                const timer = setInterval(() => setNow(new Date()), 1000);
                return () => clearInterval(timer);
            }, []);

            return (
                <div className="glass-panel p-6 rounded-3xl mb-8 border-l-8 flex items-center gap-6 animate-fade-in transition-all duration-500" style={{ borderLeftColor: theme ? `var(--tw-color-${theme.color}-500)` : '#3b82f6' }}>
                    <AnalogClock time={now} themeText={theme?.text || 'text-blue-600'} />
                    <div>
                        <h3 className="text-xl font-bold tracking-tight text-slate-800/80">
                            {now.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}
                        </h3>
                        <p className={`text-4xl font-mono font-black mt-1 tracking-wider ${theme?.text || 'text-blue-600'} drop-shadow-sm`}>
                            {now.toLocaleTimeString('ko-KR')}
                        </p>
                    </div>
                </div>
            );
        };

        const MeetingRoomReservation = () => {
            const [view, setView] = useState('selection');
            const [selectedRoom, setSelectedRoom] = useState(null);
            
            const [currentDate, setCurrentDate] = useState(new Date());
            const [reservations, setReservations] = useState([]);
            const [isModalOpen, setIsModalOpen] = useState(false);
            const [selectedDate, setSelectedDate] = useState(null);
            
            const [formData, setFormData] = useState({
                time: '',
                endTime: '',
                userName: '',
                password: ''
            });

            const rooms = ["원탁회의실", "행정실쪽 회의실", "행정실 반대쪽 회의실"];
            const currentTheme = selectedRoom ? getTheme(selectedRoom) : null;

            useEffect(() => {
                if (window.lucide) {
                    window.lucide.createIcons();
                }
            }, [reservations, isModalOpen, currentDate, view, selectedRoom]);

            useEffect(() => {
                fetch('/api/reservations')
                    .then(res => res.json())
                    .then(data => setReservations(data))
                    .catch(err => console.error("예약 정보를 불러오는데 실패했습니다.", err));
            }, []);

            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();

            const firstDayOfMonth = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            const daysInPrevMonth = new Date(year, month, 0).getDate();

            const calendarDays = [];
            for (let i = firstDayOfMonth - 1; i >= 0; i--) {
                calendarDays.push({ day: daysInPrevMonth - i, month: month - 1, currentMonth: month });
            }
            for (let i = 1; i <= daysInMonth; i++) {
                calendarDays.push({ day: i, month: month, currentMonth: month });
            }

            const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
            const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));
            const goToToday = () => setCurrentDate(new Date());

            const handleDateClick = (day, m) => {
                setSelectedDate(new Date(year, m, day));
                setIsModalOpen(true);
            };

            const handleInputChange = (e) => {
                setFormData({ ...formData, [e.target.name]: e.target.value });
            };

            const handleSubmit = async (e) => {
                e.preventDefault();
                if (!formData.time || !formData.endTime || !formData.userName || !formData.password) return alert("모든 필드를 채워주세요.");

                if (formData.time >= formData.endTime) {
                    return alert("종료 시간은 시작 시간보다 늦어야 합니다.");
                }

                const newResData = {
                    date: selectedDate.toDateString(),
                    roomName: selectedRoom,
                    ...formData
                };

                try {
                    const response = await fetch('/api/reservations', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(newResData)
                    });
                    
                    if (response.ok) {
                        const savedRes = await response.json();
                        setReservations([...reservations, savedRes]);
                        setIsModalOpen(false);
                        setFormData({ time: '', endTime: '', userName: '', password: '' });
                    } else {
                        const errData = await response.json();
                        alert(errData.detail || "예약 등록에 실패했습니다.");
                    }
                } catch (error) {
                    console.error(error);
                    alert("예약 중 서버 통신 오류가 발생했습니다.");
                }
            };

            const deleteReservation = async (id) => {
                const password = window.prompt("예약을 취소하려면 설정한 비밀번호를 입력하세요:");
                if (password === null) return; // 취소 버튼 클릭시

                try {
                    const response = await fetch(`/api/reservations/${id}?password=${encodeURIComponent(password)}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        setReservations(reservations.filter(res => res.id !== id));
                    } else {
                        const errData = await response.json();
                        alert(errData.detail || "예약 취소에 실패했습니다.");
                    }
                } catch (error) {
                    console.error(error);
                    alert("삭제 중 서버 통신 오류가 발생했습니다.");
                }
            };

            // 랜딩 페이지 화면
            if (view === 'selection') {
                return (
                    <div className="p-8 mx-auto min-h-screen flex flex-col items-center justify-center animate-fade-in relative z-10 w-full max-w-7xl">
                        <div className="absolute top-8 left-8 right-8 flex justify-center">
                            <div className="w-full max-w-4xl">
                                <CurrentTimeDisplay />
                            </div>
                        </div>
                        <div className="glass-panel p-16 rounded-[40px] mt-24 animate-slide-up max-w-5xl w-full text-center shadow-2xl">
                            <h1 className="text-5xl font-black text-slate-800 mb-4 tracking-tight drop-shadow-sm">어느 공간에서 회의하시겠습니까?</h1>
                            <p className="text-xl text-slate-500 font-medium mb-16">현대적이고 편리한 프리미엄 공간 예약을 시작합니다.</p>
                            
                            <div className="grid md:grid-cols-3 gap-8 w-full place-items-stretch">
                                {rooms.map((room, idx) => {
                                    const theme = getTheme(room);
                                    return (
                                        <button 
                                            key={room}
                                            onClick={() => { setSelectedRoom(room); setView('calendar'); }}
                                            className={`glass-card p-10 rounded-3xl hover:-translate-y-3 hover:shadow-2xl hover:${theme.shadow} transition-all duration-300 border-t border-l border-r border-b-8 ${theme.border} flex flex-col items-center justify-center group cursor-pointer h-64`}
                                            type="button"
                                            style={{ animationDelay: `${idx * 100}ms` }}
                                        >
                                            <div className={`w-16 h-16 rounded-2xl ${theme.lightBg} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                                                <i data-lucide="door-open" className={`w-8 h-8 ${theme.text}`}></i>
                                            </div>
                                            <h2 className="text-2xl font-bold text-slate-700 group-hover:text-slate-900">{room}</h2>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    </div>
                );
            }

            // 달력 뷰 화면
            return (
                <div className="p-6 max-w-6xl mx-auto min-h-screen relative z-10 animate-fade-in">
                    <CurrentTimeDisplay theme={currentTheme} />

                    <div className="glass-panel p-8 rounded-3xl shadow-xl animate-slide-up">
                        {/* 네비게이션 헤더 */}
                        <div className="flex items-center justify-between mb-10 pb-6 border-b border-slate-200/50">
                            <button 
                                onClick={() => setView('selection')}
                                className="flex items-center gap-3 text-slate-500 hover:text-slate-800 font-bold transition-colors cursor-pointer text-lg group"
                                type="button"
                            >
                                <div className="p-2 rounded-full bg-white/50 group-hover:bg-white transition-colors shadow-sm">
                                    <i data-lucide="arrow-left" className="w-5 h-5"></i>
                                </div>
                                <span>회의실 목록</span>
                            </button>
                            <div className={`flex items-center gap-3 px-6 py-3 rounded-2xl ${currentTheme.lightBg} shadow-sm border border-white/40`}>
                                <div className={`w-3 h-3 rounded-full ${currentTheme.bg} animate-pulse`}></div>
                                <span className={`text-xl font-black tracking-tight ${currentTheme.text}`}>
                                    {selectedRoom}
                                </span>
                            </div>
                        </div>

                        {/* 달력 헤더 */}
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-4xl font-black text-slate-800 tracking-tighter">
                                {year}년 <span className={currentTheme.text}>{month + 1}월</span>
                            </h2>
                            <div className="flex gap-3">
                                <button onClick={goToToday} className={`px-4 py-2 bg-white/60 hover:bg-white rounded-xl shadow-sm transition-all focus:outline-none focus:ring-2 ${currentTheme.ring} font-bold text-slate-700 flex items-center gap-1`}>
                                    <i data-lucide="calendar" className="w-4 h-4"></i> 오늘
                                </button>
                                <button onClick={prevMonth} className={`p-3 bg-white/60 hover:bg-white rounded-xl shadow-sm transition-all focus:outline-none focus:ring-2 ${currentTheme.ring}`}>
                                    <i data-lucide="chevron-left" className="w-6 h-6 text-slate-600"></i>
                                </button>
                                <button onClick={nextMonth} className={`p-3 bg-white/60 hover:bg-white rounded-xl shadow-sm transition-all focus:outline-none focus:ring-2 ${currentTheme.ring}`}>
                                    <i data-lucide="chevron-right" className="w-6 h-6 text-slate-600"></i>
                                </button>
                            </div>
                        </div>

                        {/* 달력 그리드 */}
                        <div className="grid grid-cols-7 gap-3">
                            {['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map((d, i) => (
                                <div key={d} className={`text-center font-bold text-sm tracking-widest py-3 rounded-xl bg-white/40 shadow-sm ${i===0 ? 'text-rose-500' : i===6 ? 'text-blue-500' : 'text-slate-500'}`}>{d}</div>
                            ))}
                            
                            {calendarDays.map((item, idx) => {
                                const isCurrentMonth = item.month === month;
                                const dateString = new Date(year, item.month, item.day).toDateString();
                                const dayReservations = reservations
                                    .filter(res => res.date === dateString && res.roomName === selectedRoom)
                                    .sort((a,b) => a.time.localeCompare(b.time)); // 시간순 정렬

                                return (
                                    <div 
                                        key={idx}
                                        onClick={() => isCurrentMonth && handleDateClick(item.day, item.month)}
                                        className={`min-h-[140px] p-3 rounded-2xl transition-all cursor-pointer backdrop-blur-sm border
                                            ${!isCurrentMonth ? 'glass-card border-transparent text-slate-400 opacity-60' : `bg-white/80 border-white/60 shadow-sm hover:translate-y-[-2px] hover:shadow-md ${currentTheme.hover}`}
                                        `}
                                    >
                                        <div className="flex justify-between items-start mb-2">
                                            <span className={`text-lg font-black ${item.month !== month ? 'text-slate-400' : 'text-slate-700'}`}>{item.day}</span>
                                            {dayReservations.length > 0 && isCurrentMonth && (
                                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${currentTheme.lightBg} ${currentTheme.text}`}>
                                                    {dayReservations.length}건
                                                </span>
                                            )}
                                        </div>
                                        <div className="flex flex-col gap-1.5 mt-2">
                                            {dayReservations.map((res, i) => (
                                                <div key={res.id} onClick={(e) => e.stopPropagation()} className={`group relative text-xs p-2 rounded-xl backdrop-blur-md transition-all shadow-sm ${currentTheme.lightBg} border border-white/50 text-slate-800`}>
                                                    <button 
                                                        type="button"
                                                        onClick={(e) => { e.preventDefault(); e.stopPropagation(); deleteReservation(res.id); }}
                                                        className={`absolute -right-2 -top-2 opacity-0 group-hover:opacity-100 bg-rose-500 text-white rounded-full w-5 h-5 text-[10px] shadow-md flex items-center justify-center cursor-pointer transition-all z-10 hover:scale-110 hover:bg-rose-600`}
                                                    ><i data-lucide="x" className="w-3 h-3"></i></button>
                                                    <div className={`font-black tracking-tight ${currentTheme.text} mb-0.5`}>{res.time} ~ {res.endTime}</div>
                                                    <div className="font-medium text-slate-600 flex items-center gap-1 opacity-90 truncate">
                                                        <i data-lucide="user" className="w-3 h-3"></i> {res.userName}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* 예약 모달 */}
                    {isModalOpen && (
                        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
                            <div className="bg-white/90 backdrop-blur-xl border border-white rounded-[32px] p-8 w-full max-w-md shadow-[0_30px_60px_-15px_rgba(0,0,0,0.3)] animate-slide-up">
                                <div className="flex justify-between items-center mb-8">
                                    <div>
                                        <p className="text-sm font-bold text-slate-400 mb-1">{selectedDate.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}</p>
                                        <h3 className="text-2xl font-black text-slate-800 flex items-center gap-2">
                                            <div className={`w-3 h-3 rounded-full ${currentTheme.bg}`}></div>
                                            {selectedRoom} 예약
                                        </h3>
                                    </div>
                                    <button type="button" onClick={() => setIsModalOpen(false)} className="p-2 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors">
                                        <i data-lucide="x" className="text-slate-600"></i>
                                    </button>
                                </div>
                                
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">시작 시간</label>
                                            <input type="time" name="time" value={formData.time} onChange={handleInputChange} className={`w-full p-3.5 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 ${currentTheme.ring} focus:bg-white transition-all font-mono text-lg font-bold text-slate-700`} required />
                                        </div>
                                        <div>
                                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">종료 시간</label>
                                            <input type="time" name="endTime" value={formData.endTime} onChange={handleInputChange} className={`w-full p-3.5 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 ${currentTheme.ring} focus:bg-white transition-all font-mono text-lg font-bold text-slate-700`} required />
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">예약자 성함</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                                    <i data-lucide="user" className="w-5 h-5 text-slate-400"></i>
                                                </div>
                                                <input type="text" name="userName" value={formData.userName} onChange={handleInputChange} className={`w-full pl-11 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 ${currentTheme.ring} focus:bg-white transition-all text-slate-700 font-bold`} placeholder="예: 홍길동 책임" required />
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">비밀번호</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                                    <i data-lucide="lock" className="w-5 h-5 text-slate-400"></i>
                                                </div>
                                                <input type="password" name="password" value={formData.password} onChange={handleInputChange} className={`w-full pl-11 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 ${currentTheme.ring} focus:bg-white transition-all text-slate-700 font-bold`} placeholder="취소용 암호" required />
                                            </div>
                                        </div>
                                    </div>
                                    <button type="submit" className={`w-full ${currentTheme.bg} text-white py-4 mt-8 rounded-2xl font-black text-lg ${currentTheme.btnHover} shadow-lg ${currentTheme.shadow} transition-all hover:-translate-y-1`}>
                                        확인 및 예약 완료
                                    </button>
                                </form>
                            </div>
                        </div>
                    )}
                </div>
            );
        };
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<MeetingRoomReservation />);
    </script>
</body>
</html>
"""

@app.get("/")
async def get_index():
    return HTMLResponse(content=HTML_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)