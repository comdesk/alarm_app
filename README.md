# alarm_app
날짜와 시간을 설정하고 알람을 등록할 수 있는 프로그램이다.

- 주요 기능:
  - 알람을 등록할 때 알람시간에서 몇 분 전에 알람을 울릴 지 설정할 수 있는 기능
  - 알람이 울렸을 때 5분 뒤에 다시 알람을 실행시킬 수 있는 기능
  - 닫기 버튼을 누르면 트레이 아이콘을 통해 실행시킬 수 있는 기능


![image](https://github.com/user-attachments/assets/d30bbfa7-012e-42ee-ac95-ee24b530e829)

---
# 설치 방법
1. 해당 프로젝트가 있는 경로에서 ``pyinstaller --onefile --windowed your_script.py`` 를 실행한다.
2. 생성된 dist 폴더에 있는 .exe 파일과 alarm.json 파일을 한 폴더에 넣고 .exe 파일을 실행한다.
