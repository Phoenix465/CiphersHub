def filter(text):
    alphabet = 'QWERTYUIOPASDFGHJKILZXCVBNM'
    newtext = ''
    for char in text:
        if char in alphabet:
            newtext += str(char)
        else:
            next
    return newtext
