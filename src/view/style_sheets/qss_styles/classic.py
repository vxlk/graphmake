classic_stylesheet = """
QWidget {
    font-size: 11px;
}

QTableView {
    font-size: 10px;
    alternate-background-color: #EEEEFF;
}

Browser QPushButton {
    font-size: 10px;
    min-width: 10px;
}

ColorButton::enabled {
    border: 1px solid #444444;
}

ColorButton::disabled {
    border: 1px solid #AAAAAA;
}


Browser QGroupBox {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);
    border: 2px solid #999999;
    border-radius: 5px;
    margin-top: 1ex; /* leave space at the top for the title */
    font-size: 13px;
    color: black;
}

Browser QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding: 0 3px;
    font-size: 13px;
    color: black;
}

PluginItem {
    border: 2px solid black;
    background: white;
}


PluginItem Frame {
    background: #CCCCCC;
}


TabButton {
    border: 1px solid #8f8f91;
    border-radius: 2px;
    padding: 3px;
    min-width: 120px;
}

TabButton::checked {
    background-color: qlineargradient(x1: 0, y1: 0 , x2: 0, y2: 1,
                                      stop: 0 #9a9b9e, stop: 1 #babbbe);
}


TabButton::pressed {
    background-color: qlineargradient(x1: 0, y1: 0 , x2: 0, y2: 1,
                                      stop: 0 #9a9b9e, stop: 1 #babbbe);
}
"""