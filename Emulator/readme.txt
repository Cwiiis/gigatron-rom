ROM (theloop.2.rom) can be downloaded here: https://github.com/kervinck/gigatron-rom
so simply download and place in the gigatron folder

Usage:
start ScriptTest, click File/Open and locate gigatron/gtemu.script
click Run Sketch (JIT) => note that the JITted VM typically runs 3x slower than native C++
press Escape to go back to IDE

the scripting environment is unfinished, in pre-alpha (no pun intended) stage, plus native API is still a bit clumsy
controller (input) might be emulated as well, arrows + A,S,Z,X for buttons, but I've no idea if it maps correctly
(can be changed in HandleInput)

Linux users will probably have set use_vsync to false (but this will imply tearing)
it might work with MESA emulation, but I've no idea about performance
also don’t forget to chmod u+x on ./ScriptTest

Mac users:
Due to sandboxing in Sierra+?, the app cannot be run from inside finder.
This is a problem because only the app folder is virtualized, datafiles fail to load and... boom.

Probably the best workaround is to unzip with a third party program (for example in midnight commander),
then restore executable permissions using chmod u+x ScriptTest.app/Contents/MacOS/ScriptTest via terminal.

Another workaround: run run_mac.sh from a terminal.
Another possibility might be to transfer via FTP to bypass browser, allowing the app to be run directly
from within Finder.

I'm not sure the RGB palette is ok but again it can be fixed in the script itself

Thanks to Marcel van Kervinck for Gigatron (+emulator) and to Harm Geert Muller for explaining how Gigatron works
