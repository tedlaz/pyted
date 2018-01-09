import parse_singularo as ps


if __name__ == '__main__':
    # book = ps.book_from_file('el2017.txt')
    book = ps.book_from_file('/home/tedlaz/pelates/2017/c/el2017c.txt')
    # book.isozygio_print('2017-01-01', '2017-09-30')
    book.eebook_totals('2017-01-01', '2017-09-30')
    book.eebook_print()
    # print(book.typoi)
    # book.isozygio_print('2017-01-01', '2017-09-30', 'ΦΠΑ')
    # book.kartella_print('38.00.00.000', '2017-01-01', '2017-09-30')
    # book.arthra_print()
    # txt = 'ΦΠΑ#54.00'
    # print(txt.split('#'))
