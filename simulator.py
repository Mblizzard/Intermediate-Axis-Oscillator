import PySimpleGUI as sg
import os

filepaths = []

for root, dirs, files in os.walk('data'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.csv') and "meta" not in root:
            # print whole path of files
            filepath = os.path.join(root, file)
            filepaths.append(filepath)

colLayout = []

for i in range(0, len(filepaths)):
    colLayout.append([sg.Text(filepaths[i])])
    colLayout.append([sg.Graph((800, 200), (0, -60), (800, 60), "grey10", key="-GRAPH" + str(i) + "-")])

layout = [[sg.Col(colLayout, "grey30", (800, 800), key="-COL-", scrollable=True, element_justification="center")]]

window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   background_color="grey9",
                   finalize=True)

window.refresh()

print("Done.")

t = -100

header = True

data = []
lastxw = [0, 0]
lastyw = [0, 0]
lastzw = [0, 0]


for dataIndex in range(0, len(filepaths)):
    with open(filepaths[dataIndex], "r") as file:
        data = file.readlines()[1:]

    for i in range(1, 1000, 10):
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((i, -100), (i, 100), "grey15", 1)
        
    for dataPoint in data:
        time, xw, yw, zw, absw = dataPoint.split(",")
        time, xw, yw, zw, absw = float(time)*100, float(xw), float(yw), float(zw), float(absw)

        window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastxw, (time, xw), "green1", 2)
        lastxw = (time, xw)
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastyw, (time, yw), "light blue", 2)
        lastyw = (time, yw)
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastzw, (time, zw), "yellow", 2)
        lastzw = (time, zw)


#window["-GRAPH-"].DrawLine((-800, 0), (800, 0), "grey20", 1)


while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

    t += 1

