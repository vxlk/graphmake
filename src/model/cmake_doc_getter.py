from model.node_model import nodeManager
import urllib.request, urllib.error, urllib.parse

class CmakeDocumentationGetter():
    cmake_version = "v3.20"
    base_url_command = "https://cmake.org/cmake/help/" + cmake_version + "/command/"
    base_url_variable = ""
    
    def __base_url__():
        if nodeManager.current_node_type == nodeManager.selected_type_function:
            return CmakeDocumentationGetter.base_url_command
        if nodeManager.current_node_type == nodeManager.selected_type_variable:
            return CmakeDocumentationGetter.base_url_variable

    def get(key):
        url = CmakeDocumentationGetter.__base_url__() + "cmake_host_system_information" + ".html" # need map in db
        response = urllib.request.urlopen(url)
        webContent = response.read()
        return str(webContent) # maybe revisit this to properly get form the site
        