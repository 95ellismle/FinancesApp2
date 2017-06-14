from numpy import linspace

### Table Related Styles
font = "Helvetica [Cronyx]"
Header_Font = (font,16)
Item_Font = (font,14)
Tab_Font = (font,15)
Show_Table_Grid_Lines = False
Search_Bar_Font = (font, 16)
Search_Info_Font = (font,14)
Title_Font = (font, 17)

###


### App Styles

background_colour = [255, 255, 255, 255]
number_of_buttons_on_sidebar = 3
sidebar_button_colour = '#f0f0ff'
date_format = '%d/%m/%Y'

###rgba(251, 251, 251, 1)


### Plotting Page Styles

Command_Font = (font,16)

###

StyleSheets = {}
 ### Things that adjust the look of the tabs and the Table   
StyleSheets['Table']  = """
        QTableView
        {   
            border: none;
            alternate-background-color: #fbfbfb;
            background-color: white;
            color: black;
        }
        QTableView::item:hover
        {   
            color: black;
            background: rgb(255,240,190);  
        }
        QTableView::item:focus
        {   
            color: black;
            background: #ADD8E6;  
        }
        QHeaderView::section
        {
            background-color: white;
            border: 0;
            color: black;
            height: 50px;
            text-align: right;
            font-weight: bold;
        }
        QScrollBar:vertical {
            width: 25px;
            background-color: white;
        }  
        QScrollBar::handle::vertical
        {
            min-height: 100px;
            background-color: lightgrey;
        }
        QScrollBar::up-arrow::vertical 
        { 
            background-color: #f2f2f2;
            border: 0;
        }

        QScrollBar::down-arrow::vertical 
        {
            background-color: #f2f2f2;
            border: 0;

        }

"""

StyleSheets['Tab'] = """ 
        QTabBar::tab 
        {
                background-color: lightgrey;  
                gridline-color: none;
        }
        QTabWidget::pane 
        { 
                border: 0; 
                background-color: white;
        }
        QTabBar::tab::selected
        {
                background-color: white; 
                font-weight: bold;
        }
        QTabBar::tab::hover
        {
                background-color: lightgrey;
                font-weight: bold;
                color: darkslategrey;
        }
        QTabBar::tab::selected::hover
        {
                background-color: grey;
                font-weight: bold;
                color: white;
        }
        """
        
StyleSheets['Sidebar'] = """.QFrame 
        {
            background-color: white;
        }
"""

StyleSheets['Ok Button'] = """.QPushButton
        {
            background-color: green;
            color: white;
            font-size: 14;
            font-weight: bold;
            border: 0;
        }
        .QPushButton::hover
        {
            background-color: lightgreen;
            color: black;
            font-size: 15;
            font-weight: 900;
            border: 0;
        }
"""

StyleSheets['Date Buttons'] = """.QPushButton
        {
            background-color: white;
            color: black;
            font-size: 14;
            font-weight: bold;
            border: 0;
        }
        .QPushButton::hover
        {
            background-color: lightgreen;
            color: black;
            font-size: 15;
            font-weight: 900;
            border: 0;
        }
"""

StyleSheets['Text Frame'] = """.QPlainTextEdit
        {
            background-color: #f0f0f0;
            color: black;
            font-size: 14;
            font-weight: bold;
            border: 0;
        }
        .QPlainTextEdit::hover
        {
            background-color: white;
            font-size: 14;
            font-weight: bold;
            border: 0;
        }
"""

StyleSheets['Help Frame'] = """.QLabel
        {
            background-color: white;
            qproperty-alignment: AlignLeft;
            color: black;
            font-size: 14;
            font-weight: normal;
            border: 0;
        }
"""

StyleSheets['Search'] = """.QLineEdit
        {
            background-color: #dfdfff;
            color: #333300;
            border: 0;
            font-weight: bold;
            font-size: 14;
        }
"""

StyleSheets['Check Boxes'] = """.QCheckBox
        {
            color: black;
            border: 0;
            font-weight: light;
            font-style: italic;
        }
"""

for i in range(number_of_buttons_on_sidebar):
    StyleSheets['Button'+str(i)] = """
        .QPushButton
        {
            background-color: %s;
            color: darkslategrey;
            font-size: 25px;
            border-top: 1px solid black;
        }
        .QPushButton::hover
        {
            background-color: rgb(255,240,190);
            border: 0;
            color: darkslategrey;
            font-size: 27px;
            font-weight: 900;
        }"""%(sidebar_button_colour)