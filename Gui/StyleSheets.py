from numpy import linspace

table_background_colour = [250,250,250,255]

Header_Font = ("Helvetica",16)
Item_Font = ("Helvetica",14)
Tab_Font = ("Helvetica",15)

number_of_buttons_on_sidebar = 10
#border: 1px solid black;
StyleSheets = {                
        ### Things that adjust the look of the tabs and the Table        
        'tab' :""" QTabBar::tab 
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
            background: #ffdab9;  
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
        """,
        
        
        'button2':""".QPushButton
        {
            background-color: rgb(240,250,255);
            border: 0;
            color: rgb(240,69,19);
            font-size: 25px;
        }
        .QPushButton::hover
        {
            background-color: rgb(255,200,255);
            border: 0;
            color: rgb(240,69,19);
            font-size: 25px;
            font-weight: bold;
        }"""
}
       
button_colours = ['rgb(%i,%i,%i)'%(i,i,i) for i in linspace(250,220,number_of_buttons_on_sidebar)]
for i in range(number_of_buttons_on_sidebar):
    StyleSheets['button'+str(i)] = """
        .QPushButton
        {
            background-color: %s;
            color: rgb(139,69,19);
            font-size: 25px;
            border: 0;
        }
        .QPushButton::hover
        {
            background-color: rgb(255,240,190);
            border: 0;
            color: rgb(139,69,19);
            font-size: 29px;
            font-weight: 900;
        }"""%(button_colours[i])