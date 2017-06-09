table_background_colour = [245,255,255,255]

#border: 1px solid black;
StyleSheets = {                
        ### Things that adjust the look of the tab         
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
            background-color: #fbffff;
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
        
        
        ### Things that adjust the look of the tableview
        'table'    :""" 
            """,
            
            ### Things that change the look of the sidebar
            'sidebar':""" 
            .QFrame
            {
                background-color: white;
                border: 0;
            }""",
            
            ### Things that change the look of the buttons on the sidebar
            'button1':"""
            .QPushButton
            {
                background-color: rgb(230,255,255);
                color: rgb(139,69,19);
                font-size: 25px;
                border: 0;
            }
            .QPushButton::hover
            {
                background-color: rgb(200,255,255);
                border: 0;
                color: rgb(139,69,19);
                font-size: 25px;
                font-weight: bold;
            }""",
            
            'button2':""".QPushButton
            {
                background-color: rgb(255,230,255);
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