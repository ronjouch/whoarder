from whoarder.clippings import Clippings, InvalidFormatException
import unittest
import os


class TestImport(unittest.TestCase):

    def setUp(self):
        path = (os.path.dirname(__file__)) + "/test.txt"
        clippingsimporter = Clippings(path)
        self.clippings = clippingsimporter.clippings

    def test_first_clipping(self):
        self.assertEqual(self.clippings[0]['book'], '_BOOK_')
        self.assertEqual(self.clippings[0]['author'], '_AUTHOR_LAST_NAME_, _AUTHOR_FIRST_NAME_')
        self.assertEqual(self.clippings[0]['type'], '_TYPE_')
        self.assertEqual(self.clippings[0]['page'], 'Page 42')
        self.assertEqual(self.clippings[0]['location'], '123-321')
        self.assertEqual(self.clippings[0]['date'], '_DATE_')

    def test_count(self):
        '''
        test.txt should yield a certain number of clippings.
        '''
        self.assertEqual(len(self.clippings), 18)

    def test_count_notes(self):
        '''
        test.txt should yield 1 note
        '''
        print(self.clippings)
        notes = [i for i in self.clippings if i['type'] == 'Note']
        self.assertEqual(len(notes), 1)

    def test_count_highlights(self):
        '''
        test.txt should yield 13 highlights
        '''
        highlights = [i for i in self.clippings if i['type'] == 'Highlight']
        self.assertEqual(len(highlights), 14)

    def test_count_bookmarks(self):
        '''
        test.txt should yield 2 bookmarks
        '''
        bookmarks = [i for i in self.clippings if i['type'] == 'Bookmark']
        self.assertEqual(len(bookmarks), 2)

    def test_bom_stripped(self):
        '''
        Ensure repeated BOMs incorrectly written by Kindle are stripped
        '''
        for clipping in self.clippings:
            book_first_char = clipping['book'][0]
            self.assertNotEqual(book_first_char, "\ufeff")

    def test_presence_book(self):
        '''
        Each clipping should reference a book.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['book'])

    def test_presence_author(self):
        '''
        Each clipping should reference its author's name.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['author'])

    def test_presence_location(self):
        '''
        Each clipping should reference the kindle location it appeared on.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['location'])

    def test_presence_date(self):
        '''
        Each clipping should have a date.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['date'])

    def test_presence_contents(self):
        '''
        Each clipping should have contents.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['contents'])

    def test_multi_line_highlights(self):
        '''
        Multiline clippings should be read correctly
        '''

        contents = """John Doe remarked: \"Man, yeah.\n\nThis is tricky stuff\"\n"""
        print(self.clippings[-1]['contents'])
        self.assertEqual(contents, self.clippings[-1]['contents'])

class TestWrongImport(unittest.TestCase):

    def test_wrong_path(self):
        '''
        converting a non-existent file should return a FileNotFoundError
        '''
        with self.assertRaises(FileNotFoundError):
            self.clippings = Clippings('bar.txt')


class TestMulitlineHighlights(unittest.TestCase):

    def setUp(self):
        self.path = (os.path.dirname(__file__)) + "/failed_test.txt"

    def test_failed_multiline_highlights(self):
        '''
        the multiline highlight for failed_test.txt should return an InvalidFormatException
        
        '''
        with self.assertRaises(InvalidFormatException):
            Clippings(self.path)
        # self.assertIsNone(None)
    

if __name__ == '__main__':
    unittest.main()
