# Container Build Management Mastering Program

## 라이브러리 

해당 프로그램을 구동하기 위해서 필요한 라이브러리는 아래와 같다.

- uvicorn[standard] == 0.22.0 # FastAPI 비동기 구동 라이브러리
- FastAPI == 0.95.1 # FastAPI 라이브러리
- docker == 6.1.3 # Docker SDK 라이브러리
- python-dotenv = 1.0.0 # env 해석 라이브러리
- torch == 2.0.1 # GPU 확인용 파이토치

<br><br>

## 디랙토리

해당 프로그램이 구성되어있는 파일, 디랙토리 형식은 아래와 같이 구성되어있다.

<br>

```
.container-build-management-mastering-program
│
├── Log
│   └── README.md
├── README.md
├── SQL
│   ├── SQL.sqlite
│   └── SetupSQL.sql
├── Setting
│   ├── Error.json
│   ├── README.md
│   └── Setting.json
├── dockerfile
├── jsonset.py
├── main.py
├── requirements.txt
├── src
│   ├── Container
│   │   ├── build
│   │   │   ├── __init__.py
│   │   │   ├── databases.py
│   │   │   ├── jupyter.py
│   │   │   └── ssh.py
│   │   ├── delete
│   │   │   ├── __init__.py
│   │   │   └── delete.py
│   │   └── search
│   │       ├── __init__.py
│   │       └── info.py
│   ├── error.py
│   └── set.py
└── test
    ├── test.ipynb
    └── test.py

9 directories, 23 files
```

<br><br>

### 디랙토리 설명

- Log: 시스템적 이슈가 발생시 저장되는 디랙토리

- SQL: SQLite에 필요한 파일 및 디랙토리

- Setting: 시스템을 구동하기 위한 기초적인 셋업 디랙토리

- src/Container/build: 프로젝트 컨테이너 배포 디랙토리

- src/Container/delete: 프로젝트 컨테이너 삭제 디랙토리

- src/Container/search: 프로젝트 컨테이너 정보 출력 디랙토리