"""Module numspell.py
return greek text number
"""


def num2text(num):
    """
    num2text
    number must be integer always
    """
    txtval = str(num)

    mons = {1: 'ένα', 2: 'δύο', 3: 'τρία', 4: 'τέσσερα', 5: 'πέντε',
            6: 'έξι', 7: 'επτά', 8: 'οκτώ', 9: 'εννέα', 10: 'δέκα',
            11: 'έντεκα', 12: 'δώδεκα', 100: 'εκατό', 1000: 'χίλια'}
    deks = {1: 'δέκα', 2: 'είκοσι', 3: 'τριάντα', 4: 'σαράντα', 5: 'πενήντα',
            6: 'εξήντα', 7: 'εβδομήντα', 8: 'ογδόντα', 9: 'ενενήντα'}
    ekas = {1: 'εκατόν', 2: 'διακόσια', 3: 'τριακόσια', 4: 'τετρακόσια',
            5: 'πεντακόσια', 6: 'εξακόσια', 7: 'επτακόσια', 8: 'οκτακόσια',
            9: 'εννιακόσια'}
    if num == 0:
        return ''
    if num in mons:
        return mons[num]
    if len(txtval) == 2:
        di1, di2 = txtval
        return '%s %s' % (deks[int(di1)], mons[int(di2)])
    if len(txtval) == 3:
        di1 = txtval[0]
        di2 = txtval[1:]
        return '%s %s' % (ekas[int(di1)], num2text(int(di2)))
    if len(txtval) == 4:
        di1 = int(txtval[0])
        di2 = int(txtval[1:])
        if di1 == 1:
            return 'χίλια %s' % num2text(di2)
        else:
            return '%s χιλιάδες %s' % (num2text(di1), num2text(di2))
    if len(txtval) == 5:
        di1 = int(txtval[:2])
        di2 = int(txtval[2:])
        return '%s χιλιάδες %s' % (num2text(di1), num2text(di2))
    if len(txtval) == 6:
        di1 = int(txtval[:3])
        di2 = int(txtval[3:])
        return '%s χιλιάδες %s' % (num2text(di1), num2text(di2))
