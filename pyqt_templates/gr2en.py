import os
TGR = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩςάέήίϊΐόύϋΰώΆΈΉΊΪΌΎΫΏ"
TEN = "abgdezh8iklmn3oprstyfx4wABGDEZH8IKLMN3OPRSTYFX4WsaeiiiioyyywAEHIIOYYW"
counter = 0


def cap_first_letter(txt):
    '''Capitalize first letter'''
    lejeis = txt.split()
    ftxt = []
    for leji in lejeis:
        ftxt.append(leji.title())
    return ' '.join(ftxt)


def gr2en(txt, space=' '):
    '''Greek to Greeglish'''
    gdic = dict(zip(TGR, TEN))
    gdic[' '] = space
    found = False
    if space == '':
        tmp = cap_first_letter(txt)
    else:
        tmp = txt
    ftxt = ''
    for char in tmp:
        if char in gdic:
            found = True
        ftxt += gdic.get(char, char)
    if found:
        return ftxt
    return None


def rename_file(fname, no_space):
    '''Rename a file'''
    if no_space:
        space = ''
    else:
        space = '_'
    fnam, ext = os.path.splitext(fname)
    enam = gr2en(fnam, space)
    if ext:
        if enam:
            return ''.join([enam, ext])
    else:
        if enam:
            return enam


def process_dir(directory, no_space=False):
    """process all files in the folder"""
    global counter
    for fname in os.listdir(directory):
        file_or_dir = directory + os.sep + fname
        if os.path.isdir(file_or_dir):
            process_dir(file_or_dir, no_space)
        else:
            enam = rename_file(fname, no_space)
            if enam:
                oldf = directory + os.sep + fname
                newf = directory + os.sep + enam
                counter += 1
                # os.rename(oldf, newf)
                print('%5s:%s|%s' % (counter, oldf, newf))

if __name__ == '__main__':
    # print(gr2en('Καλά κρασιά και η ζωή μου 1όλη', ':'))
    process_dir('/run/media/tedlaz/wd1terra/backup/media/audio/music/greek', True)
