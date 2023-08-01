from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
#----------------------------------------------------
#FOR TESTING PURPOSES, REMOVE BEFORE RELEASE
import os 

os.chdir(r"C:\Users\aikma\Desktop\python\palette")
#----------------------------------------------------

width = 113
height = 100
padding = 20
margin = 20
row_margin = 40

def rect(output, x, y, hex):
    output.roundRect(x, y, width, height, 10)
    tabledata = [[hex]]
    table = Table(tabledata, colWidths=width, rowHeights=padding)
    

output = canvas.Canvas("Hello.pdf")
rect(output, 20, 692)
output.showPage()
output.save()