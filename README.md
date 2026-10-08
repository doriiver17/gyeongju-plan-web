# 수성구청 경주 현장체험 계획서 만들기

교육생이 내용을 입력하면 제공된 수정 양식에 텍스트를 배치해 A4 한 장 PDF를 다운로드합니다.
현재 버전은 계획서 전용입니다.

## 반영한 기준

- 수정된 원본 PDF 배경 유지
- 조 번호: Pretendard ExtraBold 40pt, 1~99
- 나머지 입력 글자: Pretendard Medium
- 조원 이름: 왼쪽 정렬, 쉼표로 구분, 최대 8명
- 역할: 팀장 / 일정 관리 / 예산 관리 / 사진 촬영 / 인사이트 기록 2명 / 보고서 작성 2명
- 인사이트 기록과 보고서 작성의 두 번째 담당자는 선택 입력
- 컨셉: 5개 중 한 개 이상 복수 선택
- 일정: 중식 / 방문지(1) / 방문지(2)
- 활동 계획: 항목별 공백 포함 60자, 남은 글자수 표시
- 자동 줄바꿈 및 칸 크기 검사: 내용을 몰래 잘라내지 않고, 배치 불가 시 안내
- 파일명: 현장체험계획서_15조_집에언제보내주조.pdf
- 카카오톡 인앱 브라우저 안내 및 주소 복사
- 입력 내용은 서버 파일이나 데이터베이스에 저장하지 않음

60자보다 긴 검증 예시는 이 버전의 입력 제한으로 제출할 수 없습니다. 제한을 변경할 때는 pdf_builder.py의 ACTIVITY_LIMIT을 수정하면 웹 화면과 서버 검증에 함께 적용됩니다. 최종 PDF 칸 크기 검사는 계속 적용됩니다.

## 파일 구성

- app.py: 입력 검증 및 다운로드 API
- pdf_builder.py: 확정 좌표와 PDF 배치
- templates/index.html: 입력 화면
- static/style.css, static/app.js: 모바일 스타일과 다운로드/글자수 표시
- assets/plan_template.pdf: 수정 원본 서식
- assets/fonts/: Pretendard Medium, ExtraBold 및 OFL 라이선스
- requirements.txt: 설치할 패키지
- render.yaml: Render 배포 설정

## GitHub 업로드 (웹 브라우저)

1. ZIP을 다운로드하고 압축을 풉니다.
2. https://github.com/new 에서 새 저장소를 만듭니다. 이름 예: gyeongju-plan-web.
3. README 추가 옵션을 켜고 Create repository를 누릅니다.
4. 저장소에서 Add file → Upload files를 선택합니다.
5. 압축을 푼 gyeongju-plan-web 폴더를 열고, 그 안의 파일과 assets/templates/static 폴더를 모두 드래그합니다. 바깥 gyeongju-plan-web 폴더 자체나 ZIP 파일을 업로드하지 마세요.
6. Commit changes를 누릅니다.
7. 저장소 첫 화면에서 app.py, pdf_builder.py, requirements.txt, render.yaml이 바로 보이는지 확인합니다. assets/fonts 안의 글꼴과 assets/plan_template.pdf도 확인합니다.

.gitignore 파일은 Windows에서 숨겨져 보일 수 있습니다. 누락되면 GitHub에서 Add file → Create new file로 .gitignore를 만들고 다음 내용을 넣으면 됩니다:

```text
.venv/
__pycache__/
*.pyc
.env
```

## Render에서 웹사이트 실행

GitHub 업로드는 코드 저장입니다. 교육생이 접속할 주소는 Render에서 배포해 만듭니다.

1. Render에 로그인합니다.
2. New → Web Service를 선택합니다.
3. GitHub를 연결하고 위 저장소를 선택합니다.
4. 설정을 아래와 같이 입력합니다.

| 항목 | 값 |
|---|---|
| Language / Runtime | Python |
| Branch | main |
| Root Directory | 비워 둠 |
| Build Command | pip install -r requirements.txt |
| Start Command | gunicorn --workers 1 --threads 1 --timeout 60 --bind 0.0.0.0:$PORT app:app |
| 환경변수 PYTHON_VERSION | 3.12.10 |

5. 원하는 인스턴스 요금제를 선택하고 배포합니다.
6. Live 상태가 되면 표시되는 https://…onrender.com 주소에 접속합니다.
7. 내용을 입력해 PDF를 생성하고, 파일명·한글·체크 표시·조원 이름 왼쪽 정렬을 확인합니다.

render.yaml은 Blueprint 배포용 설정입니다. Web Service를 수동으로 만들 때는 위 표를 직접 입력합니다.

## PC에서 먼저 실행 (Windows)

Python 3.12를 설치한 PC에서 압축을 푼 프로젝트 폴더의 터미널을 열고 실행합니다.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Chrome에서 http://127.0.0.1:5000 에 접속합니다. 종료는 터미널에서 Ctrl+C입니다.

## 배포 시 주의

PyMuPDF는 AGPL/상용 라이선스 체계를 사용합니다. 배포자는 사용 조건을 확인해야 합니다. 포함한 Pretendard 글꼴은 SIL Open Font License이며 원문을 assets/fonts/OFL.txt에 포함했습니다.
PDF 처리는 요청마다 메모리에서 수행합니다. Gunicorn은 PyMuPDF의 다중 스레드 동시 사용을 피하도록 threads=1로 설정했습니다.
