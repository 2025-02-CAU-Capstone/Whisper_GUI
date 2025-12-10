import os
os.environ["KSS_DISABLE_AUGMENTATION"] = "1"


"""
Whisper STT GUI - 동영상을 문장별 타임스탬프 TXT로 변환
MP4/AVI/MKV/MOV 등 다양한 동영상 파일 지원
"""




import re
import sys
import json
import threading
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkfont
from faster_whisper import WhisperModel
import kss  # 한국어 문장 분리기
import requests
<<<<<<< HEAD
# import torch

# 다크 테마 색상
# Toss-style pastel / light UI 색상 세트
COLORS = {
    'bg': '#f5f7fa',          # 전체 배경 (파스텔 라이트 톤)
    'fg': '#333333',          # 기본 텍스트 (짙은 회색)

    'input_bg': '#ffffff',    # Entry, Listbox 등의 배경색
    'border': '#d0d7e2',      # 연한 보더색

    # Button (primary)
    'accent': '#5b7cfa',      # primary color
    'button_bg': '#e3f2fd',   # 파스텔 블루 버튼 배경
    'button_hover': '#4a63c9', # hover primary

    # 상태 색상
    'success': '#6ee7b7',     # 초록 성공 메시지
    'error': '#fb7185',       # 오류(레드-핑크)

    # listbox selection colors
    'select_bg': '#c7d2fe',   # 밝은 인디고
    'select_fg': '#ffffff'
=======
import torch

# 다크 테마 색상
COLORS = {
    'bg': '#1e1e1e',
    'fg': '#ffffff',
    'button_bg': '#3a3a3a',
    'button_hover': '#4a4a4a',
    'accent': '#007acc',
    'success': '#4caf50',
    'error': '#f44336',
    'border': '#555555',
    'input_bg': '#2d2d2d'
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
}

class WhisperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper STT - 동영상 → 텍스트 변환")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS['bg'])
        
        # 윈도우 아이콘 설정 (옵션)
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 변수 초기화
        self.input_file = None
        self.output_file = None
        self.model = None
        self.is_processing = False
        self.process_thread = None
        
        # 설정 저장/로드
        self.config_file = Path.home() / '.whisper_stt_config.json'
        self.load_config()
        
        # UI 구성
        self.setup_styles()
        self.create_widgets()
        
        # 윈도우 닫기 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styles(self):
        """ttk 스타일 설정"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 버튼 스타일
        self.style.configure('Accent.TButton',
                           background=COLORS['accent'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat')
        self.style.map('Accent.TButton',
                      background=[('active', '#005a9e')])
        
        # 프레임 스타일
        self.style.configure('Dark.TFrame',
                           background=COLORS['bg'])
        
        # 레이블 스타일
        self.style.configure('Dark.TLabel',
                           background=COLORS['bg'],
                           foreground=COLORS['fg'])
        
        # 콤보박스 스타일
        self.style.configure('Dark.TCombobox',
                           fieldbackground=COLORS['input_bg'],
                           background=COLORS['button_bg'],
                           foreground=COLORS['fg'])
        
    def create_dark_popup(self, title="Popup", size="350x300"):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(size)
        popup.configure(bg=COLORS['bg'])

        # 팝업의 Label 기본색상
        def dark_label(text):
            return tk.Label(popup, text=text, bg=COLORS['bg'], fg=COLORS['fg'], font=('Segoe UI', 10))

        # Entry 생성 함수
        def dark_entry():
            return tk.Entry(popup, bg=COLORS['input_bg'], fg=COLORS['fg'], insertbackground=COLORS['fg'])

        # Button 생성 함수
        def dark_button(text, cmd):
            return tk.Button(
                popup,
                text=text,
                command=cmd,
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['accent'],
                fg='white',
                activebackground='#005a9e',
                activeforeground='white',
                bd=0,
                padx=15,
                pady=5,
                cursor='hand2'
            )

        return popup, dark_label, dark_entry, dark_button

        
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 컨테이너
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 제목
        title_label = tk.Label(main_container, 
<<<<<<< HEAD
                              text="P2L - Problem to Lecture: 강의 자막 생성기",
=======
                              text="🎬 동영상 → 문장별 타임스탬프 변환",
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
                              font=('Segoe UI', 18, 'bold'),
                              bg=COLORS['bg'], fg=COLORS['fg'])
        title_label.pack(pady=(0, 20))
        
        # README (사용법) 섹션
        self.create_usage_note_section(main_container)

        # 파일 선택 섹션
        self.create_file_section(main_container)
        
        # 설정 섹션
        self.create_settings_section(main_container)
        
        # 변환 버튼
        self.create_convert_button(main_container)
        
        # 로그 출력 섹션
        self.create_log_section(main_container)
        
        # 진행 상태 바
        self.create_progress_section(main_container)
        
    def create_file_section(self, parent):
        """파일 선택 섹션"""
        file_frame = tk.Frame(parent, bg=COLORS['bg'])
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 입력 파일
        input_frame = tk.Frame(file_frame, bg=COLORS['bg'])
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="입력 동영상:", 
                font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['fg']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.input_label = tk.Label(input_frame, 
                                   text="파일을 선택하세요",
                                   font=('Segoe UI', 10),
                                   bg=COLORS['input_bg'], 
                                   fg='#888888',
                                   anchor='w',
                                   padx=10,
                                   pady=8)
        self.input_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(input_frame, 
                 text="📁 선택",
                 font=('Segoe UI', 10),
                 bg=COLORS['button_bg'],
                 fg=COLORS['fg'],
                 activebackground=COLORS['button_hover'],
                 activeforeground=COLORS['fg'],
                 bd=0,
                 padx=20,
                 command=self.select_input_file).pack(side=tk.LEFT, padx=(10, 0))
        
        # # 출력 파일
        # output_frame = tk.Frame(file_frame, bg=COLORS['bg'])
        # output_frame.pack(fill=tk.X)
        
        # tk.Label(output_frame, text="출력 파일:  ", 
        #         font=('Segoe UI', 10),
        #         bg=COLORS['bg'], fg=COLORS['fg']).pack(side=tk.LEFT, padx=(0, 10))
        
        # self.output_label = tk.Label(output_frame, 
        #                             text="자동 설정됨",
        #                             font=('Segoe UI', 10),
        #                             bg=COLORS['input_bg'], 
        #                             fg='#888888',
        #                             anchor='w',
        #                             padx=10,
        #                             pady=8)
        # self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # tk.Button(output_frame, 
        #          text="📝 변경",
        #          font=('Segoe UI', 10),
        #          bg=COLORS['button_bg'],
        #          fg=COLORS['fg'],
        #          activebackground=COLORS['button_hover'],
        #          activeforeground=COLORS['fg'],
        #          bd=0,
        #          padx=20,
        #          command=self.select_output_file).pack(side=tk.LEFT, padx=(10, 0))
    

    def create_usage_note_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="📢 사용법 안내",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            bd=1
        )
        frame.pack(fill=tk.X, pady=(0, 15))

        label = tk.Label(
            frame,
            text=(
                "1. 먼저 \"수업(Lecture)\"을 등록하거나 기존 목록에서 선택하세요.\n"
                "2. 선택한 수업 안에서 \"강의(Chapter)\"를 등록하세요.\n"
                "3. 이후 변환할 영상 파일을 선택하고, 제공된 수업 (Lecture)의 ID와 강의 (Chapter)의 ID를 입력 후 \"변환 시작\" 버튼을 누르세요."
            ),
            justify="left",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=('Segoe UI', 10),
            anchor='w'
        )
        label.pack(fill=tk.X, padx=10, pady=10)



    def create_settings_section(self, parent):
        """설정 섹션"""
        settings_frame = tk.LabelFrame(parent, 
                                      text="⚙️ 설정",
                                      font=('Segoe UI', 11, 'bold'),
                                      bg=COLORS['bg'], 
                                      fg=COLORS['fg'],
                                      relief=tk.GROOVE,
                                      bd=1)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        inner_frame = tk.Frame(settings_frame, bg=COLORS['bg'])
        inner_frame.pack(padx=15, pady=15)
        
        # 1. 모델 크기 + 언어 선택 (한 줄, center-align)
        row1_container = tk.Frame(inner_frame, bg=COLORS['bg'])
        row1_container.pack(fill=tk.X)

        row1 = tk.Frame(inner_frame, bg=COLORS['bg'])
        row1.pack(pady=10)

        model_frame = tk.Frame(row1, bg=COLORS['bg'])
        model_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(model_frame, text="모델 크기:",
                font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['fg']).pack(anchor="w")

        self.model_var = tk.StringVar(value=self.config.get('model', 'base'))
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=['tiny', 'base', 'small', 'medium', 'large-v3'],
            state='readonly',
            width=15,
            style='Dark.TCombobox'
        )
        model_combo.pack(anchor="w", pady=3)

        # 모델 설명
        model_info = {
            'tiny': '가장 빠름 (정확도 낮음)',
            'base': '균형잡힌 선택 (추천)',
            'small': '준수한 정확도',
            'medium': '높은 정확도',
            'large-v3': '최고 정확도 (느림)'
        }

        self.model_info_label = tk.Label(
            model_frame,
            text=model_info.get(self.model_var.get(), ''),
            font=('Segoe UI', 9),
            bg=COLORS['bg'], fg='#888888'
        )
        self.model_info_label.pack(anchor="w")

        def update_model_info(event):
            self.model_info_label.config(text=model_info.get(self.model_var.get(), ''))

        model_combo.bind('<<ComboboxSelected>>', update_model_info)

        # 언어 선택
        lang_frame = tk.Frame(row1, bg=COLORS['bg'])
        lang_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(lang_frame, text="언어:",
                font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['fg']).pack(anchor="w")

        self.lang_var = tk.StringVar(value=self.config.get('language', 'ko'))
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=['ko', 'en', 'ja', 'zh', 'auto'],
            state='readonly',
            width=15,
            style='Dark.TCombobox'
        )
        lang_combo.pack(anchor="w", pady=3)

        lang_names = {
            'ko': '한국어',
            'en': '영어',
            'ja': '일본어',
            'zh': '중국어',
            'auto': '자동 감지'
        }

        self.lang_info_label = tk.Label(
            lang_frame,
            text=lang_names.get(self.lang_var.get(), ''),
            font=('Segoe UI', 9),
            bg=COLORS['bg'], fg='#888888'
        )
        self.lang_info_label.pack(anchor="w")

        def update_lang_info(event):
            self.lang_info_label.config(text=lang_names.get(self.lang_var.get(), ''))

        lang_combo.bind('<<ComboboxSelected>>', update_lang_info)


<<<<<<< HEAD
        #        # 2. 수업(LECTURE) 제목 + 강의(CHAPTER) 제목 표시 영역
=======
        # 2. 수업 고유번호 + 강의 고유번호 (한 줄)
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
        row2_container = tk.Frame(inner_frame, bg=COLORS['bg'])
        row2_container.pack(fill=tk.X)

        row2 = tk.Frame(row2_container, bg=COLORS['bg'])
        row2.pack(pady=10)

<<<<<<< HEAD
        # ─────────────────────────────
        # 수업 (Lecture)
        # ─────────────────────────────
        lecture_frame = tk.Frame(row2, bg=COLORS['bg'])
        lecture_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(
            lecture_frame,
            text="수업:",
            bg=COLORS['bg'],
            fg=COLORS['fg']
        ).pack(anchor="w")

        # 제목 표시용 Label
        self.lecture_title_var = tk.StringVar(value="선택된 수업 없음")
        lecture_title_label = tk.Label(
            lecture_frame,
            textvariable=self.lecture_title_var,
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            anchor="w",
            padx=10,
            pady=8
        )
        lecture_title_label.pack(fill="x")

        # 숨겨진 ID 저장용 변수 (UI에 표시 X)
        self.lecture_var = tk.StringVar()


        # ─────────────────────────────
        # 강의 (Chapter)
        # ─────────────────────────────
        chapter_frame = tk.Frame(row2, bg=COLORS['bg'])
        chapter_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(
            chapter_frame,
            text="강의:",
            bg=COLORS['bg'],
            fg=COLORS['fg']
        ).pack(anchor="w")

        self.chapter_title_var = tk.StringVar(value="선택된 강의 없음")
        chapter_title_label = tk.Label(
            chapter_frame,
            textvariable=self.chapter_title_var,
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            anchor="w",
            padx=10,
            pady=8
        )
        chapter_title_label.pack(fill="x")

        # 숨겨진 ID 저장 변수
        self.chapter_var = tk.StringVar()
=======
        lecture_frame = tk.Frame(row2, bg=COLORS['bg'])
        lecture_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(lecture_frame, text="수업 고유번호:",
                bg=COLORS['bg'], fg=COLORS['fg']).pack(anchor="w")

        self.lecture_var = tk.StringVar()
        tk.Entry(lecture_frame,
                textvariable=self.lecture_var,
                bg=COLORS['input_bg'], fg=COLORS['fg'],
                insertbackground=COLORS['fg']).pack(anchor="w")

        chapter_frame = tk.Frame(row2, bg=COLORS['bg'])
        chapter_frame.pack(side=tk.LEFT, padx=20, expand=True)

        tk.Label(chapter_frame, text="강의 고유번호:",
                bg=COLORS['bg'], fg=COLORS['fg']).pack(anchor="w")

        self.chapter_var = tk.StringVar()
        tk.Entry(chapter_frame,
                textvariable=self.chapter_var,
                bg=COLORS['input_bg'], fg=COLORS['fg'],
                insertbackground=COLORS['fg']).pack(anchor="w")
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
        
        
        # 3. 수업 등록, 수업 목록, 강의 등록 버튼 3개를 한 줄에 가운데 정렬
        buttons_frame = tk.Frame(inner_frame, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.X, pady=(15, 5))

<<<<<<< HEAD
        # ➕ 새로운 수업 등록 (Lecture)
        btn_new_lecture = tk.Button(
=======
        btn1 = tk.Button(
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
            buttons_frame,
            text="➕ 새로운 수업 등록 (Lecture)",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['accent'], fg='white',
            activebackground='#005a9e',
            activeforeground='white',
            bd=0, padx=20, pady=6, cursor='hand2',
            command=self.register_lecture
        )
<<<<<<< HEAD
        btn_new_lecture.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # 📚 기존 수업 목록 보기
        btn_view_lecture = tk.Button(
=======
        btn1.pack(side=tk.LEFT, expand=True, padx=5)

        btn2 = tk.Button(
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
            buttons_frame,
            text="📚 기존 수업 목록 보기",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['button_bg'], fg=COLORS['fg'],
            activebackground=COLORS['button_hover'],
            activeforeground='white',
            bd=0, padx=20, pady=6, cursor='hand2',
            command=self.view_lecture_list
        )
<<<<<<< HEAD
        btn_view_lecture.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # ➕ 새로운 강의 등록 (Chapter)
        btn_new_chapter = tk.Button(
=======
        btn2.pack(side=tk.LEFT, expand=True, padx=5)

        btn3 = tk.Button(
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
            buttons_frame,
            text="➕ 새로운 강의 등록 (Chapter)",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['accent'], fg='white',
            activebackground='#005a9e',
            activeforeground='white',
            bd=0, padx=20, pady=6, cursor='hand2',
            command=self.register_chapter
        )
<<<<<<< HEAD
        btn_new_chapter.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # 📚 기존 강의 목록 보기
        btn_view_chapter = tk.Button(
            buttons_frame,
            text="📚 기존 강의 목록 보기",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['button_bg'], fg=COLORS['fg'],
            activebackground=COLORS['button_hover'],
            activeforeground='white',
            bd=0, padx=20, pady=6, cursor='hand2',
            command=self.open_chapter_selector 
        )
        btn_view_chapter.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Grid 균등 확장
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
=======
        btn3.pack(side=tk.LEFT, expand=True, padx=5)
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61


        
    def create_convert_button(self, parent):
        """변환 버튼"""
        button_frame = tk.Frame(parent, bg=COLORS['bg'])
        button_frame.pack(pady=(0, 15))
        
        self.convert_btn = tk.Button(button_frame,
                                    text="🚀 변환 시작",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=COLORS['accent'],
                                    fg='white',
                                    activebackground='#005a9e',
                                    activeforeground='white',
                                    bd=0,
                                    padx=40,
                                    pady=12,
                                    cursor='hand2',
                                    command=self.start_conversion)
        self.convert_btn.pack()
        
    def create_log_section(self, parent):
        """로그 출력 섹션"""
        log_frame = tk.LabelFrame(parent, 
                                 text="📋 처리 로그",
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=COLORS['bg'], 
                                 fg=COLORS['fg'],
                                 relief=tk.GROOVE,
                                 bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 스크롤 가능한 텍스트 위젯
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 height=10,
                                                 bg=COLORS['input_bg'],
                                                 fg=COLORS['fg'],
                                                 font=('Consolas', 9),
                                                 wrap=tk.WORD)
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def create_progress_section(self, parent):
        """진행 상태 바"""
        progress_frame = tk.Frame(parent, bg=COLORS['bg'])
        progress_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(progress_frame,
                                      text="대기 중...",
                                      font=('Segoe UI', 10),
                                      bg=COLORS['bg'],
                                      fg=COLORS['fg'])
        self.progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           mode='indeterminate',
                                           style='TProgressbar')
        self.progress_bar.pack(fill=tk.X)
        
    def select_input_file(self):
        """입력 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="동영상 파일 선택",
            filetypes=[
                ("동영상 파일", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            self.input_file = Path(file_path)
            self.input_label.config(text=self.input_file.name, fg=COLORS['fg'])
            
            # 출력 파일 자동 설정
            self.output_file = self.input_file.with_suffix('.txt')
            self.output_label.config(text=self.output_file.name, fg=COLORS['fg'])
            
    # def select_output_file(self):
    #     """출력 파일 선택"""
    #     if not self.input_file:
    #         messagebox.showwarning("경고", "먼저 입력 파일을 선택하세요.")
    #         return
            
    #     file_path = filedialog.asksaveasfilename(
    #         title="출력 파일 저장 위치",
    #         defaultextension=".txt",
    #         filetypes=[
    #             ("텍스트 파일", "*.txt"),
    #             ("모든 파일", "*.*")
    #         ],
    #         initialfile=self.output_file.name if self.output_file else "output.txt"
    #     )
        
    #     if file_path:
    #         self.output_file = Path(file_path)
    #         self.output_label.config(text=self.output_file.name, fg=COLORS['fg'])
            
    def log(self, message, level='info'):
        """로그 메시지 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 색상 설정
        if level == 'error':
            color = COLORS['error']
        elif level == 'success':
            color = COLORS['success']
        else:
            color = COLORS['fg']
            
        # 로그 추가
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.update()
        
    def start_conversion(self):
        """변환 시작"""
        if self.is_processing:
            messagebox.showinfo("알림", "이미 변환이 진행 중입니다.")
            return
            
        if not self.input_file:
            messagebox.showwarning("경고", "입력 파일을 선택하세요.")
            return
            
        if not self.input_file.exists():
            messagebox.showerror("오류", "선택한 파일이 존재하지 않습니다.")
            return
            
        # 설정 저장
        self.save_config()
        
        # UI 상태 변경
        self.is_processing = True
        self.convert_btn.config(state='disabled', text='⏳ 변환 중...')
        self.progress_bar.start(10)
        self.progress_label.config(text="변환 준비 중...")
        
        # 로그 초기화
        self.log_text.delete(1.0, tk.END)
        self.log(f"입력 파일: {self.input_file}")
        self.log(f"모델: {self.model_var.get()}, 언어: {self.lang_var.get()}")
        self.log("-" * 50)
        
        # 백그라운드 스레드에서 변환 실행
        self.process_thread = threading.Thread(target=self.run_conversion, daemon=True)
        self.process_thread.start()
        
    def run_conversion(self):
        """실제 변환 작업 (백그라운드 스레드)"""
        try:
            # 진행 상태 업데이트
            self.update_progress("모델 로딩 중...")
            self.log(f"Whisper 모델 로딩 중... (크기: {self.model_var.get()})")
            
            # 모델 로드
            if not self.model or self.model_var.get() != self.config.get('model'):
<<<<<<< HEAD
                #device = "cuda" if torch.cuda.is_available() else "cpu"

                # compute_type = "float16" if device == "cuda" else "int8"
                device = "cpu"
                compute_type = "int8"
=======
                device = "cuda" if torch.cuda.is_available() else "cpu"

                compute_type = "float16" if device == "cuda" else "int8"
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61

                self.model = WhisperModel(
                    self.model_var.get(),
                    device=device,
                    compute_type=compute_type
)
            
            self.update_progress("음성 인식 중... (시간이 걸릴 수 있습니다)")
            self.log("음성 인식 시작...")
            
            # 음성 인식
            language = None if self.lang_var.get() == 'auto' else self.lang_var.get()
            segments, info = self.model.transcribe(
                str(self.input_file),
                language=language,
                beam_size=5,
                vad_filter=False
            )
            
            # 감지된 언어 표시
            if self.lang_var.get() == 'auto':
                self.log(f"감지된 언어: {info.language}")
            
            self.update_progress("문장 분리 중...")
            self.log("문장 단위로 분리 중...")
            
            # 세그먼트를 문장으로 분리
            all_sentences = []
            for segment in segments:
                sentences = self.split_segment_by_sentences(
                    segment, 
                    info.language if self.lang_var.get() == 'auto' else self.lang_var.get()
                )
                all_sentences.extend(sentences)
            
            self.update_progress("백엔드 서버로 전송 중...")
            success = self.send_to_backend(all_sentences)

            if success:
                self.log("백엔드 저장 성공!", 'success')
            else:
                self.log("백엔드 저장 실패!", 'error')
            
            # 완료
            self.log(f"변환 완료!", 'success')
            self.update_progress("변환 완료!")
            
            # 완료 알림
            self.root.after(0, lambda: messagebox.showinfo(
                "완료", 
                f"변환이 완료되었습니다!\n\n"
            ))
            
        except Exception as e:
            self.log(f"오류 발생: {str(e)}", 'error')
            self.root.after(0, lambda: messagebox.showerror(
                "오류", 
                f"변환 중 오류가 발생했습니다:\n{str(e)}"
            ))
            
        finally:
            # UI 상태 복구
            self.is_processing = False
            self.root.after(0, self.reset_ui)
            
    def split_segment_by_sentences(self, segment, language):
        """세그먼트를 문장 단위로 분할"""
        start = segment.start
        end = segment.end
        text = segment.text.strip()
        duration = end - start
        
        if not text or duration <= 0:
            return []
        
        MIN_DURATION = 7.0
        if duration < MIN_DURATION:
            return [{"start": start, "end": end, "text": text}]
        
        sentences = self.split_sentences(text, language)
        
        if len(sentences) <= 1:
            return [{"start": start, "end": end, "text": text}]
        
        # 문장 길이 비율로 시간 배분
        char_counts = [len(s.replace(" ", "")) for s in sentences]
        total_chars = sum(char_counts)
        
        if total_chars == 0:
            total_chars = len(sentences)
            char_counts = [1] * len(sentences)
        
        result = []
        current_time = start
        
        for i, sentence in enumerate(sentences):
            if i == len(sentences) - 1:
                sentence_end = end
            else:
                ratio = char_counts[i] / total_chars
                sentence_duration = duration * ratio
                sentence_end = current_time + sentence_duration
            
            result.append({
                "start": current_time,
                "end": sentence_end,
                "text": sentence
            })
            current_time = sentence_end
        
        return result
        
    def split_sentences(self, text, language):
        """텍스트를 문장 단위로 분리"""
        text = text.strip()
        if not text:
            return []
        
        if language == "ko":
            # 한국어는 kss 사용
            sentences = kss.split_sentences(text)
            return [s.strip() for s in sentences if s.strip()]
        else:
            # 영어 및 기타 언어
            sentences = re.split(r'(?<=[\.!?])\s+', text)
            return [s.strip() for s in sentences if s.strip()]
        
    def format_time(self, seconds):
        """시간을 [HH:MM:SS,mmm] 형식으로 변환"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        
    def update_progress(self, message):
        """진행 상태 업데이트"""
        self.root.after(0, lambda: self.progress_label.config(text=message))
        
    def reset_ui(self):
        """UI 상태 초기화"""
        self.convert_btn.config(state='normal', text='🚀 변환 시작')
        self.progress_bar.stop()
        self.progress_label.config(text="대기 중...")
        
    def load_config(self):
        """설정 불러오기"""
        self.config = {
            'model': 'base',
            'language': 'ko'
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except:
            pass
            
    def save_config(self):
        """설정 저장"""
        self.config = {
            'model': self.model_var.get(),
            'language': self.lang_var.get()
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except:
            pass
            
    def on_closing(self):
        """프로그램 종료"""
        if self.is_processing:
            if messagebox.askokcancel("종료", "변환이 진행 중입니다. 정말 종료하시겠습니까?"):
                self.root.destroy()
                sys.exit()
        else:
            self.root.destroy()

    def register_chapter(self):
<<<<<<< HEAD
        """새로운 챕터 등록 (Lecture ID 숨김 + UI 개선)"""

        # 팝업 생성
        popup, L, E, B = self.create_dark_popup("새로운 챕터 등록", "450x420")

        popup.configure(padx=20, pady=20)

        # 내부적으로 저장할 lecture_id 변수
        selected_lecture_id = {"id": None}
        selected_lecture_title = tk.StringVar(value="선택된 강의 없음")

        # ─────────────────────
        # 강의 선택 영역
        # ─────────────────────
        L("Lecture 선택").pack(anchor="w")

        top_frame = tk.Frame(popup, bg=COLORS['bg'])
        top_frame.pack(fill="x", pady=(5, 15))

        lecture_label = tk.Label(
            top_frame,
            textvariable=selected_lecture_title,
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            anchor="w",
            padx=10, pady=8,
            width=30
        )
        lecture_label.pack(side=tk.LEFT, fill="x", expand=True)

        def open_lecture_selector():
            """Lecture 선택 팝업"""
            select_popup, L2, E2, B2 = self.create_dark_popup("강의 선택", "420x400")

            L2("🔎 강의 검색").pack(pady=(10, 5))
            search_entry = E2()
            search_entry.pack(fill=tk.X, padx=10, pady=(0, 10))

            frame = tk.Frame(select_popup, bg=COLORS['bg'])
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(
                frame,
                bg=COLORS['input_bg'], fg=COLORS['fg'],
                selectbackground=COLORS['accent'],
                selectforeground="white",
                font=("Segoe UI", 10),
                yscrollcommand=scrollbar.set
            )
            listbox.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)

            try:
                response = requests.get("https://13-209-30-220.nip.io/api/lectures", timeout=10)
                lectures = response.json()
            except Exception as e:
                messagebox.showerror("오류", f"서버 오류: {e}")
                select_popup.destroy()
                return

            def render(items):
                listbox.delete(0, tk.END)
                for lec in items:
                    listbox.insert(tk.END, f"{lec['title']}  (ID:{lec['lectureId']})")

            render(lectures)

            def on_search(event=None):
                key = search_entry.get().lower()
                filtered = [lec for lec in lectures if key in lec["title"].lower()]
                render(filtered)

            search_entry.bind("<KeyRelease>", on_search)

            def select():
                try:
                    idx = listbox.curselection()[0]
                    entry = listbox.get(idx)
                    title = entry.split("(ID:")[0].strip()
                    lecture_id = int(entry.split("(ID:")[1].replace(")", ""))

                    selected_lecture_title.set(title)
                    selected_lecture_id["id"] = lecture_id

                    self.lecture_var.set(str(lecture_id))
                    self.lecture_title_var.set(title)
                    select_popup.destroy()
                except:
                    messagebox.showwarning("선택 오류", "강의를 선택하세요.")

            B2("선택하기", select).pack(pady=10)

        tk.Button(
            top_frame,
            text="📚 선택",
            command=open_lecture_selector,
            font=('Segoe UI', 10),
            bg=COLORS['button_bg'], fg=COLORS['fg'],
            activebackground=COLORS['button_hover'],
            activeforeground='white',
            bd=0, padx=15, pady=6, cursor='hand2'
        ).pack(side=tk.RIGHT, padx=(10, 0))

        # ─────────────────────
        # 제목 / order / URL 입력
        # ─────────────────────
        L("챕터 제목").pack(anchor="w")
        entry_title = E()
        entry_title.pack(fill="x", pady=(0, 15))

        L("몇 번째 강의인가요? (숫자만 입력)").pack(anchor="w")
        entry_order = E()
        entry_order.pack(fill="x", pady=(0, 15))

        L("영상 URL").pack(anchor="w")
        entry_url = E()
        entry_url.pack(fill="x", pady=(0, 20))

        # ─────────────────────
        # 등록 버튼
        # ─────────────────────
        def submit():
            if selected_lecture_id["id"] is None:
                messagebox.showerror("입력 오류", "Lecture를 선택해주세요.")
                return

            title = entry_title.get().strip()
            order = entry_order.get().strip()
            url = entry_url.get().strip()

            if not title:
                messagebox.showerror("입력 오류", "챕터 제목은 필수입니다.")
                return
            if not order.isdigit():
                messagebox.showerror("입력 오류", "order_index는 숫자여야 합니다.")
                return

            payload = {
                "lectureId": selected_lecture_id["id"],
                "title": title,
                "orderIndex": int(order),
                "url": url or None,
                "duration": None
=======
        """새로운 챕터 등록"""
        popup, L, E, B = self.create_dark_popup("새로운 챕터 등록", "350x360")

        L("Lecture ID (정수)").pack(pady=(10,0))
        entry_lecture_id = E()
        entry_lecture_id.pack(pady=(0,10))

        L("챕터 제목").pack()
        entry_title = E()
        entry_title.pack(pady=(0,10))

        L("order_index (몇 강인지)").pack()
        entry_order = E()
        entry_order.pack(pady=(0,10))

        L("영상 URL (선택)").pack()
        entry_url = E()
        entry_url.pack(pady=(0,10))

        L("영상 길이 (초 단위, 선택)").pack()
        entry_duration = E()
        entry_duration.pack(pady=(0,10))

        def submit_chapter():
            lecture_id_str = entry_lecture_id.get().strip()
            title = entry_title.get().strip()
            order_str = entry_order.get().strip()
            url = entry_url.get().strip()
            duration_str = entry_duration.get().strip()

            # 기본 검증
            if not lecture_id_str.isdigit():
                messagebox.showerror("입력 오류", "Lecture ID는 정수여야 합니다.")
                return
            if not title:
                messagebox.showerror("입력 오류", "챕터 제목은 필수입니다.")
                return
            if not order_str.isdigit():
                messagebox.showerror("입력 오류", "order_index는 정수여야 합니다.")
                return

            lecture_id = int(lecture_id_str)

            payload = {
                "lectureId": lecture_id,
                "title": title,
                "orderIndex": int(order_str),
                "url": url or None,
                "duration": float(duration_str) if duration_str else None
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
            }

            try:
                response = requests.post(
                    "https://13-209-30-220.nip.io/api/chapters",
                    json=payload,
                    timeout=10
                )
<<<<<<< HEAD
                data = response.json()
                if response.status_code == 200:
                    chapter_id = data.get("chapterId")
                    self.chapter_var.set(str(chapter_id))
                    # messagebox.showinfo("성공", f"챕터 등록 완료!\nChapter ID = {chapter_id}")
                    popup.destroy()
                else:
                    messagebox.showerror("오류", response.text)
            except Exception as e:
                messagebox.showerror("오류", str(e))

        B("등록하기", submit).pack(pady=10)

    def open_chapter_selector(self, parent_popup=None):
        """기존 Chapter 선택 팝업"""

        popup, L, E, B = self.create_dark_popup("기존 챕터 선택", "420x400")

        L("🔎 챕터 검색").pack(pady=(10, 5))
        search_entry = E()
        search_entry.pack(fill=tk.X, padx=10, pady=(0, 10))

        frame = tk.Frame(popup, bg=COLORS['bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            frame,
            bg=COLORS['input_bg'], fg=COLORS['fg'],
            selectbackground=COLORS['accent'],
            selectforeground="white",
            font=("Segoe UI", 10),
            yscrollcommand=scrollbar.set
        )
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # 서버에서 Chapter 목록 fetch
        try:
            response = requests.get("https://13-209-30-220.nip.io/api/chapters", timeout=10)
            chapters = response.json()
            chapters = sorted(chapters, key=lambda x: x["chapterId"])
        except Exception as e:
            messagebox.showerror("오류", f"서버 오류: {e}")
            popup.destroy()
            return

        # 렌더링
        def render(items):
            listbox.delete(0, tk.END)
            for ch in items:
                listbox.insert(tk.END, f"[{ch['chapterId']}] {ch['title']}")

        render(chapters)

        # 검색 기능
        def on_search(event=None):
            key = search_entry.get().lower()
            filtered = [ch for ch in chapters if key in ch["title"].lower()]
            render(filtered)

        search_entry.bind("<KeyRelease>", on_search)

        # 선택 처리
        def select():
            try:
                idx = listbox.curselection()[0]
                text = listbox.get(idx)

                chapter_id = int(text.split("]")[0].replace("[", ""))
                chapter_title = text.split("]")[1].strip()

                # UI 변수 갱신
                self.chapter_var.set(str(chapter_id))
                self.chapter_title_var.set(chapter_title)

                popup.destroy()

                if parent_popup:
                    parent_popup.destroy()

                # messagebox.showinfo("선택 완료", f"기존 챕터 선택됨:\nID={chapter_id}\n제목={chapter_title}")

            except:
                messagebox.showwarning("선택 오류", "챕터를 선택하세요.")

        B("선택하기", select).pack(pady=10)

        



=======
                if response.status_code == 200:
                    data = response.json()
                    chapter_id = data.get("chapterId")

                    if chapter_id:
                        # UI 메인 입력창에도 Chapter ID 넣어주기
                        self.chapter_var.set(str(chapter_id))

                    messagebox.showinfo("성공", f"챕터 등록 완료!\nChapter ID = {chapter_id}")
                    popup.destroy()
                else:
                    messagebox.showerror("오류", f"등록 실패\n{response.text}")
            except Exception as e:
                messagebox.showerror("오류", f"예외 발생: {e}")

        tk.Button(popup, text="등록", command=submit_chapter).pack(pady=10)
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61

    def view_lecture_list(self):
        """기존 Lecture 목록 조회 팝업"""
        
        # 팝업 생성 (dark theme)
        popup, L, E, B = self.create_dark_popup("기존 강의 목록", "420x400")

<<<<<<< HEAD
        L("🔎 수업 검색").pack(pady=(10,5))
=======
        L("🔎 강의 검색").pack(pady=(10,5))
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
        search_entry = E()
        search_entry.pack(fill=tk.X, padx=10, pady=(0,10))

        # Listbox + Scrollbar
        frame = tk.Frame(popup, bg=COLORS['bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            frame,
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            font=("Segoe UI", 10),
            yscrollcommand=scrollbar.set
        )
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # 1) 서버에서 Lecture 목록 fetch
        try:
            response = requests.get("https://13-209-30-220.nip.io/api/lectures", timeout=10)
            lectures = response.json()
<<<<<<< HEAD
            lectures = sorted(lectures, key=lambda x: x["lectureId"])
=======
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
        except Exception as e:
            messagebox.showerror("오류", f"서버 통신 오류: {e}")
            popup.destroy()
            return

        # 원본 목록 보관
        self._lecture_list_cache = lectures

        # 2) Listbox에 내용 채우기
        def render_list(items):
            listbox.delete(0, tk.END)
            for lec in items:
                line = f"[{lec['lectureId']}] {lec['title']}"
                listbox.insert(tk.END, line)

        render_list(lectures)

        # 검색 기능
        def on_search(*args):
            keyword = search_entry.get().strip()
            if not keyword:
                render_list(lectures)
                return
            filtered = [
                lec for lec in lectures
                if keyword.lower() in lec["title"].lower()
            ]
            render_list(filtered)

        search_entry.bind("<KeyRelease>", on_search)

        # 선택 처리
        def select_item():
            try:
                index = listbox.curselection()[0]
                text = listbox.get(index)
                # "[3] 강의 제목" 형태 → ID만 추출
                lecture_id = int(text.split("]")[0].replace("[", ""))
<<<<<<< HEAD
                lecture_title = text.split("]")[1].strip()
                self.lecture_var.set(str(lecture_id))
                self.lecture_title_var.set(lecture_title)
=======
                self.lecture_var.set(str(lecture_id))
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61
                popup.destroy()
            except:
                messagebox.showwarning("선택 오류", "먼저 항목을 선택하세요.")

        B("선택하기", select_item).pack(pady=10)


    def register_lecture(self):
        """새로운 수업 등록"""
        # 팝업창 열기
        popup, L, E, B = self.create_dark_popup("새로운 강의 등록", "350x250")

        L("강의 제목 (필수)").pack(pady=(10,0))
        entry_title = E()
        entry_title.pack(pady=(0,10))

        L("강의 설명 (선택)").pack()
        entry_desc = E()
        entry_desc.pack(pady=(0,10))

        def submit_lecture():
            title = entry_title.get().strip()
            desc = entry_desc.get().strip()

            if not title:
                messagebox.showerror("입력 오류", "강의 제목은 필수입니다.")
                return

            payload = {
                "title": title,
                "description": desc
            }

            try:
                response = requests.post(
                    "https://13-209-30-220.nip.io/api/lectures/create",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()

                    generated_id = data.get("lectureId")  # 백엔드가 자동 생성한 ID

                    if generated_id is None:
                        messagebox.showerror("오류", "백엔드가 lectureId를 반환하지 않았습니다.")
                        return

                    # UI의 Lecture 입력칸에 자동 입력
                    self.lecture_var.set(str(generated_id))
<<<<<<< HEAD
                    self.lecture_title_var.set(title)

                    # messagebox.showinfo(
                    #     "성공",
                    #     f"강의 등록 완료!\nLecture ID = {generated_id}"
                    # )
=======

                    messagebox.showinfo(
                        "성공",
                        f"강의 등록 완료!\nLecture ID = {generated_id}"
                    )
>>>>>>> b46c109ba43801b21a0ba7af5db9cf02b3eddb61

                    popup.destroy()

                else:
                    messagebox.showerror("오류", f"등록 실패\n{response.text}")

            except Exception as e:
                messagebox.showerror("오류", f"예외 발생: {e}")

        tk.Button(popup, text="등록", command=submit_lecture).pack(pady=10)


    
    def send_to_backend(self, all_sentences):
        lecture_str = self.lecture_var.get().strip()
        chapter_str = self.chapter_var.get().strip()

        if not lecture_str.isdigit():
            self.log("Lecture ID가 비어있거나 숫자가 아닙니다.", level="error")
            return False
        if not chapter_str.isdigit():
            self.log("Chapter ID가 비어있거나 숫자가 아닙니다.", level="error")
            return False

        lecture_id = int(lecture_str)
        chapter_id = int(chapter_str)

        payload = {
            "lectureId": lecture_id,
            "chapterId": chapter_id,
            "transcripts": [
                {
                    "startTime": f"[{self.format_time(s['start'])}]",
                    "content": s["text"]
                }
                for s in all_sentences
            ]
        }

        try:
            url = "https://13-209-30-220.nip.io/api/transcripts/upload/json"
            self.log("백엔드로 업로드 중...")

            response = requests.post(url, json=payload, timeout=30)

            if response.status_code == 200:
                self.log("전송 성공!", level="success")
                return True
            else:
                self.log(f"전송 실패: {response.status_code} {response.text}", level="error")
                return False

        except Exception as e:
            self.log(f"전송 에러: {str(e)}", level="error")
            return False

    
            

def main():
    """메인 함수"""
    root = tk.Tk()
    app = WhisperGUI(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()