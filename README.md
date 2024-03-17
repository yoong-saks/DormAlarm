# DormAlarm

2023.01.23 기숙사 공지사항을 알려주는 알림 서비스가 없어 근로학생 모집 정보를 찾기 용이하게 하기위해 만들어졌습니다.  

## 기능

DormAlarm은 기숙사의 공지사항을 주기적으로 db에 추가하여 모니터링하며 새로운 게시글 정보를 발견하면 사용자에게 디스코드/텔레그램 알림을 보내는 기능을 제공합니다.  
![image](https://github.com/yoong-saks/DormAlarm/assets/42439493/b3d9ea2b-7ef9-4c48-accf-132e8e4fe9d7)

## Usage

crontab에 .sh 파일을 등록하여 주기적으로 py 파일이 실행되도록 했습니다.  
![스크린샷 2024-03-17 오후 6 15 41](https://github.com/yoong-saks/DormAlarm/assets/42439493/cde430af-c5eb-4974-9dcb-b47bf6b17e8d)  
sh의 로그를 추척하기위해 crontab을 통해 해당 디렉토리에 log를 남기도록 했습니다.

## 디스코드 알림봇
blog 설명 : https://flannelsocks.tistory.com/18

