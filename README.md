- url : https://jumpingfrogs.run.goorm.site
- groom ide free server

- Intellij IDE
- python 플러그인 설치
- python interpreter 설정
- 터미널에서 command prompt 창에 다음 코드 입력
- uvicorn main:app --reload => 서버 활성화
- http://39.124.125.152:1234 => 이전 서버 주소

- 가상환경 활성화
- . IS/bin/activate
- 비활성화
- deactivate

- 설치 모듈
- pip install fastapi
- pip install uvicorn[standard]
- pip install sqlalchemy
- pip install pymysql


- 서버 재가동
- 정지 -> 항상켜두기 다시 켜기 -> IS run 터미널 열기 -> 이전 서버 포트 닫기 -> 아래 코드 입력
- ps ux -> 열려있는 서버 확인
- kill -9 '해당 서버 pid'
- nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /dev/null
