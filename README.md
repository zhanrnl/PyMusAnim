
#PyMusAnim

A clone of Stephen Malinowski's Music Animation Machine in Python.

This fork extends PyMusAnim so that Linux users can easily output a MPG video given an input MIDI file, using a command-line tool.

The original Music Animaion Machine and it's open source clone, PyMusAnim, are awesome. Unfortunately though the original project was never open source and ran poorly, on Windows and couldn't create video files by itself. PyMusAnim, using a totally different approach, doesn't suffer from performance issues - but it's orginally more of a proof of concept than a functioning tool. 

## Dependencies

You need those external programs installed on your system for this fork to work:

  * Python 2 https://www.python.org/
  * Timidity http://timidity.sourceforge.net/
  * FFMpeg https://ffmpeg.org/
  * MuseScore (optional) https://musescore.com/

On Debian and Ubuntu you can fulfill these requirementes by running the following command: `sudo apt-get install ffmpeg timidity python2.6 musescore`

## How it works

The core of PyMusAnim is virtually unchanged, the only difference being that instead of having to create your own Python configuration files the new module MusAnimLauncher does that for you (while still being configurable). This module is automatically called from two Linux command line (bash) utilities:

    ./pymusanim.sh file.mid outputdirectory [--dynamic]

Use this to create a video. For example: `pymusanim.sh mysong.mid mysong` will create a MPG file of `mysong.mid` inside the directory `mysong`.

    ./batch.sh midisDirectory mode [threadsLimit]

Use this one if you want to create several videos at once. Since PyMusAnim is single-threaded this will let you take advantage of a multi-core CPU if you have one (and you probably do). `midisDirectory` is the directory you have your MIDI files on and `threadsLimit` is an optional argument to explicitally set the number of threads to use (if not set the program will use all available processors). For each MIDI file a sub-directoy will be created inside the `output` folder, which will be created if it doesn't exist. For example: `batch.sh mymidis/`

Remember to run all these commands from the project's root directory.

## Dynamic mode

This fork adds a new rendering mode that can be activated by passing the argument --dynamic as the last argument to `MusAnimLauncher.py` or `pymusanim.sh`. Note that when running `batch.sh` you'll always need to inform which mode you're using (either `--classic` or `--dynamic`).

This mode tries to mimic somewhat the "shapes mode" of the original Music Animation Machine and focuses more on enhancing what's being played at each moment than on having a wider view of the composition being played.

## MuseScore

MuseScore is a great composition tool and offers a few featuress that work very well with PyMusAnim - namely being able to convert unsupported MIDI files into a supported format and also the ability to render them as audio files with higher quality than other tools. It is suggested that you install MuseScore in your system and, if you do then PyMusAnim will take full advantage of it when possible. Having it installed should help you automatically circumvent the issues detailed below.

## Issues

### A note about PyMusAnim and MIDI files

Unfortunately PyMusAnim is pretty bad at reading MIDI files in weird formats. I would go as far as to say that it's unable to read most MIDI files found on the web. The good news is that as long as the file is well formatted it will work perfectly.

Well... How is this even good news then? 

I have found that if I have trouble opening a MIDI file then I can use TuxGuitar to import that file and then export it again. This way the exported MIDI file will most likely work with PyMusAnim. TuxGuitar even has a batch conversion tool (under the Tools menu) that you can use to import and export many MIDI files at once automatically, making this a very fast if somewhat bothersome step.

I haven't tried but other programs with MIDI import and export features could potentially work for this as well.

### FreePats

FreePats is the libre soundbank that is used by Timidity and other Linux MIDI software. Despite doing a great job of allowing you to play most MIDI files for free, it can be a bit quirky and unfortunately isn't updated very often. You can see some hacks around its shortcomings on the 'freepats' directory. If you happen to know of any others hacks or good alternative libre soundbanks, let me know!

## Links

Original PyMusAnim: https://github.com/zhanrnl/PyMusAnim

PyMusAnim on YouTube: https://www.youtube.com/user/PyMusAnim

Original Music Animation Machine by Stephen Malinowski: http://www.musanim.com/player/

Malinowski on YouTube https://www.youtube.com/user/smalin

TuxGuitar: http://tuxguitar.herac.com.ar/ (also available via `sudo apt-get install tuxguitar` )

FreePats http://freepats.zenvoid.org/

## To do

* Improve support for reading all formats of MIDI files (this would be huge, if you think you can help please contact me!)
* Make PyMusAnim run on Python 3 too (should be pretty easy)
* A simple visual interface (GUI) so that it would be even easier to create PyMusAnim videos
* There is a issue with file paths containing whitespace not loading properly
* There may be an issue in batch mode with Timidity blocking the virtual MIDI device, rendering some videos silent but it doesn't seem to happen often
