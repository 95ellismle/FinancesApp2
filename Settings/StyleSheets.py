from PyQt5.QtGui import QFont


from Gui import Funcs as f

### Table Related Styles

table_background_color = '#ffffff'
font = "Helvetica [Cronyx]"
Header_Font = (font,16)
Item_Font = (font,14)
Tab_Font = (font,15)
Show_Table_Grid_Lines = False
Search_Bar_Font = (font, 16)
Search_Info_Font = (font, 14)
Title_Font = (font, 17)

###


### App Styles

background_colour = '#eeeeee'
number_of_buttons_on_sidebar = 3
sidebar_button_colour = '#eeeeee'
date_format = '%d/%m/%Y'

###rgba(251, 251, 251, 1)


### Plotting Page Styles

plot_background_color = '#ffffff'
Command_Font = (font,16)

###

StyleSheets = {}
 ### Things that adjust the look of the tabs and the Table   
StyleSheets['Table']  = """
        QTableView
        {   
            border: none;
            alternate-background-color: %s;
            background-color: %s;
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
            background-color: %s;
            border: 0;
            color: black;
            height: 50px;
            text-align: right;
            font-weight: bold;
        }
        QScrollBar:vertical {
            width: 25px;
            background-color: %s;
        }  
        QScrollBar::handle::vertical
        {
            min-height: 100px;
            background-color: lightgrey;
        }
        QScrollBar::up-arrow::vertical 
        { 
            background-color: %s;
            border: 0;
        }

        QScrollBar::down-arrow::vertical 
        {
            background-color: %s;
            border: 0;
        }
        QScrollBar::add-line:vertical 
        {
              border: none;
              background: %s;
        }
        
        QScrollBar::sub-line:vertical 
        {
              border: none;
              background: %s;
        }
"""%(f.colorChange(table_background_color, 0.97, [0,1,2], 'scale'), table_background_color, table_background_color, table_background_color, table_background_color, table_background_color, table_background_color, table_background_color)

StyleSheets['Tab'] = """ 
        QTabBar::tab 
        {
                background-color: %s;  
                height: 45px; 
                width: 160px;
        }
        QTabWidget::pane 
        { 
                background-color: white;
        }
        QTabBar::tab::selected
        {
                background-color: white; 
                font-weight: bold;
        }
        QTabBar::tab::hover
        {
                background-color: #eeeeee;
                font-weight: 900;
                color: darkslategrey;
        }
        QTabBar::tab::selected::hover
        {
                background-color: white;
                font-weight: bold;
                color: black;
        }
        """%background_colour
        
StyleSheets['Info Table']  = """
        .QTableView
        {   
            border: none;
            alternate-background-color: white;
            background-color: white;
            color: black;
        }
        .QTableView::item
        {
            text-align: center;
        }
        .QHeaderView::section
        {
            background-color: white;
            border: none;
            color: black;
            font-weight: bold;
        }
        .QTableCornerButton::section 
        {
            border: none;
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
       
StyleSheets['Combo Box'] = """
        .QComboBox
        {
            background-color: white;
            color: black;
            font-size: 14pt;
            font-weight: bold;
            border: 0;
        }
"""

StyleSheets['Date Buttons'] = """.QPushButton
        {
            background-color: white;
            color: black;
            font-weight: light;
            border: 0;
        }
        .QPushButton::hover
        {
            background-color: white;
            color: black;
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

StyleSheets['Plot Buttons Account'] = """
        .QPushButton
        {
            background-color: white;
            color: black;
            font-weight: light;
            border: 0;
            font-size: 14pt;
        }
        .QPushButton::hover
        {
            background-color: #ededed;
        }
        .QPushButton::checked 
        {
            font-size: 16pt;
            color: black; 
            background-color: #fafafa; 
            border: 1px solid black;
            font-weight: bold;
        }
"""

StyleSheets['Plot Buttons Ydata'] = """
        .QPushButton
        {
            background-color: white;
            color: black;
            font-weight: light;
            border: 0;
            font-size: 13pt;
        }
        .QPushButton::hover
        {
            background-color: #ededed;
        }
        .QPushButton::checked 
        {
            font-size: 15pt;
            color: black; 
            background-color: #ffff00; 
            border: 1px solid black;
            font-weight: bold;
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
        QFrame
        {
        background-color: white;
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

StyleSheets['QLabel'] = """
    .QLabel
    {
         width=100;
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
        }
        .QPushButton::checked
        {
                font-weight: bold;
        }
        """%(sidebar_button_colour)