from view.style_sheets.qss_styles.dark_orange import *
from view.style_sheets.qss_styles.dark_blue import *
from view.style_sheets.qss_styles.classic import *
from util.settings import *

class QssStyleSheetManager():
    dark_orange = dark_orange_stylesheet
    dark_blue = dark_blue_stylesheet
    classic = classic_stylesheet
    collection = { 'Dark Orange': dark_orange, 'Dark Blue': dark_blue, 'Classic': classic }
    currently_selected = settings.Value(settings.kThemeColor) # the default theme