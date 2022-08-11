class Proposed(object):

     def __init__(self, tempid, name):
          self.tempid = tempid
          self.name = name
          self.tactics = []
          self.bluf = ""
          self.source = []
          self.is_attack = False

     def set_tempid(self, tempid):
          self.tempid = tempid

     def get_tempid(self):
          return self.tempid

     def set_name(self, name):
          self.name = name

     def get_name(self):
          return self.name

     def add_tactic(self, tactic):
         if tactic.lower() in self.tactics:
             raise Exception("Proposed %s %s already has %s" % (self.tid, self.tname, tactic))
         else:
             self.tactics.append(tactic.lower())

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

     def set_bluf(self, text):
          self.bluf = text

     def get_bluf(self):
          return self.bluf

     def add_source(self, source):
          self.source.append(source)

     def get_sources(self):
          return self.sources

     def set_attack(self):
          self.is_attack = True

     def check_attack(self):
          return self.is_attack

