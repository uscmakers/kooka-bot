import sys
from PyQt5.QtWidgets import QApplication
from uitest import UI

def main():
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()

    ui = UI()
    ui.show()
    ui.setFixedSize(width/1.8, height/2.3)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()