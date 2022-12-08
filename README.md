# PrettyASM

PrettyASM is a code formatting tool designed for 8-bit assembly language for processors such as the 6502, Z80, and 6809.

I have tried some "auto-format" tools and not had a great deal of success. In the old days when all code was in upper case and real tabs (Control-I, chr$(9) kind of things) were viewed more favorably, some did okay. But my recent projects needed something and were getting too large for line-by-line manual formatting.

I have used Python (primarily for data science type applications) and decided this was a chance to dig a bit deeper into some of the things I had wanted to learn about Python as I fixed a problem I had with my 8-bit assembly code.

BTW, I use the 6502 the most, but also work with code for the Z80, 8080/8085, 6809, 1802, and 6800. Some featurs of PrettyASM like putting a single space between the opcode and operand work well for the 6502 (where opcodes are always 3 characters) but might not be the best choice for other processors (or some assembler directives. I expect some tweaks in the code over time.

## Basics

You can run this from the command line once you enable execute priveleges for the the file under Linux. You can request help and should see something like this:

```
$ ./PrettyASM -h
usage: prettyasm [-h] [-l] [-L] [--colon {add,remove}] [-o] [-O] [-s] [-c]
                 [-C] [--tabs TAB TAB TAB] [-k]
                 input_file output_file

Pretty formatting for 8-bit assembly code.

positional arguments:
  input_file            input file name
  output_file           output file name

optional arguments:
  -h, --help            show this help message and exit
  -l, --llower          convert labels to lower case
  -L, --lupper          convert labels to UPPER CASE
  --colon {add,remove}  add or remove colon after all labels
  -o, --olower          convert opcodes and operands to lower case
  -O, --oupper          convert opcodes and operands to UPPER CASE
  -s, --space           single space between opcode and operands
  -c, --clower          convert comments to lower case
  -C, --cupper          convert comments to UPPER CASE
  --tabs TAB TAB TAB    Tab space for opcode, operade, and comment
  -k, --clobber         overwrite existing file with output file
```

I typically use the following command line:

`$ ./prettyasm -losk input.asm output.asm`

This forces labels, opcodes, and operands to lower case. It also puts a single space between the opcode and operand instead of expanding that out fully. By default, colons are added after labels. Finally, the `-k` option allows you to clobber any previous output file that might have the same name.

Semicolon comment indicators are what is mostly used today. In the old days, some of the 6502 assemblers I used expected the astrik instead. (Other 6502 assemblers used the astrix as a tolken for the current address and it would show up in the first column to set the address.

It was also more common to do some elaborate work with comments for things like:

```
;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                         ;
;;; EXAMPLE ;;;;;;;;;;;;;;;
;                         ;
; This is a fancy comment ;
; comment block!          ;
;                         ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;
```

These comment blocks were easy to find in printed listings and also could capture notes (both in the code and scribbled on hard copies).

The problem is that some code I have tinkered with has comments like this in it:

`    LDA #0   ;Initialize the counter`

I really don't like not having a space after the `;`. Pretty ASM will add a space in the later example, but is smart enough to look at the second character of a comment line and check for a space or a second `;`. If it sees either of those, it will not add a space. So far this logic seems to work with the code I have tested.

No modern assembler I use assumes asterisks at the first of a line are comments, not a reference to the program counter. But if you do want to let asterisks be receognized as the start of full-line comments there is a `-a` or `--asterisk` option that will treat those lines as comments and basically pass them through unchanged.


## Testing

I have created a fairly messy assembly file to run various test cases in the code against. If you think there are other ideas on things to fix or test for, I would be interested in hearing about them.

There is also a `-v` option from the command line (that is not listed in the help output) that will print details of what is happening as it goes through a source file line-by-line. This can help with debugging.


## Future Features

There are a few things I might change. I have actually thought about a GUI with radio buttons for selecting options and displays of the results side-by-side with the original code.

I know some people also use labels 'stand-alone' on their own line and might add support for that (even though I rarely use that format). PrettyASM should handle label lines okay in either approach.

I suspect there are some things that will need be be tweaked for specific assember directives and you can see the start of that in parts of the code.


## Reporting Bugs or Requesting Features

Please feel free to report any bugs you find! I try to test things before releasing them, but sometimes things slip through. Although only a modest project, this is one of the largest pieces of code I've done from scratch in Python.

If there are features you would like to see added, I'd be interested in hearing about them (although I can't promise they'll always get implemented). Or if you want to add features on your own, I'm happy to assist as possible.

I am also interested in any (hopefully) well-intentioned feedback on the code. As I mentioned, although I have used Python for a while, this is one of my largest projects done from scratch and includes my first use of argparse.

Development was done under Linux and I have not tested in other environments.


## The fine print...

Feel free to use this project under the terms of the MIT License.

MIT License

Copyright (c) 2022 by James McClanahan W4JBM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
