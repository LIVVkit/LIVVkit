import ConfigParser
import pprint

class ValidationParser(ConfigParser.ConfigParser):

    def read_dict(self, filepath):
        """ 
        Reads a config file and returns as a nested dictionary.
        If the config file had a section named Globals that section
        will be stripped out of the resulting dictionary, and its 
        values will be distributed to the rest of the sections.

        Args:
            filepath: the path of the file to be read

        Returns:
            A nested dictionary containing all of the sections
            and variables from the file given.
        """
        self.read(filepath)
        dt = dict(self._sections)
        # Prune out some information we don't need
        for k in dt:
            dt[k] = dict(self._defaults, **dt[k])
            dt[k].pop('__name__', None)

        # Go through and distribute the global information if 
        # there is any, but don't overwrite information if it
        # existed in the section previously
        if dt.has_key('Globals'):
            glbls = dt.pop('Globals',None)
            for sect in dt.keys():
                pprint.pprint(sect)
                for k,v in glbls.iteritems():
                    if not dt[sect].has_key(k): dt[sect][k] = v
        return dt

