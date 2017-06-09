background_colour = [255,255,255,255]

#border: 1px solid black;
StyleSheets = {                
        ### Things that adjust the look of the tab         
        'tab' :""" QTabBar::tab 
        {
                background-color: white;  
                gridline-color: none;
        }
        QTabWidget 
        {
                background-color: white;
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
                background-color: grey;
                font-weight: bold;
                color: yellow;
        }
        QTabBar::tab::focus::hover
        {
                background-color: grey;
                font-weight: bold;
        }
        """,
        
        
        ### Things that adjust the look of the tableview
        'Table'    :""" .QTableView
            {   
                border: none;
                alternate-background-color: #fbfbfb;
                background-color: white;
                color: black;
            }
            .QTableView::item:hover
            {   
                color: black;
                background: #ffdab9;            
            }
            .QTableView::item:focus
            {   
                color: black;
                background: #ADD8E6;  
            }
            .QHeaderView::section
            {
                border: 0.5px solid black;
                background-color: #fbffff;
                color: black;
                height: 50px;
                font-weight: bold;
            }
            QScrollBar:vertical {
                width: 25px;
                background-color: white;
                margin: 25 0 0 0;
            }  
            QScrollBar::handle::vertical
            {
                min-height: 100px;
                background-color: lightgrey;
            }
            QScrollBar::up-arrow::vertical 
            { 
                background-color: white;
            }
    
            QScrollBar::down-arrow::vertical 
            {
                background-color: white;
            }
            """
        }