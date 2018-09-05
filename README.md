Software for Gigatron ROM
=========================

Important files
===============
```
gigatron-rom
 +--- LICENSE                   2-Clause BSD License
 +--- Makefile                  Marcel's Makefile
 +--- Core/                     Gigatron kernel and build tools
 |     +--- ROMv1.py            Video/audio/io/interpreter loops, built-in vCPU
 |     |                        applications and data ("kernel + ROM disk")
 |     |                        Execute this to build ROM files
 |     `--- compilegcl.py       Stand-alone GCL to vCPU compiler (GT1 files)
 +--- interface.json            Formal bindings interface to ROM for programs
 +--- Apps/                     Built-in and example applications (GCL and GT1)
 |     +--- Blinky.gcl          Very simple GCL program
 |     +--- HelloWorld.gcl      Program that draws "Hello world" on screen
 |     +--- WozMon.gt1          Port of Apple-1 monitor program
 |     `--- TinyBASIC.gt1       Integer BASIC interpreter
 +--- BASIC/                    Example BASIC programs
 +--- Images/                   Built-in images
 +--- Utils/
 |     +--- sendFile.py         Send a GT1 or BASIC file from laptop/PC to Gigatron
 |     `--- BabelFish/          Generic Arduino sketch for interfacing with
 |                              Gigatron. Used for transferring GT1 files into
 |                              the computer and/or hooking up an keyboard.
 +--- Docs/
 |     +--- GT1-files.txt       vCPU object file format and ROM versioning
 |     +--- GCL-language.txt    Gigatron Control Language and vCPU explanation
 |     +--- gtemu.c             An executable instruction set definition
 |     +--- TinyBASIC.ebnf      Formal definition of Gigatron TinyBASIC syntax
 |     `--- TinyBASIC.xhtml     Railroad diagram of Gigatron TinyBASIC syntax
 |
 `--- Contrib/                  Contributions outside the kit's ROM and tooling
       +--- at67/               Emulator/visualizer (SDL2), 8-bit/16-bit
       |                        assembler, debugger, MIDI music, demos (sprites,
       |                        lines, game of life, tetris game...)
       +--- flok99/             Simple (and slow) visualizer using SDL2
       +--- kervinck/           Ramblings (all work in progress)
       |     +--- gcl1.ebnf     Formal definition of GCL1 syntax
       |     `--- EBNF.xhtml    Railroad diagram of GCL1 syntax
       `--- xxxbxxx/            Bricks game; RPi port of BabelFish.ino
```

Files generated by ROMv1.py
=============================
```
ROMv1.asm                       Annotated disassembly, with labels and comments (large!)
ROMv1.rom                       ROM file for 27C1024 (PCB versions)
```

Memory map (RAM)
================
```
              0 1          47 48     127 128 129         (vSP)       255
             +-+-------------+-----------+-+-------------+--------------+
page 0       |0| System vars | User vars |1| User vars <-| Stack/Loader |
             +-+-------------+-----------+-+------+------+--+-----------+
page 1       | Video table                     239| vReset  | Channel 1 |
             +------------------------------------+---------+-----------+
page 2       |0                                    240   249| Channel 2 |
             |                                              +-----------+
page 3       | User vCPU code and/or data                   | Channel 3 |
             |                                              +-----------+
page 4       |                                              | Channel 4 |
             |                                              +-----------+
page 5-6     |                                              250      255|
             |                                                          |
             |                                                          |
             +----------------------------------------------------------+
page 7       | Sound tables                                             |
             +--------------------------------+-------------------------+
page 8-127   |0                            159|160                   255|
             | 120 lines of 160 pixels        |  Extra space for user   |
             | Default video memory           |  code and/or data       |
             =                                =                         =
             |                                |                         |
             +--------------------------------+-------------------------+
page 128-255 | Not used in the 32K system: mirror of page 0-127         |
             +----------------------------------------------------------+
              0                                                      255

Address   Name          Description
--------  ------------- -----------
0000      0             Constant
0001      memSize       Number of RAM pages detected at hard reset (64kB=0)
0002      channel       Sound channel update on current scanline
0003      sample        Accumulator for synthesizing next sound sample
0004      bootCount     0 for cold boot, >0 for warm boot
0005      bootCheck     Checksum of bootCount
0006-0008 entropy       Randomness from SRAM boot and input, updated each frame
0009      videoY        Counts up from 0 to 238 in steps of 2 (odd in vBlank)
000a      frameX        Starting byte within page for pixel burst
000b      frameY        Page of current pixel row (updated by videoA)
000c      nextVideo     Jump offset to scan line handler (videoA, B, C...)
000d      videoDorF     Handler for every 4th line (videoD or videoF)
000e      frameCount    Continuous video frame counter
000f      serialRaw     New raw serial read
0010      serialLast    Previous serial read
0011      buttonState   Clearable button state (can be convenient in user code)
0012      resetTimer    After 2 seconds of holding 'Start', do a soft reset
0013      xout          Memory cache for XOUT register
0014      xoutMask      The blinkenlights and sound on/off state
0015      vTicks        Remaining interpreter ticks (=units of 2 CPU cycles)
0016-0017 vPC           Interpreter program counter, points into RAM
0018-0019 vAC           Interpreter accumulator, 16-bits
001a-001b vLR           Return address, for returning after CALL
001c      vSP           Stack pointer
001d      vTmp          Scratch storage location for vCPU
001e      vReturn       Return address (L) from vCPU into the loop (H is fixed)
001f-0020 reserved      Reserved for ROM extensions
0021      romType       0x1c for ROMv1 release
0022-0023 sysFn         Address for SYS function call
0024-002b sysArgs       Arguments for SYS functions
002c      soundTimer    Countdown timer for playing sound
002d      ledTimer      Number of frames until next LED change
002e      ledState      Current LED state machine value (branch offset)
002f      ledTempo      Next value for ledTimer after LED state change
0030-007f userVars      Program variables
0080      1             Constant
0081-.... -             More space for program variables
....-00ff <stack>
0100-01ef videoTable
01f0-01f9 vReset        vCPU routine to load and start Reset sequence
01fa      wavA[1]       Sound channel 1
01fb      wavX[1]
01fc      keyL[1]
01fd      keyH[1]
01fe      oscL[1]
01ff      oscH[1]
0200-02f9 userCode      vCPU code/data (default start of user code)
02fa      wavA[2]       Sound channel 2
02fb      wavX[2]
02fc      keyL[2]
02fd      keyH[2]
02fe      oscL[2]
02ff      oscH[2]
0300-03f9 -             vCPU code/data
03fa      wavA[3]       Sound channel 3
03fb      wavX[3]
03fc      keyL[3]
03fd      keyH[3]
03fe      oscL[3]
03ff      oscH[3]
0400-04f9 -             vCPU code/data
04fa      wavA[4]       Sound channel 4
04fb      wavX[4]
04fc      keyL[4]
04fd      keyH[4]
04fe      oscL[4]
04ff      oscH[4]
0500-05ff -             vCPU code/dat
0600-06ff -             vCPU code/data
0700-07ff soundTable
0800-7fff screenMemory
0800-089f pixel line 0
08a0-08ff -             vCPU code/data
...
7f00-7f9f pixel line 119
7fa0-7fff -             vCPU code/data
--------  ------------- -----------
```

Memory map (ROM)
================
```
             +----------------------------------------------------------+
page 0       | Boot and reset sequences                                 |
             +----------------------------------------------------------+
page 1       | Video and audio loop (visible lines)                     |
             |                                                          |
page 2       | Video and audio loop (vertical blank)                    |
             +----------------------------------------------------------+
page 3       | vCPU interpreter loop (primary page)                     |
             |                                                          |
page 4       | vCPU extended instructions and SYS functions             |
             +----------------------------------------------------------+
page 5       | Shift tables                                             |
             |                                                          |
page 6       | SYS functions (LSRW and others)                          |
             +----------------------------------------------------------+
page 7-8     | Font table (ASCII 32..81 and 82..127)                    |
             +----------------------------------------------------------+
page 9       | Notes table (C-0..A#7)                                   |
             +----------------------------------------------------------+
page 10      | Inversion table                                          |
             +----------------------------------------------------------+
page 11-214  | ROM tables: Embedded high-resolution images (packed)     |
             |                                                          |
page 215-255 | ROM files: Embedded vCPU applications (serial)           |
             +----------------------------------------------------------+
              0                                                      255
```
