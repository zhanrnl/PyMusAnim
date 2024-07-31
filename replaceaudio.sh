#!/bin/bash
function usage() {
  echo "Usage: ./replaceaudio.sh directory/"
  echo ""
  echo "This utility takes a directory name and will use the following files"
  echo "to create a new video with a given audio track:"
  echo "- audio.mid (will be converted to ogg with timidity)"
  echo "- audio.ogg (will exists will not process audio.mid)"
  echo "- video.mpg (will be used as video input, current audio being ignored)"
}

if [ $# == 0 ]; then
  usage;exit 1
fi
cd "$1"
if [ ! -e "video.mpg" ]; then
  usage;exit 2
fi
if [ ! -e "audio.ogg" ]; then
    if [ ! -e "audio.mid" ]; then
        usage;exit 2
    fi
    timidity audio.mid -Ov -o audio.ogg
fi
ffmpeg -i video.mpg -codec copy -an silent.tmp.mpg
ffmpeg -i silent.tmp.mpg -i audio.ogg -vcodec copy replaced.mpg
rm silent.tmp.mpg
