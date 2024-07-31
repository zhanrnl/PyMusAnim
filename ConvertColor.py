import sys

for num in sys.argv[1:]:
    num = int("0x"+num,0)
    red = (num & 0xFF0000) >> 16
    green = (num & 0x00FF00) >> 8
    blue = (num & 0x0000FF)
    red = round((red + 0.0) / 255, 3)
    green = round((green + 0.0) / 255, 3)
    blue = round((blue + 0.0) / 255, 3)
    print (red, green, blue)