from ..html.Element import Element

#TODO: Make an ABC for the Render method
class ViewModule(object):
    def Render(self):
        return Container
        
    @property
    def Container(self):
        return Element('div')