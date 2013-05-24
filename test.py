from whoarder.clippings import Clippings
import unittest


class TestWrongImport(unittest.TestCase):

    def test_wrong_path(self):
        '''
        converting a non-existent file should return a FileNotFoundError
        '''
        with self.assertRaises(FileNotFoundError):
            self.clippings = Clippings('bar.txt')


class TestImport(unittest.TestCase):

    def setUp(self):
        clippingsimporter = Clippings('test.txt')
        self.clippings = clippingsimporter.clippings

    def test_first_clipping(self):
        self.assertEqual(self.clippings[0]['book'], '<book>')
        self.assertEqual(self.clippings[0]['author_first_name'],
                         '<author_first_name>')
        self.assertEqual(self.clippings[0]['author_last_name'],
                         '<author_last_name>')
        self.assertEqual(self.clippings[0]['type'], '<type>')
        self.assertEqual(self.clippings[0]['page'], 'Page 42')
        self.assertEqual(self.clippings[0]['location'], '123-321')
        self.assertEqual(self.clippings[0]['date'], '<date>')

    def test_count(self):
        '''
        test.txt' should yield 14 clippings (either note or highlight)
        '''
        self.assertEqual(len(self.clippings), 15)

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

    def test_presence_author_first_name(self):
        '''
        Each clipping should reference its author's first name.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['author_first_name'])

    def test_presence_author_last_name(self):
        '''
        Each clipping should reference its author's last name.
        '''
        for clipping in self.clippings:
            self.assertIsNotNone(clipping['author_last_name'])

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

#     def test_presence_page(self):
#         '''
#                 # each clipping should reference the page it appeared on
#         '''
#         for clipping in self.clippings:
#             self.assertIsNotNone(clipping['page'])

if __name__ == '__main__':
    unittest.main()
