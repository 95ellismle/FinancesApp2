from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from numpy.ma import masked_where, compressed
from numpy import abs

from Data import Strings as st

# A function to place objects in a layout.
# Align decideds the alignment of the layout, the Margins decide the margins and spacing decides the spacing between widgets.
# VH decides whether the widgets are aligned vertically or horizontally. Object is the parent widget, widgets are the children.
# Stretches must be a list and decides how big the widget is compared to its siblings.
def AllInOneLayout(Parent,children,Stretches=[1], VH='V', Align=False, Margins=[0,0,0,0], Spacing=0):
    if VH.lower() == "v":
        layout = QVBoxLayout()
    elif VH.lower() == 'h':
        layout = QHBoxLayout()
    else:
        print("\n\n\nLayout Function Won't Work As The VH Argument Has Not Been Set\n\n\n")
        return 0
    if Align:
        layout.setAlignment(Align)
    
    # Set the margins and the spacing
    layout.setContentsMargins(*Margins)
    layout.setSpacing(Spacing)
    
    # Add widgets to the layout
    try:
        try:
            Stretches[0]
        except TypeError:
            Stretches = list(Stretches)
        Stretches = Stretches*len(children)
        for i in range(len(children)):
            layout.addWidget(children[i],Stretches[i])
    except TypeError as e:
        layout.addWidget(children, Stretches[0])
        
    # Add the layout to the parent widget.
    if Parent:
        Parent.setLayout(layout)
        
    return layout

def aboveThreshold(data, threshold):
     if type(data) == list:
         new_data = []
         for i in range(len(data)):
             dat = masked_where(abs(data[0]) < threshold, data[i])
             dat = compressed(dat)
             new_data.append(dat)
         return new_data
     else:
         data = masked_where(abs(data) < threshold, data)
         data = compressed(data)
         return data
        
def hex2RGB(HEX):
    h = HEX.lstrip('#')
    try:
        return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
    except ValueError:
        return st.letterStrip(HEX)

def rgb2hex(rgb):
    if type(rgb) == str:
        rgb = st.letterStrip(rgb, "abcdefghijklmnopqrstuvwxyz()").split(',')
        rgb = [int(i) for i in rgb]     
    if any(type(i) == float for i in rgb):
        rgb = [int(i) for i in rgb]
    hex = "#{:02x}{:02x}{:02x}".format(*rgb)
    return hex

def shiftCol(rgb, amount, rgb_indices, Type='add'):
    rgb = list(rgb)
    for i in rgb_indices:
        if Type.lower() == 'add':
            rgb[i] += amount
        elif Type.lower() == 'scale':
            rgb[i] *= amount
            
        if rgb[i] < 0:
            rgb[i] = 0
        elif rgb[i] > 255:
            rgb[i] = 255
    return rgb

def rgb2str(rgb):
    string = 'rgb('
    for i in range(3):
        string += str(int(rgb[i]))+','
    string = string.rstrip(',')
    string += ')'
    return string

def colorChange(col, amount, rgb_indices, Type='add', output='rgb'):
    col = hex2RGB(col)
    col = shiftCol(col, amount, rgb_indices, Type)
    if output.lower() == 'rgb':
        return rgb2str(col)    
    if output.lower() == 'hex':
        return rgb2hex(col)
    
    
    
    