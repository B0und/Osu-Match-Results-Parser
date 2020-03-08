from des_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import re
import json
from lxml import html
import requests
from pprint import pprint
from openpyxl import Workbook
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Beatmap parser")
        app_icon = QtGui.QIcon()
        app_icon.addFile("icon.png", QtCore.QSize(256, 256))
        self.setWindowIcon(app_icon)

        self.ui.pushButton.clicked.connect(self.pushBtnFun)

    def pushBtnFun(self):
        url = self.ui.lineEditBeatmap.text()
        filename = self.ui.lineEditFilename.text()

        lobby_dict = {}

        url_list = url.split("|")
        for url in url_list:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            results = tree.xpath("//script[@id='json-events']/text()")
            # print(dir(results[0]))
            # print(str(results[0]))
            data = json.loads(str(results[0]))

            for item in data["events"]:
                if "game" in item.keys():
                    for _ in item["game"].keys():
                        # pprint(item['game']['beatmap']['beatmapset']['artist'])
                        artist = item["game"]["beatmap"]["beatmapset"]["artist"]
                        song = item["game"]["beatmap"]["beatmapset"]["title"]
                        diff = item["game"]["beatmap"]["version"]
                        col_name_str = artist + " - " + song + f"[{diff}]"

                        score_list = []
                        for score in item["game"]["scores"]:
                            score_list.append(score)

                        if col_name_str in lobby_dict.keys():
                            current_list = lobby_dict[col_name_str]
                            lobby_dict[col_name_str] = current_list + score_list

                        else:
                            lobby_dict[col_name_str] = score_list

                        score_list = []
                        break

        lobby_dict_new = {}

        for k, v in lobby_dict.items():
            temp_list = []
            for item in v:
                temp_list.append((item["score"], item["user_id"]))

            score_list = sorted(temp_list, key=lambda x: x[0], reverse=True)
            lobby_dict_new[k] = score_list

        # pprint(lobby_dict_new)

        wb = Workbook()
        ws = wb.active

        rowCnt = 1
        colCnt = 1

        for k, v in lobby_dict_new.items():
            ws.cell(row=rowCnt, column=colCnt, value=k)
            for item in v:
                rowCnt += 1
                ws.cell(row=rowCnt, column=colCnt, value=item[0])
                colCnt += 1
                ws.cell(row=rowCnt, column=colCnt, value=item[1])
                colCnt -= 1

            rowCnt = 1
            colCnt += 2

        wb.save(filename)
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    root.show()
    sys.exit(app.exec_())

