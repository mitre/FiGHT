class ReferenceSet(object):

    def __init__(self):
        self.references = {}

    def add_reference(self, name, desc, url):
        if url in self.references:
            old_name = self.references[url].get_name()
            old_desc = self.references[url].get_desc()
            if name == old_name and desc == old_desc:
                pass
            

class Reference(object):

    def __init__(self, name, desc, url):
        self.name = name
        self.desc = desc
        self.url = url

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_desc(self, desc):
        self.desc = desc

    def get_desc(self):
        return self.desc