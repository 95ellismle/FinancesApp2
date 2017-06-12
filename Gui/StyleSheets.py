from numpy import linspace

### Table Related Styles

table_background_colour = [250,250,250,255]
Header_Font = ("Helvetica",16)
Item_Font = ("SansSerif",14)
Tab_Font = ("SansSerif",15)
Show_Table_Grid_Lines = True

###


### App Styles

number_of_buttons_on_sidebar = 3
sidebar_button_colour = '#f0f0ff'

###


### Plotting Page Styles

Command_Font = ("Helvetica",16)

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
            border: 0px solid black;
            background-color: #ebebeb;
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
                background-color: #f2f2f2;  
                gridline-color: none;
        }
        QTabWidget::pane 
        { 
                border: 0; 
                background-color: white;
        }
        QTabBar::tab::focus
        {
                background-color: lightgrey; 
                font-weight: bold;
        }
        QTabBar::tab::hover
        {
                background-color: lightgrey;
                font-weight: bold;
                color: darkslategrey;
        }
        QTabBar::tab::focus::hover
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

for i in range(number_of_buttons_on_sidebar):
    StyleSheets['Button'+str(i)] = """
        .QPushButton
        {
            background-color: %s;
            color: darkslategrey;
            font-size: 25px;
            border: 0;
        }
        .QPushButton::hover
        {
            background-color: rgb(255,240,190);
            border: 0;
            color: darkslategrey;
            font-size: 27px;
            font-weight: 900;
        }"""%(sidebar_button_colour)