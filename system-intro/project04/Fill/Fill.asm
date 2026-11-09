// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(MAIN_LOOP)

    (FILL_LOOP)
        @KBD
        D=M
        @CLEAR_LOOP
        D;JEQ

        @i
        M=1

        @SCREEN  // get base address of SCREEN
        D=A
        @addr
        M=D

        (BLACKEN)
            @i
            D=M
            @8192
            D=D-A
            @END_BLACKEN
            D;JGT

            @addr
            A=M
            M=-1

            @addr
            D=M+1
            M=D

            @i
            M=M+1
            
            @BLACKEN
            0;JMP
        (END_BLACKEN)

        @KBD
        D=M

        @END_FILL
        D;JEQ
        @FILL_LOOP
        D;JGT
    (END_FILL)

    (CLEAR_LOOP)
        @KBD
        D=M
        @FILL_LOOP
        D;JGT
        
        @i      // reset i
        M=1
        
        @SCREEN
        D=A
        @addr
        M=D
        
        (WHITEN)
            @i
            D=M
            @8192
            D=D-A
            @END_WHITEN
            D;JGT

            @addr
            A=M
            M=0

            @addr
            D=M+1
            M=D

            @i
            M=M+1
            
            @WHITEN
            0;JMP
        (END_WHITEN)

@MAIN_LOOP
0;JMP