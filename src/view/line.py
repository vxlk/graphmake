from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPainterPath

class LineSettings():
    class LineType():
        Sinusoid = "Sine Wave Pattern"
    def __init__(self) -> None:
        self.type = LineSettings.LineType.Sinusoid
        self.color = Qt.black

class Line():
    def draw(
             startPoint : QPoint, 
             endPoint : QPoint,
             painter : QPainter, 
             settings : LineSettings = LineSettings()
             ) -> QPainterPath:
        # hardcoded sine wave
        half_width = (startPoint.x() - endPoint.x()) / 2.
        half_height = (startPoint.y() - endPoint.y()) / 2.
        half_point_x = endPoint.x() - half_width
        half_point_y = endPoint.y() - half_height
        
        painter.drawArc(QRect(startPoint.x(), startPoint.y(), half_width, half_height), -half_height, half_width)
        painter.drawArc(QRect(half_point_x, half_point_y, half_width, half_height), half_height, half_width)
