#!/usr/bin/python3
#
# prettyASM.py - Do bulk changes to .ASM code to make thing prettier
#
# USAGE: ./prettyASM.py filename.ext
#
# By Jim McClanahan, W4JBM (Dec 2020, June 2022)
#
# Mainly have used with 6502 assembly language code that is for the
# 64tass assembler. On some projects, the source code was getting
# messy and I'm bad about having a mix of tabs and spaces depending
# on the editor I am using at the time.
#
# Eventually I'd like to turn this into a command line utility
# that accepts options, but for now it is largely manual. (And,
# realistically, I only use it a few time a year, so a major
# overhaul is low on the priority list.)
#

import sys
import os.path
import argparse

# Options for "pretty" spacing and formatting. Eventually may convert
# to command line options.

snott = True # use spaces, not tab (tabs not yet implemented)
lblwr = True # convert labels to lower case
lbupr = False # convert labels to upper case
lbcln = True # put a colon after label?
oplwr = True # convert opcode and operand to lower case
opupr = False # convert opcode and operand to upper case
cmlwr = False # convert comments to lower case
cmupr = False # convert comments to upper case
frcsp = True # Force a space between fields so code can assemble
             # even if fields are too long for their allocated
             # space on the line.
spcfl = True # Force space after colon on full line comments?
             # Some coders do "pretty comments" that this will break

# Some vintage assemblers used "*" in column 1 for a comment. There
# may be trouble with truly vintage code because sometimes the assembler
# handled the label, opcode, and operand and simply discarded anything
# remaining as a "comment".

askor = True # Treat an "*" in column one as origin, not a comment

opcol = 10 # opcodes go in this column
opspc = False # just put a space between opcode and operand
orcol = 15 # if opsce is False, put operand in this column
cmcol = 25 # comments go out in this column

trbsh = not True # flag to turn on troubleshooting options

def valid_file():
# This method checks whether a valid file name was provided
    if (len(sys.argv) < 2):
        print("Pretty Formating for 8-Bit Assembly Code")
        print("USAGE: ./prettyASM.py <filename>")
        sys.exit(0)
    if not os.path.isfile(sys.argv[1]):
        print("Error! File does not exist.")
        sys.exit(0)

def is_blank(s):
# This is used to check for lines that are blank even if they
# have spaces or tabs in them

    return not bool(s and not s.isspace())


def contain(string_to_test, string_tested_against):
# This will check to see if the first string is in the second
# string. Used here only to check if a particular character is
# in a string of values of interest. (Similar to Java contain
# function.)

    return string_to_test in string_tested_against


def line_type(x):
# This determines type of line:
#
#   0 - unknown type of line
#   1 - blank line
#   2 - comment line (";" in first column)
#   3 - line starting with label
#   4 - line with whitespace then op code
#
# Note that a "*" at the start of the line can be treated as either
# a comment or a label (ORiGin) depending on options.

    if is_blank(x):
        return(1)

    if x[0]==";" or (not askor and x[0]=="*"):
        return(2)

    # Some assemblers support local labels that are only valid
    # within a range and may start with a period or a dollar sign

    if x[0].isalpha() or (x[0] in "$.") or (askor and x[0]=="*"):
        return(3)

    if x[0]==" " or x[0]=="/t":
        return(4)

    else:
        return(0)


def get_label(x):
# This function will get the label from the supplied string and
# handle thing such as conversion to upper or lower case and adding
# or removing traing colons

    if lblwr:
        line_lbl = x.lower().split()[0]
    elif lbupr:
        line_lbl = x.upper().split()[0]
    else:
        line_lbl = x.split()[0]

    # We have the label, make sure there is no colon
    if line_lbl[-1] == ":":
        line_lbl = line_lbl[:-1]

    # Now add colon if option is set, but not if it
    # part of an equate
    line_nxt = line.lower().split()[1]

    if lbcln and line_nxt != "equ" and line_nxt != "=":
        line_lbl = line_lbl + ":"
    return(line_lbl)


def get_opcode(x,y):
# This function will get the op code from a line of input
# If there is no op code, it will return a null string

    # adjust op code index to take into account whether
    # or not there is a label on the line
    if y==3:
        op_index=1
    else:
        op_index=0

    if oplwr:
        line_opc = x.lower().split()[op_index]
    elif opupr:
        line_opc = x.upper().split()[op_index]
    else:
        line_opc = x.split()[op_index]

    # Check to see if we have a comment instead of an op code
    if line_opc[0] == ";":
        line_opc = ""

    return(line_opc)


def get_operand(x,y,z):
# This function will get the operand from a line of input;
# If there is no operand, it will return a null string

# This code has to handle spaces even though they are not
# typically in operands; things like the following will
# exist and the series of numbers must be handled:
# crlf:  .db $0d, $0a, $00

# BEWARE: This will not properly handle a line where there
#         are multiple spaces like .db "Hello   World   !!"
#
#         In these cases, only a single space will be preserved
#         giving you .db "Hello World !!"

    # adjust op code index to take into account whether
    # or not there is a label on the line
    if y==3:
        op_index=2
    else:
        op_index=1

    # It is much, much easier if we "force" a "comment"
    # at the end of the line so we don't run into an
    # out of range condition

    x = x + " ; dummy comment"

    line_opr = ""

    # split the line into a list
    splt_line = x.split()

    # Get rid of label and op code
    for i in range(op_index):
        del splt_line[0]

    # This line should handle cases like LDA #"X" or .db "X"
    # NEEDS MORE TESTING TO VERIFY
    if (splt_line[0][0] == '"' or splt_line[0][0] == "'" or
        splt_line[0][0:1] == '#"' or splt_line[0][0:1] == "#'"):
       z = True

    for word in splt_line:
        if word[0] ==";":
            break # we have hit a comment (dummy or real)
        elif oplwr and not z:
            line_opr = line_opr + " " + word.lower()
        elif opupr and not z:
            line_opr = line_opr + " " + word.upper()
        else:
            line_opr = line_opr + " " + word

    # We have a stray space at the beginning
    if not is_blank(line_opr):
        line_opr = line_opr[1:]

    return(line_opr)


def get_comment(x):
# This function will get a comment staring with the first semicolon
# If there is no semicolon, it will return a null string

# BEWARE: To avoid having this glitch on something like an LDA ";",
#         we search for a blank space preceeding a comment; if there
#         is no blank space, we won't get the comment at the right
#         location on the line

    cmt_start = x.find(" ;")

    if cmt_start == -1:
        return("")

    # Get rid of leading space
    cmt_start += 1

    # This adds a space if there is not one between the semicolon
    # and the comment--should probably use an option flag to control
    if x[cmt_start+1] != " ":
        x = x[:cmt_start+1] + " " + x[cmt_start+1:]

    if cmlwr:
        return(x.lower()[cmt_start:-1])
    elif cmupr:
        return(x.upper()[cmt_start:-1])
    else:
        return(x[cmt_start:-1])


def format_flcomment(x):
# This function formats full line comments as needed.

    # This adds a space if there is not one between the semicolon
    # and the comment, but not if it looks like multiple semicolons
    # were used for a formatted comment
    if spcfl and (x[1] != " ") and (x[1] !=";"):
        x = "; " + x[1:]

    if cmlwr:
        return(x.lower())
    elif cmupr:
        return(x.upper())
    else:
        return(x)

####################################
#                                  #
### The real work starts here!!! ###
#                                  #
####################################

# Originally used a single command line argument for the input file
# and sent the output to a generic, fixed file name.
# infl = sys.argv[1]

parser = argparse.ArgumentParser(description="Pretty formatting for 8-bit assembly code.")
parser.add_argument("input_file", help="input file name")
parser.add_argument("output_file", help="output file name")
parser.add_argument("-l","--llower", action="store_true", help="convert labels to lower case")
parser.add_argument("-L", "--lupper", action="store_true", help="convert labels to UPPER CASE")
parser.add_argument("--colon", choices=["add", "remove"], default="add", help="add or remove colon after all labels")
parser.add_argument("-o", "--olower", action="store_true", help="convert opcodes and operands to lower case")
parser.add_argument("-O", "--oupper", action="store_true", help="convert opcodes and operands to UPPER CASE")
parser.add_argument("-s", "--space", action="store_true", help="single space between opcode and operands")
parser.add_argument("-c", "--clower", action="store_true", help="convert comments to lower case")
parser.add_argument("-C", "--cupper", action="store_true", help="convert comments to UPPER CASE")
parser.add_argument("-v", action="store_true", help="generate verbose debugging info")
parser.add_argument("--tabs", type=int, nargs=3, default=[12,18,28], metavar="TAB", help="Tab space for opcode, operade, and comment")

args = parser.parse_args()

# We may not always be interested in converting the case of the characters
# If not selections are made, only spacing is modified

lblwr = False # convert labels to lower case
lbupr = False # convert labels to upper case

if args.lupper:
    lblwr = False
    lbupr = True

if args.llower:
    lblwr = True
    lbupr = False

# lbcln = True # put a colon after label?
# Now handled by default value of "add" for --colon

if args.colon=="add":
    lbcln==True
else:
    lbcln==False

oplwr = False # convert opcode and operand to lower case
opupr = False # convert opcode and operand to upper case

if args.oupper:
    oplwr = False
    opupr = True

if args.olower:
    oplwr = True
    opupr = False

# opspc = False # just put a space between opcode and operand
# Now handled by presence or abscence of --space

opspc = args.space

cmlwr = False # convert comments to lower case
cmupr = False # convert comments to upper case

if args.cupper:
    oplwr = False
    opupr = True

if args.clower:
    oplwr = True
    opupr = False

# opcol = 12 # opcodes go in this column
# orcol = 18 # if opsce is False, put operand in this column
# cmcol = 28 # comments go out in this column
# Now handled with command line values and defaults

opcol = args.tabs[0]
orcol = args.tabs[1]
cmcol = args.tabs[2]

# Did we set the troubleshooting "verbose" output flag?

trbsh = args.v

# Seperate out the file names provided

infl = args.input_file
outfl = args.output_file

with open(infl) as f1:
    with open(outfl, "w") as f2:
        line_count =0

        for line_raw in f1:

            # we care about whitespace, not whether it is a tab,
            # so having everything be spaces might make life easier
            line = line_raw.replace('\t', ' ')

            line_count += 1 # increment line count

            if trbsh:
                f2.write("__processing line "+str(line_count)+"__\n")
            linet = line_type(line)

            # Print Blank Line
            if linet==1:
                if trbsh:
                    f2.write("__blank line__\n")
                f2.write("\n")
                continue # we are done with this line

            # Print Full Line Comment
            if linet==2:
                if trbsh:
                    f2.write("__full line comment follows__\n")
                f2.write(format_flcomment(line))
                continue # we are done with this line

            # Isolate the label
            if linet==3:
                line_label = get_label(line)
                if trbsh:
                    f2.write("__line label__ "+line_label+"\n")
            else:
                line_label = ""
                if trbsh:
                    f2.write("__no line label__\n")

            line_opcode = get_opcode(line, linet)
            if trbsh:
                if is_blank(line_opcode):
                    f2.write("__no op code found__\n")
                else:
                    f2.write("__op code found__ "+line_opcode+"\n")

            # The following tries to keep the logic that changes
            # operands to upper or lower case from changing the
            # case of some psydo op codes like those preceeding
            # a portion of text--manually expanded with experience
            if (line_opcode.lower() == ".text"):
                preserve_case = True
            else:
                preserve_case = False

            if is_blank(line_opcode):
                line_operand ="" # Not opcode, then no operand
            else:
                line_operand = get_operand(line, linet, preserve_case)

            if trbsh:
                if is_blank(line_operand):
                    f2.write("__no operand found__\n")
                else:
                    f2.write("__operand found__ "+line_operand+"\n")


            line_comment = get_comment(line)
            if trbsh:
                if is_blank(line_comment):
                    f2.write("__no comment found__\n")
                else:
                    f2.write("__comment found__ "+line_comment+"\n")

            if opspc:
                new_op = line_opcode + " " + line_operand
            else:
                # Added space so that even if there is an overrun we
                # do no blur things together (for example, .text is a
                # really long psydo op-code)
                new_op = line_opcode.ljust(orcol-opcol-1) + " " + line_operand

            # Things are nicely parsed at this point, but before we print
            # a line, we add space to ensure seperation. Some assemblers
            # might be able to handle no white space after a label that is
            # terminated by a colon, but I can't think of one I've used
            # where I would assume that without testing it first. This option
            # will likely remain hard-coded on.
            #
            # This does mess up later fields (they are pushed out of position
            # by the same number of spaces as the overrun), but for me this
            # would be a portion of source that needed some manual reformatting
            # or need a different set of parameters around column locations
            # so that doesn't matter.

            if frcsp:
                line_label = line_label + " "
                new_op = new_op + " "

            new_line = (line_label.ljust(opcol-1) + new_op.ljust(cmcol-opcol)
                        + line_comment)

            if linet==3 or linet==4:
                if trbsh:
                    f2.write(line)
                f2.write(new_line.rstrip()+"\n")


#            f2.write(str(linet))
#            f2.write(line)
f2.close()
f1.close()
