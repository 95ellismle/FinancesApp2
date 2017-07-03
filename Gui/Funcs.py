from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from numpy.ma import masked_where, compressed
from numpy import abs

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

# Just tries to get the values associated with a dictionary, if the key isn't there it silently ignores it and returns None
def dict_value_get(dictionary,value):
    value = [i for i in dictionary.keys() if value in i]
    try:
        return dictionary[value[0]]
    except IndexError:
        return None

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
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))


def changeColor(rgb, amount, rgb_indices):
    rgb = list(rgb)
    for i in rgb_indices:
        rgb[i] = rgb[i] + amount
    return rgb

def rgb2str(rgb):
    return 'rgb('+str(rgb[0])+','+str(rgb[1])+','+str(rgb[2])+')'