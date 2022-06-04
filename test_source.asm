; Test Input File for PrettyASM.py
;
; by James McClanahan W4JBM
; This file will not actually assemble because of things like
; including two different types of ORiGin statements.
;
; NOTE TO SELF: UPDATE FINAL LINE COUNT AFTER ANY EDITS!
;
; Version 0.0

; Some of this code started from my port of the following
; implementation of the eWoz monitor...
;
; "Just a few mods to the original monitor."
;
; By fsafstrom (March 2007)
; http://www.brielcomputers.com/phpBB3/viewtopic.php?f=9&t=197#p888

;;;;;;;;;;
; Some people use semis for "visual seperation"
;;;;;;;;;;
;But do we want a space after the first one on full line
;comments?
;;;;;;;;;;
; Comment might include things; simicolons for example ;
    nop ; same for non-full-line comments; eh? ;
;;Two or more semicolons at the beginning should not have
;; a space added.

; Some ASCII Equates

NULL    = $00
BS      = $08                   ; Backspace
LF      = $0A                   ; Linefeed
CR      = $0D                   ; Carriage Return
ESC     = $1B                   ; Escape
SPC     = $20                   ; Space
BSL     = $2F                   ; Backslash

ADDRL = $80 + 0
ADDRH = $80 + 1

*       = $1100
* = $1100
ORG     = $1100

; Some old school stuff that
* Old school astrick as a comment
label: sta msg comment starts after operand

; Test Case shifting

rEsEt   SEI                     ; DiSaBlE InTeRuPtS
        ClI                     ; clear interupts
        cLd                     ; NO BCD Mode

; ACIA initialization

SEND:   LDA #<MSG1   ; Point to Welcome Message
        sta msgl
        LDA #>MSG1
        sta msgH

;In general, trailing whitespace should is removed
; The following line had ten spaces
          
; Did they survive processing?

; The following two lines have ten spaces at the end
	LDA #0          
	lda #$ff ; comment          
; Did they survive processing?

; If there is not whitespace before a comment,
; we have problems processing it.
;
; this is lda ";"
test lda ";"
test lda ";" ;with valid comment comment spacing
test lda #0;invalid comment spacing
; Known issue should make the third test above glitch,
; although most assemblers would state there should be
; whitespace between the operand and the comment.


; Test that quoted values are handled properly...
    LDA #"X"
    .db "X"

really_long_label STA MSGH
lab05 nop
lab006 nop
lab0007 nop
lab00008 nop
lab000009 nop
lab0000010 nop
lab00000011 nop
lab000000012 nop
lab0000000013 nop
lab00000000014 nop

 sta msgl ; not much leading whitespace
 lda test ;and a comment with no space after semicolon

; full line comment with no space after semicolon

; a code segment with local labels starting with . or $

SHWMSG  LDY #$0
.PRINT  LDA (MSGL),Y
$PRINT: LDA (MSGL),Y
        BEQ .DONE
        JSR ECHO
        INY
        BNE .PRINT
.DONE   RTS
$DONE:  RTS

; tab to RTS
	RTS
; four spaces to RTS
    rts

MSG1    .TEXT CR,LF,"DUMMY TEST MeSsAgE",CR,LF,0
MSG2    .TEXT "Start Warp Engines!",0
MSG3    .db $41,$42,$4A,$4B,0



; This is final line (Line 130); no blank line follows...
