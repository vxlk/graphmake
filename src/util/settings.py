import json
import os
import io

class Settings():
    def __init__(self):
         # data
        self.data = {}
        self.data['settings'] = {}

        # settings file location
        self.appData = os.getenv('APPDATA') + "\\Graphmake"
        self.settingsFilePath = self.appData + "\\settings.json"

         # keys - fill me in when you add new params!
        self.kCmakeFileLoc = 'cmake_file_location'
        self.kLogFileLoc = 'log_file_location'
        self.kDbLocation = 'xml_database_location'
        self.kVarLocation = 'xml_var_database_location'
        self.kTagLocation = 'xml_tag_database_location'
        self.kDescLocation = 'xml_desc_database_location'
        self.kThemeColor = 'theme_color'
        self.kCmakeLogFileLoc = 'cmake_output'

        self.cmakeFilePath =  self.appData + "\\CMakeLists.txt"
        self.logFilePath = self.appData + "\\log.txt"
        self.dbPath = os.path.dirname(__file__) + "\\..\\model\\db\\db.xml"
        self.varPath = os.path.dirname(__file__) + "\\..\\model\\db\\vars.xml"
        self.descPath = os.path.dirname(__file__) + "\\..\\model\\db\\desc.xml"
        self.tagsPath = os.path.dirname(__file__) + "\\..\\model\\db\\tags.xml"
        self.theme = "Dark Orange" # default theme
        self.cmakeLogFilePath = self.appData + "\\cmake_output.txt"

        # if our settings file was deleted

        if not self.__on_load__():
            if not os.path.isdir(self.appData):
                os.mkdir(self.appData)
            # add data - fill me when you add new params!
            self.Add(self.kCmakeFileLoc, self.cmakeFilePath)
            self.Add(self.kLogFileLoc, self.logFilePath)
            self.Add(self.kDbLocation, self.dbPath)
            self.Add(self.kVarLocation, self.varPath)
            self.Add(self.kThemeColor, self.theme)
            self.Add(self.kCmakeLogFileLoc, self.cmakeLogFilePath)
            self.Add(self.kDescLocation, self.descPath)
            self.Add(self.kTagLocation, self.tagsPath)

    # remember to close this file handle if you use this function
    def CmakeFile(self) -> io.TextIOWrapper:
        return open(self.cmakeFilePath, 'w+')
    # remember to close this file handle if you use this function
    def SettingsFile(self) -> io.TextIOWrapper:
        return open(self.settingsFilePath, 'w+')
    # remember to close this file handle if you use this function
    def DBFile(self) -> io.TextIOWrapper:
        return open(self.dbPath, 'r')
    # remember to close this file handle if you use this function
    def DBVarFile(self) -> io.TextIOWrapper:
        return open(self.varPath, 'r')

    # modifying this will not actually modify the value
    def Value(self, settingName) -> str:
        return self.data['settings'][settingName]

    def Dump(self) -> None:
        json.dump(self.data, self.SettingsFile(), indent=4)

    def Add(self, key, value) -> None:
        self.data['settings'][key] = value
        self.Dump()

    # fill me in when you add new params!
    def __on_load__(self) -> bool:
        if not os.path.isdir(self.appData) or not os.path.isfile(self.settingsFilePath):
            return False
        
        settings_file = open(self.settingsFilePath, "r")
        self.data = json.load(settings_file)
        _map = self.data['settings']
        self.cmakeFilePath =  _map[self.kCmakeFileLoc]
        self.logFilePath = _map[self.kLogFileLoc]
        self.dbPath = _map[self.kDbLocation]
        self.varPath = _map[self.kVarLocation]
        self.theme = _map[self.kThemeColor] # default theme
        self.cmakeLogFilePath = _map[self.kCmakeLogFileLoc]
        self.tagsPath = _map[self.kTagLocation]
        self.descPath = _map[self.kDescLocation]

        settings_file.close()
        return True

# global "singleton"
settings = Settings()
