__author__ = 'willem'

text = """

#    # #   # #####  ###### #####  #    #  ####  #####  ######
#    #  # #  #    # #      #    # ##   # #    # #    # #
######   #   #    # #####  #    # # #  # #    # #    # #####
#    #   #   #####  #      #####  #  # # #    # #    # #
#    #   #   #      #      #   #  #   ## #    # #    # #
#    #   #   #      ###### #    # #    #  ####  #####  ######


     ####  #    # #####  #    # # #    #  ####  #####
    #      #    # #    # #    # # #    # #    # #    #
     ####  #    # #    # #    # # #    # #    # #    #
         # #    # #####  #    # # #    # #    # #####
    #    # #    # #   #   #  #  #  #  #  #    # #   #
     ####   ####  #    #   ##   #   ##    ####  #    #

"""


encoding = []

for r, line in enumerate(text.splitlines()):
    # print "line %s: %s" % (i, line)
    for c, char in enumerate(line):
        # print "char %s: %s" % (n, char)
        if char == '#':
            encoding.append((r + 1, c + 10))


print tuple(encoding)