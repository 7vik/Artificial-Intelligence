f = open("data.txt", "r")
text = f.read()
words = text.split(sep=' ')
final = []
for word in words:
    if '@' in word:
        final.append(word+'\n')
f.close()
ff = open("ddd.txt", "w")
ft = ''.join(final)
ff.write(ft)

    