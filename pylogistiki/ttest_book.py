import parse_singularo as ps


if __name__ == '__main__':
    # book = ps.book_from_file('el2017.txt')
    book = ps.book_from_file('/home/tedlaz/pelates/2017/d/el2017d.txt')
    # book.isozygio_print('2017-01-01', '2017-09-30')
    book.eebook_totals('2017-01-01', '2017-12-31')
    book.eebook_print()
    # print(book.typoi)
    # book.isozygio_print('2017-01-01', '2017-12-31')
    # book.kartella_print('38.00.00.000', '2017-01-01', '2017-09-30')
    # book.arthra_print()
    # txt = 'ΦΠΑ#54.00'
    # print(txt.split('#'))
