import base64
import os

with open(os.path.join('client','Assets', 'BG.png'), 'rb') as imagefile:
    base64string = base64.b64encode(imagefile.read()).decode('ascii')

print(base64string)  # print base64string to console
# Will look something like:
# iVBORw0KGgoAAAANS  ...  qQMAAAAASUVORK5CYII=

# or save it to a file
with open('testfile.txt', 'w') as outputfile:
    outputfile.write(base64string)
