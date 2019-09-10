import re
from regexp import calculate


def findall_0(regexp):
    text = """
    a=1
    a=+1
    a=-1
    a=b
    a=b+100
    a=b-100
    
    b+=10
    b+=+10
    b+=-10
    b+=b
    b+=b+100
    b+=b-100
    
    c-=101
    c-=+101
    c-=-101
    c-=b
    c-=b+101
    c-=b-101
    """

    return re.findall(regexp, text)


def findall_5(regexp):
    text = 'y+=y+100a=+1x-=y+101a=b+100y+=y-100y+=yx-=101x=1a=bx=y'

    return re.findall(regexp, text)


if __name__ == '__main__':
    print('test 0')
    result = calculate({'a': 1, 'b': 2, 'c': 3}, findall_0)
    correct = {"a": -98, "b": 196, "c": -686}
    if result == correct:
        print("Correct\n")
    else:
        print("Incorrect: %s != %s\n" % (result, correct))

    print('test 5')
    result = calculate({'a': 10, 'b': 20, 'c': 30}, findall_5)
    correct = {'a': 20, 'b': 20, 'c': 30}
    if result == correct:
        print("Correct\n")
    else:
        print("Incorrect: %s != %s\n" % (result, correct))

