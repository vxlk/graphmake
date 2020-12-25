import json
import os

class Settings():
    def __init__(self):
        # filepaths
        self.appData = os.getenv('APPDATA') + "\\Graphmake"
        self.settingsFilePath = self.appData + "\\settings.json"
        self.cmakeFilePath =  self.appData + "\\CmakeLists.txt"
        self.logFilePath = self.appData + "\\log.txt"

        if not os.path.isdir(self.appData):
            os.mkdir(self.appData)

        # keys
        self.kCmakeFileLoc = 'cmake_file_location'
        self.kLogFileLoc = 'log_file_location'

        # data
        self.data = {}
        self.data['settings'] = {}
        self.Add(self.kCmakeFileLoc, self.cmakeFilePath)
        self.Add(self.kLogFileLoc, self.logFilePath)

    def CmakeFile(self):
        return open(self.cmakeFilePath, 'w+')

    def SettingsFile(self):
        return open(self.settingsFilePath, 'w+')

    # modifying this will not actually modify the value
    def Value(self, settingName):
        return self.data['settings'][settingName]

    def Dump(self):
        json.dump(self.data, self.SettingsFile(), indent=4)

    def Add(self, key, value):
        self.data['settings'][key] = value
        self.Dump()

    def Update(self, key, value):
        jsonObj = json.load(data)
        jsonObj[key] = value
        self.data = json.load(jsonObj)
        self.Dump()

# global singleton
settings = Settings()
