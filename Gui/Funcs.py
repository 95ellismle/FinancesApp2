from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


# A function to place objects in a layout.
# Align decideds the alignment of the layout, the Margins decide the margins and spacing decides the spacing between widgets.
# VH decides whether the widgets are aligned vertically or horizontally. Object is the parent widget, widgets are the children.
# Stretches must be a list and decides how big the widget is compared to its siblings.
def AllInOneLayout(Parent,children,Stretches=[1], VH='V',Align=False, Margins=[0,0,0,0], Spacing=0):
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


# A function to remove any substring enclosed between 2 ~ symbols within a string
def abs_remove(string):
         first = string.find('~')
         last =  string.rfind('~')
         if first != -1 and last != -1:
             return string[:first]+ string[last+1:]
         else:
             return string
    
    