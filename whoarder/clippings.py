

class Clippings:

    def __init__(self, source, dest=None):
        '''
        Launches the import and store it into the 'clippings' dict.
        '''
        self.source = source
        self.dest = self.get_default_dest() if dest is None else dest
        self.books = ()
        self.clippings = []
        self.import_clippings()

    def get_default_dest(self):
        '''
        When no destination is specified, output to InputFilename.html
        '''
        import os
        source_full_path = os.path.realpath(self.source)
        dirname, filename_with_ext = os.path.split(source_full_path)
        filename = os.path.splitext(filename_with_ext)[0]
        default_destination = os.path.join(dirname, filename + '.html')
        return default_destination

    def import_clippings(self):
        clippings = ClippingsIterator(self.source)
        for c in clippings:
            self.clippings.append(c)

        # a set of books will be useful later to display groups
        self.books = set((clipping['book'],clipping['author']) for clipping in self.clippings)

    def export_clippings(self):
        '''
        Output the clippings dict to HTML, using a Jinja2 template
        '''
        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader('whoarder', '.'),
                         autoescape=True,
                         extensions=['jinja2.ext.autoescape'])
        template = env.get_template('template.html')
        render = template.render(clippings=self.clippings, books=self.books)

        with open(self.dest, mode='w', encoding='utf-8') as output:
            output.write(render)


class ClippingsIterator:
    '''
    Iterator that abstracts the Kindle format and spits a dict per clipping.
    A 'clipping' can be either a Highlight or a Note, and is (as far as I
    know, on my Kindle) a succession of five lines (see ex. and regexes below):
    - Lines 1 & 2 contain metadata
    - Line 3 is empty
    - Line 4 is the clipping
    - Line 5 is the separator

    Example:
    <book> (<author_last_name>, <author_first_name>)
    - Your <type> on Page <page> | Location <locs>-<loce> | Added on <date>

    <contents>
    ==========
    '''
    import re

    clipping_separator = '==========\n'
    pattern_line1 = re.compile(r'''
        ^(?P<book>.*)                               # Le Petit Prince
        \ \((?P<author_last_name>.*)                #  (De Saint-Exupery
        ,\ (?P<author_first_name>.*)\)$             #  , Antoine)
        ''', re.VERBOSE)
    pattern_line2 = re.compile(r'''
        ^-\ Your\ (?P<type>.*)                      # Your Highlight
        \ on\ (?P<page>Unnumbered\ Page|Page\ .*)   #  on Page 42
        \ \|\ Location\ (?P<location>.*)            #  | Location 123-321
        \ \|\ Added\ on\ (?P<date>.*)$              #  | Added on...
        ''', re.VERBOSE)

    def __init__(self, source):
        detected_encoding = self.detect_encoding(source)
        self.source_file = open(source, mode='r', encoding=detected_encoding)
        pass

    def __iter__(self):
        return self

    def __next__(self):
        clipping_buffer = []
        count = 1
        while True:
            if count > 5:
                raise InvalidFormatException("Input file doesn't seem to be a clippings file, separators are missing or damaged")
            if self.source_file.closed:
                raise StopIteration

            line = self.source_file.readline()

            if not line:
                self.source_file.close()
                raise StopIteration
            elif line != self.clipping_separator:
                # Kindle writes a FEFF BOM at the start of each clipping (i.e.
                # every 6 lines), which is clearly wrong. We strip it.
                if line[0] == "\ufeff":
                    line = line.replace("\ufeff", "")
                clipping_buffer.append(line.strip())
                count += 1
            else:
                break

        line_dict = self.pattern_line1.search(clipping_buffer[0]).groupdict()
        line_dict2 = self.pattern_line2.search(clipping_buffer[1]).groupdict()
        line_dict.update(line_dict2)
        line_dict['contents'] = clipping_buffer[3]
        line_dict['author'] = line_dict['author_first_name'] + " " + line_dict['author_last_name']

        return line_dict

    def detect_encoding(self, source):
        '''
        Returns the encoding of the source file, using chardet.
        '''
        import codecs
        rawdata = open(source, "rb").read()
        # chardet detects UTF-8 with BOM as 'UTF-8' (I don't know why), i.e.
        # fails to notify us about the BOM, resulting in a string prepended
        # with \ufeff, so we manually detect and set the utf-8-sig encoding
        if rawdata.startswith(codecs.BOM_UTF8):
            detected_encoding = 'utf-8-sig'
        else:
            import chardet
            result = chardet.detect(rawdata)
            detected_encoding = result['encoding']
        return detected_encoding


class InvalidFormatException(Exception):
    pass
