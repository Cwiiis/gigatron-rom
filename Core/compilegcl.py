#!/usr/bin/env python
#-----------------------------------------------------------------------
#
#  Core video, sound and interpreter loop for Gigatron TTL microcomputer
#  - 6.25MHz clock
#  - Rendering 160x120 pixels at 6.25MHz with flexible videoline programming
#  - Must stay above 31 kHz horizontal sync --> 200 cycles/scanline
#  - Must stay above 59.94 Hz vertical sync --> 521 scanlines/frame
#  - 4 channels sound
#  - 16-bits vCPU interpreter
#  - Builtin vCPU programs
#  - Serial input handler
#  - Soft reset button (keep 'Start' button down for 2 seconds)
#
#  Cleanup after ROM v1 release
#  XXX Readability of asm.py instructions, esp. make d() implicit
#  XXX GCL: Prefix notation for high/low byte >X++ instead of X>++
#  XXX GCL: Rethink i, i. i; i= x, x. x= x: consistency, also DOKE, STLW etc
#  XXX How it works memo: brief description of every software function
#
#  Ideas for ROM v2
#  XXX Music sequencer (combined with LED sequencer, but retire soundTimer???)
#  XXX Adjustable return for LUP trampolines (in case SYS functions need it)
#  XXX Loader: make noise when data comes in
#  XXX vCPU: Multiplication (mulShift8?)
#  XXX vCPU: Interrupts / Task switching (e.g for clock, LED sequencer)
#  XXX Scroll out the top line of text, or generic vertical scroll SYS call
#  XXX Multitasking/threading/sleeping (start with date/time clock in GCL)
#  XXX Scoping for variables or some form of local variables? $i ("localized")
#  XXX Simple GCL programs might be compiled by the host instead of offline?
#  XXX vCPU: Clear just vAC[0:7] (Workaround is not bad: |255 ^255)
#  XXX Random dots screensaver
#  XXX Star field
#
#  Application ideas:
#  XXX Pacman ghosts. Sprites by scan line 4 reset method? ("videoG"=graphics)
#  XXX Audio: Decay, using Karplus-Strong
#  XXX ROM data compression (starting with Jupiter and Racer image)
#  XXX Font screen 16x8 chars
#  XXX Info screen (zero page)
#  XXX Gigatron layout balls/bricks game
#  XXX Embedded schematics
#  XXX Maze game. Berzerk/Robotron? Pac Mac
#  XXX Horizontal scroller. Flappy Bird
#  XXX Primes, Fibonacci (bignum), Queens
#  XXX Game of Life (edit <-> stop <-> slow <-> fast)
#  XXX Game #5 Shooter. Space Invaders, Demon Attack, Galaga style
#  XXX Exhibition mode: flip between applications in auto-play mode
#-----------------------------------------------------------------------

from sys import argv
from os  import getenv

from asm import *
import gcl0x as gcl

# TODO: Save out zpFree in theloop.py
# TODO: Custom start address?

def addProgram(gclSource, name, zpFree=0x0030):
  startAdr = pc()
  label(name)
  print 'Compiling file %s label %s' % (gclSource, name)
  program = gcl.Program(0x0200, name, False)
  zpReset(zpFree)
  for line in open(gclSource).readlines():
    program.line(line)
  program.end()
  print 'Success ROM %04x-%04x' % (startAdr, pc())
  print
  return (startAdr, pc())

align(0x100, 0x100)
link(argv[2])
(gclStart, gclEnd) = addProgram(argv[1], 'Main')

#-----------------------------------------------------------------------
# Finish assembly
#-----------------------------------------------------------------------
stem = basename(splitext(argv[1])[0])
end(stem)

# Extract compiled gcl into separate file
in_filename = stem + '.1.rom'
out_filename = stem + '.gt1'

print 'Create file', out_filename

with open(in_filename, 'rb') as input:
  input.seek(gclStart)
  data = input.read(gclEnd - gclStart)
  with open(out_filename, 'wb') as output:
    output.write(data)
    # Write out start address
    output.write(''.join([chr(0x02), chr(0x00)]))
