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
### 1. ERD 설계
#### ERD1
모든 것을 M:N 관계로 엮은 후 참조/역참조 매니저를 통해 데이터를 조회 <br>
--> 특정 데이터를 조회하기 위해 serializer가 너무 복잡해짐

#### ERD2
필요 없다고 생각되는 관계를 모두 삭제하여 ERD 단순화 <br>
--> 장르 테이블을 삭제하고 pinia에 저장하여 해결하려 했지만 속도 측면에서 비효율적이라고 판단

#### ERD3
누락된 게임 관련 데이터 테이블 추가 <br>
장르 테이블을 다시 만들고 기존 테이블과 M:N 관계 설정  <br>
--> 장르 테이블에서 데이터를 조회한 후 출력할 때 serializer가 복잡해지는 이슈 다시 발생

#### ERD 최종
가장 문제였던 장르 데이터를 넣을 때 하나의 기준으로 전처리하여 저장-> 핵심 데이터만 db에 저장하고 활용 <br>
--> ERD 설계 시 모든 것을 관계로 설정하지 말고 가공한 데이터를 저장하여 사용하는 방법도 고려해야 함


|<img src="https://github.com/user-attachments/assets/4a7a0998-1b1a-40ed-9f0b-32cf695a0588" alt="ERD 1" width="250" height="100"/> <br> ERD 1|<img src="https://github.com/user-attachments/assets/c4b6c196-0e0b-4c5c-856c-dd6ded19df4d" alt="ERD 1" width="250" height="100"/> <br> ERD 2|<img src="https://github.com/user-attachments/assets/c4196448-d253-408b-92ca-f8450bae39f4" alt="ERD 1" width="250" height="100"/> <br> ERD 3|
|---|---|---|

<img src="https://github.com/user-attachments/assets/4a7a0998-1b1a-40ed-9f0b-32cf695a0588" alt="ERD 1"/><br> <b>ERD 최종</b>

### 2. Django 유저 모델 커스텀
1. User registeration 커스텀 오류
- dj-rest-auth를 사용했을 때 migration 단계에서 오류
  - dj-rest-auth[with-social]을 사용해 오류 해결
- 유저 데이터를 입력 받을 필드를 추가할 때 오류 발생
  - django가 기본적으로 받는 필드를 고려하지 않고 코드를 작성하여 오류 발생 -> 기본 필드를 그대로 활용하고 사용자에게는 노출시키지 않는 방식으로 작성
- 커스텀할 수 있는 방향이 다양한데 전달받은 가이드의 방식 중 커스텀하는 과정에서 오류 발생 -> 나만의 방식으로 코드 작성해서 오류 해결
  - 강사님 방식: 커스텀한 유저 등록 방식 -> 커스텀한 어댑터 사용 -> 저장
  - 나의 방식: 유저 등록과 동시에 저장(어댑터를 커스텀하지 않아도 됨)


# 프로젝트 산출물
- [정보구조도](https://www.notion.so/isaacshin/8eb897ee327c4b86ad4060ffb9fe5d24?pvs=4)
- [요구사항 명세서](https://www.notion.so/isaacshin/a26ffc37e62d4c4c85dce7c84ba70650?pvs=4)

# 기타(느낀 점, 후기 등)
## 최현우
- 서비스 기획과 기초 설계가 중요하다는 것을 다시 한 번 깨닫게 됨.
  - 정보구조도, 요구사항 명세서, 와이어프레임, ERD 등 미리 설계를 하고 프로젝트에 들어갔지만 중간중간 놓친 부분이 많았음. 완벽하게 설계를 했다면 훨씬 더 수월하고 빠르게 프로젝트가 진행됐을 것 같음. 앞으로 초기 설계를 더 정교하게 할 수 있도록 기획과 기초 설계 단계에 대한 공부를 할 예정임.
- 서버에서 데이터를 받고 보내주는 과정을 많이 배웠음.
  - django의 serializer를 다양하게 활용하는 방법을 검색하여 찾아보고 적용하는 과정에서 서버에서 데이터를 어떤 식으로 가공하여 전달하는 것이 가장 좋은 방법인지 고민할 수 있는 기회를 갖게 됨. 그와 동시에 DB를 효율적으로 설계하는 게 얼마나 중요한 지를 알게 됨.
- 사용자의 입장에서 웹사이트의 사용성을 검증하는 것의 중요성을 깨달음.
  - 사용자의 입장에서 이 상황에 어떤 경로로 가는 것이 가장 편하고 어떤 버튼이 필요한지 고려하면서 제작했지만 중간중간 테스트하면서 놓친 부분이 많았음. 안 그러려고 노력했지만 은연 중에 개발자 입장에서 간단한 방식으로 제작한 부분이 많았음. 기능 개발 후에 꼭 테스트를 통해 사용자 입장에서 어떤 부분이 불편한지 거듭 테스트를 거쳐야 함을 깨닫게 됨.

## 김나현
- 기획 문서 중요성을 느낌
    - 나름 초기 설계를 꼼꼼히 했다고 생각하고 시작했는데, 하다 보니 추가할 것이 계속 생겨났음. 기획할 때 사용자 입장에서 Journey Map을 생각해 보는 것이 필요한 단계라고 느끼게 됨. 특히, ERD를 수정하는 단계를 여러번 거치면서 데이터베이스에 관한 공부가 더 필요하다고 느낌. 앞으로 프로젝트를 더 많이 수행해 보면서 프로젝트 문서 작성에 대한 경험치를 키울 예정임.
- 와이어 프레임을 구체적으로 만들어 놓는 것이 많은 도움이 된다는 것을 느낌
    - 와이어 프레임을 그려놓고 백엔드 개발을 시작하였음. 와이어프레임이 있으니, 정보구조도, 요구사항 명세서 등 문서를 작성하기가 수월하였고, 이후 프론트엔드 작업을 할 때에도 component 구분을 하기 편했음.
- 각자 작업 상황에 공유를 많이 하여 도움이 되었음.
    - 이번 프로젝트에서는 프론트엔드, 백엔드 구분 없이 기능별로 나누어서 작업하였음. 이때, 각자 작업을 시작하기 전 어떤 작업을 할지, 또 작업이 끝나고 어떤 작업을 했는지 공유하고 데일리 스크럼을 작성해 오늘 작업 시 발생한 문제와 해결 방법을 정리하였음. 이렇게 작업에 대해 많이 공유함으로써 팀원이 한 부분에 대한 이해가 생겼고, 프로젝트 전반적으로 어떻게 진행되고 있는지 알 수 있어서 좋았음. 또한, 팀원이 미리 겪은 문제와 해결 방법을 보았기에 나에게 그런 문제가 생겼을 때 대처하기 수월하였고, 내가 겪지 않은 문제에 대해서 어떻게 해결했는지 볼 수 있어서 도움이 되었음.
- 개발 프로젝트에서 스케줄 관리 및 노션 활용 방법을 배우게 되었음.
    - 노션을 활용하여 스케줄 관리 및 협업을 하였음. 직접 노션 템플릿을 만들어서 활용하였음. 노션을 사용하니 스케줄 관리가 수월하게 되어 팀원으로서 팀에 생산성에 기여할 수 있어서 뿌듯했음.
- 좋은 팀장과 함께 좋은 프로젝트!
    - 그동안 다양한 분야의 프로젝트를 하며 팀장을 한 경우가 대부분이어서 이번 프로젝트에서는 좋은 팀원의 역할을 배우고자 하였음. 팀장이 팀원의 의견을 적극적으로 들어주고, 결단력 있는 모습으로 프로젝트를 이끌어주어 많은 것을 배웠음.
