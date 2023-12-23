import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.figure

fig = matplotlib.figure.Figure(figsize=(5,4), dpi=100)
t = numpy.arange(0, 3, 0.1)
fig.add_subplot(111).plot(t, 2 * numpy.sin(2 * numpy.pi * t))

matplotlib.use("TkAgg")
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

layout =[
    [sg.Text("Plot test")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Ok")],
]

window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

draw_figure(window["-CANVAS-"].TKCanvas, fig)

event, values = window.read()

window.close()