# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import comtypes.client
from pyautocad import Autocad, APoint
import win32com.client as win32

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def print_cad():
    ProgID = "AutoCAD.Application.22"  # 2018版CADProgramID

    try:
        acad = comtypes.client.GetActiveObject(ProgID, dynamic=True)
    except WindowsError:
        acad = comtypes.client.CreateObject(ProgID, dynamic=True)
        acad.Visible = True

    print("The program will pause for 60 seconds.")  # 防止报错
    time.sleep(60)  # 程序暂停60s运行

    # 2.连接方式的转换
    acad = Autocad(create_if_not_exists=True)
    acad.prompt("Hello! AutoCAD from pyautocad.")
    doc = acad.ActiveDocument
    print(doc.Name)
    msp = doc.ModelSpace

    dwgobj = acad.ActiveDocument.Application.Documents.Add("")
    dwgobj.Activate()  # 设为当前文件。
    doc = acad.ActiveDocument
    print(doc.Name)
    msp = doc.ModelSpace

    # 3.创建图元
    x1, y1 = 0, 0
    x2, y2 = 100, 100
    p1, p2, = APoint(x1, y1), APoint(x2, y2)
    msp.AddLine(p1, p2)

    # 4.文件保存
    directory = r"D:"  # 工作目录
    dwgname = "ZK.dwg"  # 工作目录
    path = directory + "\\" + dwgname
    dwgobj.Close(True, path)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_cad()
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
