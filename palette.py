from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
import bokeh.colors
import tkinter as tk

#Establishing dimensions of rectangles and filename
width = 113
height = 100
padding = 20
margin = 20
row_margin = 40
userpalette = []
brightlist = []
rgblist = []
palname = "palette"
output = canvas.Canvas(f"{palname}.pdf", pagesize=letter)

#Calculates brightness of colors given
def calc():
    progresslabel.config(text="Calculating...")
    for usercolor in userpalette:
        hexcode = usercolor.lstrip("#")
        rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
        mycolor = bokeh.colors.RGB(rgb[0], rgb[1], rgb[2])
        red = mycolor.r*0.212
        green = mycolor.g*0.701
        blue = mycolor.b*0.087
        brightness = (red + green + blue)/2.55
        rgblist.append(rgb)
        brightlist.append(brightness)

#Draws rectangles on PDF
def rect(x, y, hex, rgb, fontcolor):
    output.setFillColorRGB(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    output.roundRect(x, y, width, height, 10, fill=1)
    tabledata = [[hex]]
    table = Table(tabledata, colWidths=width, rowHeights=padding)
    table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'CENTER'),
                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
                                ('FONTSIZE', (0, 0), (0, 0), 10),
                                ('TEXTCOLOR', (0, 0), (0, 0), fontcolor)]))
    table.wrapOn(output, width, padding)
    table.drawOn(output, x, y + padding - 10)

#Adds given color to list
def addcolor():
     color = hexblank.get()
     hexblank.delete(0, 7)
     userpalette.append(color)
     colorlist = ""
     for color in userpalette:
          colorlist += color + "\n"
     colorlistlabel.config(text=colorlist)

#Names the palette
def sendname():
     global palname
     palname = nameblank.get()
     hexblank.delete(0, 50)
     palnamelabel.config(text=f"Palette name: {palname}")

#Exports PDF
def exportpdf():
    calc()
    progresslabel.config(text="Exporting PDF...")
    output._filename = f"{palname}.pdf"
    for row in range(5):
        for column in range(4):
            x = margin + column * (width + margin)
            y = output._pagesize[1] - (margin + (row + 1) * (height + margin))
            try:
                hex = userpalette[row * 4 + column]
            except IndexError:
                break
            rgb = rgblist[row * 4 + column]
            if brightlist[row * 4 + column] < 50:
                    fontcolor = "#FFFFFF"
            elif brightlist[row * 4 + column] > 50:
                    fontcolor = "#000000"
            rect(x, y, hex.upper(), rgb, fontcolor)
    output.showPage()
    output.save()
    progresslabel.config(text="Export complete!")

#UI setup
window = tk.Tk()
titlecard = tk.Label(window, text="Palette Pusher",font=25)
hexlabel = tk.Label(window, text='Type a hex code here, then press "Add color".')
hexblank = tk.Entry(window)
addbutton = tk.Button(window, command=addcolor, text="Add color")
colorlistlabel = tk.Label(window, text='')
namelabel = tk.Label(window, text='Name your palette...')
nameblank = tk.Entry(window)
namebutton = tk.Button(window, command=sendname, text="Send name")
palnamelabel = tk.Label(window, text=f'Palette name: {palname}')
exportlabel = tk.Label(window, text='Then click export to export your palette PDF!')
exportbutton = tk.Button(window, command=exportpdf, text="Export")
progresslabel = tk.Label(window, text='')
iconcreds = tk.Label(window, text='Icon courtesy of Freepik',font=("Helvetica",10))

titlecard.grid(row=0,columnspan=2,sticky="ew", padx=20)
hexlabel.grid(row=1,columnspan=2,sticky="nesw", padx=10, pady=10)
hexblank.grid(row=2, column=0,sticky="nesw", padx=10)
addbutton.grid(row=2, column=1,sticky="nesw", padx=10)
colorlistlabel.grid(row=3, columnspan=2,sticky="nesw",pady=50)
namelabel.grid(row=4, columnspan=2,sticky="nesw",padx=10, pady=10)
nameblank.grid(row=5, column=0,sticky="nesw",padx=10)
namebutton.grid(row=5, column=1,sticky="nesw",padx=10)
palnamelabel.grid(row=6, column=0,sticky="nesw",pady=10)
exportlabel.grid(row=7, columnspan=2,sticky="nesw",pady=50)
exportbutton.grid(row=8, column=1,sticky="nesw",padx=50, pady=10)
progresslabel.grid(row=9, columnspan=2,sticky="nesw",padx=50, pady=10)
iconcreds.grid(row=10, columnspan=2,sticky="nesw",pady=10)
window.mainloop()