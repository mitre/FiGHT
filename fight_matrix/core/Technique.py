
class Technique(object):

    def __init__(self, tid, json_id, tname):
        self.tid = tid
        self.json_id = json_id
        self.tname = tname
        self.stids = []
        self.tactics = []
        self.platforms = []
        self.permsreq = []
        self.datasources = []
        self.version = ""
        self.created = ""
        self.modified = ""
        self.domain = ""
        self.url = ""
        self.mitigations = []
        self.detections = []
        self.references = []
        self.deprecated = False
        self.subtechnique = False

    def set_name(self, tname):
        self.tname = tname

    def get_name(self):
        return self.tname

    def set_tid(self, tid):
        self.tid = tid

    def get_tid(self):
        return self.tid

    def add_sub(self, stid):
        if stid in self.stids:
            pass
        else:
            self.stids.append(stid)

    def get_subs(self):
        return self.stids

    def deprecate(self):
        self.deprecated = True

    def get_deprecated(self):
        return self.deprecated

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def is_sub(self):
        return self.subtechnique

    def add_tactic(self, tactic):
        if tactic in self.tactics:
            raise Exception("Technique %s %s already has %s" % (self.tid, self.tname, tactic))
        else:
            self.tactics.append(tactic)

    def get_tactics(self):
        return self.tactics

    def has_tactic(self, tactic):
        if tactic in self.tactics:
            return True
        else:
            return False

    def add_platform(self, platform):
        if platform in self.platforms:
            raise Exception("Technique %s %s already has %s" % (self.tid, self.tname, platform))
        else:
            self.platforms.append(platform)

    def get_platforms(self):
        return self.platforms