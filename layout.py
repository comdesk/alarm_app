import sys
import json
import uuid
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDateTimeEdit, QSpinBox, QPushButton, QListWidget, QListWidgetItem,
    QFormLayout, QMessageBox
)
from PyQt6.QtCore import QDateTime, QTimer, Qt

class AlarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.alarms = self.load_alarms()
    
    def init_ui(self):
        self.setWindowTitle("알람 설정")
        self.setGeometry(100, 100, 600, 400)
        
        # 왼쪽 설정 레이아웃
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_form_widget = QWidget()
        left_form_layout = QFormLayout(left_form_widget)
        
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("알람 제목")
        
        self.datetime_input = QDateTimeEdit(self)
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        
        self.pre_alarm_input = QSpinBox(self)
        self.pre_alarm_input.setRange(0, 60)  # 0~60분 전까지 설정 가능
        self.pre_alarm_input.setSuffix(" 분 전 알람")
        
        self.save_button = QPushButton("저장", self)
        self.save_button.clicked.connect(self.add_alarm)

        left_label = QLabel("알람 설정")
        
        left_form_layout.setSpacing(15)
        left_form_layout.addRow(self.title_input)
        left_form_layout.addRow(self.datetime_input)
        left_form_layout.addRow(self.pre_alarm_input)
        left_form_layout.addRow(self.save_button)

        left_layout.addWidget(left_label)
        left_layout.addStretch()
        left_layout.addWidget(left_form_widget)
        left_layout.addStretch()
        left_layout.addStretch()
        
        # 오른쪽 알람 목록 레이아웃
        right_layout = QVBoxLayout()
        self.alarm_list = QListWidget(self)
        right_layout.addWidget(QLabel("알람 목록"))
        right_layout.addWidget(self.alarm_list)

        # 기존 저장된 알람 ui에 업데이트
        self.load_alarms_in_ui()

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        self.setLayout(layout)

        # 타이머 설정 (알람을 체크하는 주기)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_alarms)
        self.timer.start(60000)

    def load_alarms_in_ui(self):
        for alarm in self.load_alarms():
            print(f"기존 알람: {alarm}")
            self.add_alarm_list(alarm['id'], alarm['title'], alarm['set_time'], alarm['pre_alarm'])

    def load_alarms(self):
        try:
            with open("alarms.json", 'r', encoding='utf-8') as file:
                return json.load(file)
        except(FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_alarms(self):
        with open("alarms.json", 'w', encoding='utf-8') as file:
            json.dump(self.alarms, file, ensure_ascii=False, indent=4)

    def check_alarms(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
        print(f"현재시간: {current_time}")
        for alarm in self.alarms:
            alarm_time = QDateTime.fromString(alarm['time'], "yyyy-MM-dd hh:mm")
            alarm_time = alarm_time.addSecs(alarm['pre_alarm'] * -60)
            print(f"울려야할시간: {alarm_time.toString("yyyy-MM-dd hh:mm")}")
            print(f"같은가? : {alarm_time.toString() == current_time}")
            
            if alarm_time.toString("yyyy-MM-dd hh:mm") == current_time:
                print(f"알람***************")
                self.trigger_alarm(alarm)
        
    def trigger_alarm(self, alarm):
        print(f"알람 제목: {alarm['title']}")
        self.show_alarm_popup(alarm)
        
    def show_alarm_popup(self, alarm):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("알람")
        msg_box.setText(alarm['title'])

        remind_button = msg_box.addButton("5분 뒤 다시 알림", QMessageBox.ButtonRole.AcceptRole)
        dismiss_button = msg_box.addButton("종료", QMessageBox.ButtonRole.RejectRole)

        msg_box.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        msg_box.exec()
        print(f"클릭버튼: {msg_box.clickedButton}")

        if msg_box.clickedButton() == remind_button:
            print(f"5분뒤***")
            self.on_remind_in_5_minutes(alarm)
        elif msg_box.clickedButton() == dismiss_button:
            for i in range(self.alarm_list.count()):
                item = self.alarm_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == alarm['id']:
                    self.alarm_list.takeItem(i) 

            self.delete_alarm(alarm['id'])

    def on_remind_in_5_minutes(self, alarm):
        print(f"5분 뒤 다시 알림: {alarm['title']}")
        new_time = QDateTime.currentDateTime().addSecs(5*60 + alarm['pre_alarm']*60)
        alarm['time'] = new_time.toString("yyyy-MM-dd hh:mm")
        self.save_alarms()
        self.check_alarms()

    def delete_alarm(self, alarm_id):
        self.alarms = [a for a in self.alarms if a["id"] != alarm_id]
        self.save_alarms()
        print(f"남은 알람 목록: {self.alarms}")

    def add_alarm(self):
        id = str(uuid.uuid4())
        title = self.title_input.text()
        alarm_time = self.datetime_input.dateTime().toString("yyyy-MM-dd hh:mm")
        pre_alarm = self.pre_alarm_input.value()
        
        if title:
            # 알람 정보를 저장
            alarm_info = {
                'id': id,
                'title': title,
                'time': alarm_time,
                'set_time': alarm_time,
                'pre_alarm': pre_alarm
            }
            self.alarms.append(alarm_info)

            self.add_alarm_list(id, title, alarm_time, pre_alarm)
                
            self.save_alarms()
            self.title_input.clear()
    
    def add_alarm_list(self, id, title, set_time, pre_alarm):
            # 텍스트를 위한 QListWidgetItem
            item = QListWidgetItem()  # 텍스트는 위젯에 포함시킬 예정
            item.setData(Qt.ItemDataRole.UserRole, id)
            # item.setData(Qt.ItemDataRole.DisplayRole, "item_1")
            
            # 텍스트와 버튼을 포함할 QWidget 생성
            widget = QWidget()
            layout = QHBoxLayout(widget)
            
            # 텍스트 레이블을 추가
            label = QLabel(f"{title} - {set_time} ({pre_alarm}분 전)")
            layout.addWidget(label)
            layout.addStretch()
            
            # 삭제 버튼 추가
            delete_button = QPushButton("X")
            delete_button.setFixedWidth(25)
            delete_button.clicked.connect(lambda _, item=item: self.delete_alarm_from_button(item)) # 자바스크립트의 이벤트 핸들러의 람다 함수와 비슷
            layout.addWidget(delete_button)
            
            # 레이아웃 설정
            widget.setLayout(layout)
            
            # 아이템에 위젯 연결
            item.setSizeHint(widget.sizeHint())  # 아이템 크기를 위젯 크기에 맞게 설정
            self.alarm_list.addItem(item)  # 리스트에 아이템 추가
            self.alarm_list.setItemWidget(item, widget)

    def delete_alarm_from_button(self, item):
        # item = self.alarm_list.currentItem()
        print(f"삭제아이템: {item}")
        if item:
            row = self.alarm_list.row(item)
            item_id = self.alarm_list.item(row).data(Qt.ItemDataRole.UserRole)
            print(f"아이템롤: {item_id}")
            self.delete_alarm(item_id)
            self.alarm_list.takeItem(row)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlarmApp()
    window.show()
    sys.exit(app.exec())