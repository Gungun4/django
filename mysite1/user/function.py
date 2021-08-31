def logger(*args):
    info = 'info: '
    for i in args:
        info += str(i) + '--'
    print(info)

