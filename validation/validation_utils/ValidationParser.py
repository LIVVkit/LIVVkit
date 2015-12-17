import configparser

class ValidationParser(configparser.ConfigParser):

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
        dt = dict()
        self.read(filepath)
        for sect in self.sections():
            dt[sect] = dict()
            for k, v in self.items(sect):
                dt[sect][k] = v

        # Go through and distribute the global information if 
        # there is any, but don't overwrite information if it
        # existed in the section previously
        if dt.__contains__('Globals'):
            glbls = dt.pop('Globals',None)
            for sect in dt.keys():
                for k,v in glbls.items():
                    if not dt[sect].__contains__(k): dt[sect][k] = v
        return dt

