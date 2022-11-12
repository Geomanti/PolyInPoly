# Import math
from shapely.geometry import Polygon
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import Functions as F
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# From Data import text1, text2, text3, text4
# Creating arrays of points


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def drawChart():
    global fig_agg
    global fig
    fig = plt.figure(figsize=(10, 8))
    plt.axis('equal')
    fig_agg = draw_figure(window['canvas'].TKCanvas, fig)


layout = [
    [sg.Text('Polygon 1'), sg.InputText(), sg.FileBrowse(), sg.Checkbox('Fill holes', default=True)
     ],
    [sg.Text('Polygon 2'), sg.InputText(), sg.FileBrowse(), sg.Checkbox('Export poly')
     ],
    [sg.Text('        Area'), sg.InputText()
     ],
    [sg.Text('    Simplify'), sg.Slider(range=(1, 100), orientation='h', size=(35, 20), default_value=5, change_submits=True), sg.Button(button_text='Refresh')
     ],
    [sg.Text('     Output'), sg.InputText(), sg.FolderBrowse()
     ],
    [sg.Output(size=(120, 50), key='_output_'), sg.Canvas(size=(10, 8), key='canvas')],
    [sg.Submit(), sg.Cancel()]]

window = sg.Window('Polygon change area', resizable=True).Layout(layout).Finalize()

drawChart()

while True:  # The Event Loop
    event, values = window.read()
    window.FindElement('_output_').Update('')

    try:
        poly1Path = str(values[0])
        fillholes = bool(values[1])
        poly2Path = str(values[2])
        Exportpoly2 = bool(values[3])
        value = float(values[4])
        simplify = float(values[5])
        outpath = str(values[6])
    except:
        print('File problem')

    try:
        print('Loading...')
        f1 = open(poly1Path, 'rt')
        f2 = open(poly2Path, 'rt')
        print('Opening polygons')
        coords1 = F.PointsToPolygon(f1.read())
        coords2 = F.PointsToPolygon(f2.read())
        coords3 = F.ExtendPolyintoPoly2(coords1, coords2, value, fillholes, simplify)
        print('Creating new polygons')
        polygon1 = Polygon(coords1)
        if len(coords3) == 1:
            polygon3 = Polygon(coords3[0])
        else:
            polygon3 = Polygon(coords3)
        print('Reference polygon area: ' + str(polygon1.area))
        print('New polygon area: ' + str(polygon3.area))
        print('Added area: ' + str(polygon3.area - polygon1.area))
        polygon2 = Polygon(coords2)
        print('Done')
        print('Created polygon: ' + str(polygon3.wkt))
        preview = F.PointsToPolygon(polygon3.wkt)

        if event == 'Submit':
            print('Files has been created')

            if Exportpoly2:

                try:
                    polygon4 = polygon2.difference(polygon3)
                    with open(outpath + "\Poly2dest.wkt", "w") as file:
                        file.write(polygon4.wkt)
                        file.close
                except:
                    print('Difference problem, skipping')

            with open(outpath + "\Poly1dest.wkt", "w") as file:
                file.write(polygon3.wkt)
                file.close()

        fig_agg.get_tk_widget().forget()
        plt.clf()
        F.ShapeToView(coords1)
        F.ShapeToView(coords2)
        F.ShapeToViewContour(polygon3)
        fig_agg = draw_figure(window['canvas'].TKCanvas, fig)
    except:
        print('Something is wrong')

    if event in (None, 'Exit', 'Cancel'):
        break
