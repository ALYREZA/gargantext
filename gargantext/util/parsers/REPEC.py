from ._Parser import Parser

from gargantext.util.languages import languages

#from admin.utils import PrintException

class RepecParser(Parser):

#    def __init__(self, language_cache=None):
#
#        #super(Parser, self).__init__()
#        #super(Parser, self).__init__()
#        self._languages_cache = LanguagesCache() if language_cache is None else language_cache


    _begin = 6
    _parameters = {
        b"ER":  {"type": "delimiter"},
        b"T1":  {"type": "hyperdata", "key": "title", "separator": " "},
        b"ST":  {"type": "hyperdata", "key": "subtitle", "separator": " "},
        b"A1":  {"type": "hyperdata", "key": "authors", "separator": "\n"},
        b"JO":  {"type": "hyperdata", "key": "source"},
        b"UR":  {"type": "hyperdata", "key": "doi"},
        b"Y1":  {"type": "hyperdata", "key": "publication_year"},
        b"PD":  {"type": "hyperdata", "key": "publication_month"},
        b"N1":  {"type": "hyperdata", "key": "references", "separator": ", "},
        b"LA":  {"type": "hyperdata", "key": "language_iso2"},
        b"N2":  {"type": "hyperdata", "key": "abstract", "separator": " "},
        b"WC":  {"type": "hyperdata", "key": "fields"},
    }

    def parse(self, file):

        hyperdata = {}
        last_key = None
        last_values = []
        # browse every line of the file
        for line in file:
            if len(line) > 2 :
                # extract the parameter key
                parameter_key = line[:2]
                if parameter_key != b'  ' and parameter_key != last_key:
                    if last_key in self._parameters:
                        # translate the parameter key
                        parameter = self._parameters[last_key]
                        if parameter["type"] == "hyperdata":
                            separator = parameter["separator"] if "separator" in parameter else ""
                            if parameter["key"] == "publication_year":
                                hyperdata[parameter["key"]] = separator.join(last_values)[:4]
                            else:
                                hyperdata[parameter["key"]] = separator.join(last_values)
                        elif parameter["type"] == "delimiter":
                            if 'language_fullname' not in hyperdata.keys():
                                if 'language_iso3' not in hyperdata.keys():
                                    if 'language_iso2' not in hyperdata.keys():
                                        hyperdata['language_iso2'] = 'en'
                            yield hyperdata
                            hyperdata = {}
                    last_key = parameter_key
                    last_values = []
                try:
                    last_values.append(line[self._begin:-1].decode())
                except Exception as error:
                    print(error)
        # if a hyperdata object is left in memory, yield it as well
        if hyperdata:
            yield hyperdata
