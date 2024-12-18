# CineSeed(독립영화 추천 플랫폼)

# 목차
- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [주요 기술](#주요-기술)
- [이슈 사항](#이슈-사항)
- [프로젝트 산출물](#프로젝트-산출물)
- [기타(느낀 점, 후기 등)](#기타느낀-점-후기-등)

# 프로젝트 개요

### 진행 기간
SSAFY 12기 1학기 관통 프로젝트

2024.11.18 ~ 2024.11.27 (10일간 진행)

### 기획 의도
CineSeed는 영화 산업의 회복을 위해 새로운 감독들이 양질의 영화를 제작할 수 있도록 돕는 플랫폼입니다.
대중들에게 자신의 독립영화를 소개하고 대형 제작사를 통하지 않고도 필요한 자금 또는 인력을 펀딩 형태로 조달하여 영화의 퀄리티를 높일 수 있습니다.

### 팀 구성 및 역할 분담
- 최현우(팀장)
  - 서비스 기획
  - ERD 설계
  - 유저 관련 기능 개발
  - 영화 관련 CRUD 구현(+좋아요 기능)
  - 펀딩 기능 개발
  - 서비스에 필요한 데이터 수집 및 DB 구축
  - 프로젝트 발표

- 김나현(팀원)
  - 서비스 기획
  - ERD 설계
  - 와이어프레임 제작
  - 서비스 디자인(웹 페이지, 로고)
  - 영화 취향 토너먼트 게임 개발
  - 영화 추천 기능 구현

# 주요 기능
### 1. 영화 등록 및 조회
- 감독으로 가입한 유저는 자신의 영화를 펀딩 등록할 수 있습니다.
- 유저는 펀딩 등록된 영화를 조회할 수 있고 자신이 좋아하는 영화, 펀딩한 영화, 크루로 지원한 영화를 마이페이지에서 모아서 볼 수 있습니다.

### 2. 펀딩
- 유저는 갖고 있는 금액 내에서 펀딩 등록된 영화에 원하는 금액만큼 펀딩할 수 있습니다.

### 3. 크루로 지원
- 해당 영화를 등록한 감독이 크루를 모집하고 있다면 유저는 해당 영화에 크루로 지원할 수 있습니다.

### 3. 영화 취향 토너먼트 게임
- 영화를 볼 때 나의 성향 테스트, 취향에 가까운 영화 고르기 게임을 통해 자신의 영화 취향을 알 수 있습니다.
- 유저는 게임 진행 후 게임 결과에 따라 취향에 가까운 영화를 추천 받을 수 있습니다.

## 서비스 화면
### 영화 등록 및 조회
<img src="https://github.com/user-attachments/assets/04d0dcf4-edec-4270-9fab-c34a2635be3f" alt="영화 등록하기" width="500" />

<br>
<img src="https://github.com/user-attachments/assets/08d3a1b1-03ee-4c8a-b96e-c38bf5546f39" alt="영화 목록" width="500" />

<b>마이페이지</b>
<br>
<img src="https://github.com/user-attachments/assets/f2205384-e841-4962-a24f-751148f5720d" alt="마이페이지" width="500" />

### 펀딩 및 크루로 지원
<b>영화 상세페이지</b>
<br>
<img src="https://github.com/user-attachments/assets/ed6ae099-a89e-4175-9f66-fe0fd7bfd0fd" alt="영화 상세페이지" width="500" />

### 영화 취향 토너먼트 게임
|<img src="https://github.com/user-attachments/assets/78679394-2d54-4027-a339-cf012d33b33d" alt="영화 취향 게임 이미지 1" width="400" /> | <img src="https://github.com/user-attachments/assets/86dd9a3b-7d3e-4c00-91ea-2191b83d3687" alt="영화 취향 게임 이미지 2" width="400" />|
|---|---|

# 주요 기술
<b>FrontEnd</b>
- Vue 5.2.0
- Axios 1.7.7

<b>BackEnd</b>
- Python: Django 4.2.16
- DjangoRestframework 3.15.2
- MySQL

<b>협업툴</b>
- 형상 관리: Git
- 커뮤니케이션: Notion
- 디자인: Figma

# 이슈 사항
### ERD 설계
#### ERD1
모든 것을 M:N 관계로 엮은 후 참조/역참조 매니저를 통해 데이터를 조회 <br>
--> 데이터를 조회하기 위해 너무 많은 단계를 거쳐서 비효율적이라고 판단

#### ERD2
필요 없다고 생각되는 관계를 모두 삭제하여 ERD 단순화 <br>
--> 필요한 데이터를 조회할 수 없는 상황 발생

#### ERD3
이전으로 되돌려 필요한 데이터를 모두 조회할 수 있게 M:N 관계 설정 <br>
누락된 게임 관련 데이터 테이블 추가 <br>
--> 장르 테이블에서 데이터를 조회한 후 출력할 때 복잡함 이슈 발생

#### ERD 최종
가장 문제였던 장르 데이터를 가공하여 테이블 생성 (여러 형태로 기록되던 데이터를 하나의 기준으로 통합)

|<img src="https://github.com/user-attachments/assets/4a7a0998-1b1a-40ed-9f0b-32cf695a0588" alt="ERD 1" width="250" height="100"/> <br> ERD 1|<img src="https://github.com/user-attachments/assets/c4b6c196-0e0b-4c5c-856c-dd6ded19df4d" alt="ERD 1" width="250" height="100"/> <br> ERD 2|<img src="https://github.com/user-attachments/assets/c4196448-d253-408b-92ca-f8450bae39f4" alt="ERD 1" width="250" height="100"/> <br> ERD 3|
|---|---|---|

<img src="https://github.com/user-attachments/assets/4a7a0998-1b1a-40ed-9f0b-32cf695a0588" alt="ERD 1"/><br> <b>ERD 최종</b>

# 프로젝트 산출물

# 기타(느낀 점, 후기 등)