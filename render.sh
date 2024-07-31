#!/bin/bash
#responsible from generating the OGG files and final MPG from PyMusLauncher's output
#being a separate step allows you to do some tricks like adding a few midi files if anything goes wrong and running this step again
function record(){
    rm *.ogg* 2&>/dev/null
    for midi in *.mid*; do #call pymusanim if there is an idle thread
        echo $midi
        if [ $timidity ]; then
            me=`whoami`
            while [ `ps -u $me|grep timidity|wc -l` != 0 ]; do sleep 1; done #wait for other instances to finish
            timidity $midi -Ov -o "$midi.timidity.ogg"
        fi
        if [ $musescore ] ; then
            while [ `ps -u $me|grep mscore|wc -l` != 0 ]; do sleep 1; done #wait for other instances to finish
            mscore $midi -o "$midi.musescore.ogg"
        fi
    done
}
function merge(){
    if [ -e frame00000.png ] ; then ffmpeg -f image2 -i frame%5d.png -qscale 0 silent.mpg; fi #png -> mpg
    for ogg in *.ogg; do #call pymusanim if there is an idle thread
        ffmpeg -i silent.mpg -i $ogg -vcodec copy "$ogg.mpg"
    done
    rm *.png 2&>/dev/null
}

type mscore 2&>/dev/null;musescore=$?
type timidity 2&>/dev/null;timidity=$?
if [ $# == 0 ]; then echo "Usage: ./render.sh partialdirectory/"; exit 2; fi
cd $1
record
merge
