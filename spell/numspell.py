"""Module numspell.py
return greek text number
"""


def num2text(num, miden=True):
    """
    num2text
    number must be integer always
    """
    if num == 0:
        if miden:
            return 'μηδέν'
        return ''
    txtval = str(num)

    mons = {1: 'ένα', 2: 'δύο', 3: 'τρία', 4: 'τέσσερα', 5: 'πέντε',
            6: 'έξι', 7: 'επτά', 8: 'οκτώ', 9: 'εννέα', 10: 'δέκα',
            11: 'έντεκα', 12: 'δώδεκα', 100: 'εκατό', 1000: 'χίλια', 0: ''}
    deks = {1: 'δέκα', 2: 'είκοσι', 3: 'τριάντα', 4: 'σαράντα', 5: 'πενήντα',
            6: 'εξήντα', 7: 'εβδομήντα', 8: 'ογδόντα', 9: 'ενενήντα', 0: ''}
    ekas = {1: 'εκατόν', 2: 'διακόσια', 3: 'τριακόσια', 4: 'τετρακόσια',
            5: 'πεντακόσια', 6: 'εξακόσια', 7: 'επτακόσια', 8: 'οκτακόσια',
            9: 'εννιακόσια'}
    ekaf = {1: 'εκατόν', 2: 'διακόσιες', 3: 'τριακόσιες', 4: 'τετρακόσιες',
            5: 'πεντακόσιες', 6: 'εξακόσιες', 7: 'επτακόσιες', 8: 'οκτακόσιες',
            9: 'εννιακόσιες'}

    if num in mons:
        return mons[num]
    if len(txtval) == 2:
        di1, di2 = txtval
        return '%s %s' % (deks[int(di1)], mons[int(di2)])
    if len(txtval) == 3:
        di1 = int(txtval[0])
        di2 = int(txtval[1:])
        return '%s %s' % (ekas[di1], num2text(di2, False))
    if len(txtval) == 4:
        di1 = int(txtval[0])
        di2 = int(txtval[1:])
        if di1 == 1:
            return 'χίλια %s' % num2text(di2, False)
        else:
            return '%s χιλιάδες %s' % (num2text(di1, False), num2text(di2, False))
    if len(txtval) == 5:
        di1 = int(txtval[:2])
        di2 = int(txtval[2:])
        return '%s χιλιάδες %s' % (num2text(di1, False), num2text(di2, False))
    if len(txtval) == 6:
        di1 = int(txtval[0])
        di2 = int(txtval[1:3])
        di3 = int(txtval[3:])
        val = '%s %s χιλιάδες %s' % (ekaf[di1], num2text(di2, False), num2text(di3, False))
        val = val.strip()
        val = val.replace('  ', ' ')
        return val
