from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


# A function to place objects in a layout.
# Align decideds the alignment of the layout, the Margins decide the margins and spacing decides the spacing between widgets.
# VH decides whether the widgets are aligned vertically or horizontally. Object is the parent widget, widgets are the children.
def AllInOneLayout(Parent,widgets,Stretches=[1], VH='V',Align=False, Margins=[0,0,0,0], Spacing=0):
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
        Stretches = Stretches*len(widgets)
        for i in range(len(widgets)):
            layout.addWidget(widgets[i],Stretches[i])
    except TypeError as e:
        layout.addWidget(widgets, Stretches[0])
        
    # Add the layout to the parent widget.
    if Parent:
        Parent.setLayout(layout)
        
    return layout