from whoarder.clippings import Clippings
import unittest


class TestImport(unittest.TestCase):

    def setUp(self):
        clippingsimporter = Clippings('test.txt')
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
        self.assertEqual(len(self.clippings), 17)

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
        self.assertEqual(len(highlights), 13)

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


class TestWrongImport(unittest.TestCase):

    def test_wrong_path(self):
        '''
        converting a non-existent file should return a FileNotFoundError
        '''
        with self.assertRaises(FileNotFoundError):
            self.clippings = Clippings('bar.txt')

if __name__ == '__main__':
    unittest.main()
