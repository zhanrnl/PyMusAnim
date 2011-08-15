from MusAnimRenderer import MusAnimRenderer
import string

def main():
    # the filename of the midi file to read music from
    input_midi_filename = "gould/gouldsynccut05.MID"
    # the directory to save the generated frames to
    frame_save_dir = "gould/genimg/cut05/"

    soprano_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. So go * a- *
^head, go a- head and * write a fugue. * Write a fugue that * we can sing. Give
no mind to what we've told you. Give no heed to what we've told you. Pay no mind
to what we've told you, what _we've told you. Just for- get all that we've told
you and the theo- ry that you've read. Pay no mind, give no heed to * what we've
* told you. Pay no mind to what we've told you, what we've said. Come and write
one. ^Oh, do come and write on, oh, write us a fugue. Yes, write a fugue that we
can sing, that we can sing. ^For ^the on- ly way to ^write ^one is just to plunge
right in and ^write * one. ^So just for get the rules * and * write one, have _a
try. * For the on- ly way to write * one is just to plunge right in and ^write *
^one. So just ig- nore the rules * and * write one. It's * ^a * pleas- ure that is
bound * to * sat- is- fy. And the fun of it ^will ^get you, And the _joy of ^it will
_fetch you, it will fetch you. ^You'll _de- cide ^that John Se- bas- ^tian must have
been a ver- y per- son- a- ble guy.
'''
    alto_lyrics = '''^So you want to write a _fugue? * * You've ^got the urge to
^write a fugue. * * You've ^got the nerve to write * a * fugue. * You've got the
nerve to write * a * fugue that we * can * sing. Come a- long, go a- ^head and
_write one. Go a- head and write one, and write a good fugue, one that we can
sing. Go a- head * * write a fugue that * we can sing. Go a- head * and write a
fugue for sing- ing. Pay no ^heed to what we've told you, Pay no ^mind ^to what
we've told you. Give no heed to what we've told you, ^to what we've told you.
Just for- get all that we've told you and the theo- ry that * you've read, the
theo- ry that you've ^read. Pay no mind, give no heed to * what we've * told you.
Oh, give you mind to what we've * said. Pay no mind, give no heed to what we've
told you, what we've said. ^For the _on- _ly _way _to write one is just to _plunge
right in and write * one. So just for _get the _rules * and * write one. Why *
don't * you * have a try? For the on- ly way to write * one is just to
_plunge right in and write * one. So just ig- nore the rules * and * write a
fugue. It's a pleas- ure that is bound _to sat- is- fy. And the fun of it will
get you, And _the _joy of it will _fetch you. _You'll de- cide that _John Se- bas-
tian, _You'll de- cide that _John Se- bas- tian _was _a per- son- a- ble guy.
'''
    tenor_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. So go * a- * head,
* so go a- head, * and write a fugue. * * * * * So go a- head and write a fugue
that we * can * _sing. Go a- head, write a fugue, and write ^a fugue that we can
^sing. Go a- head, _write _a fugue that _we can sing * * that we can sing * * and
write a fugue that we can sing. Come a- long, go a- head, write a _fugue that we
can sing. Go a- head, write a fugue * that * we can sing, * * * * and write a
fugue that we can _sing. Write a good fugue, one for sing- ing. Write a fugue
that we can sing. So * go a- head * and write a fugue, and write a fugue that *
we can sing. _Come, write a good fugue. Come, write a good fugue. _Come, write a
good fugue. Pay no mind to what we've told you. Just for- get all that we've
told you and the theo- ry * that you've * read, the theo- ry that you've ^read.
* _Pay no * mind, give no heed to * what we've * told you. ^For the on- ly way _to
write * one is just to plunge right in and write * one. So just for- get the
rules * and * write one. Have * a * try, have a try, * have a _try. For the on
ly way to write one is to plunge right _in and write one. Just ig- nore the rules
* and * try. And the fun of it will get you, _And the joy of it will fetch _you,
It's a pleas- ure that ^is bound to sat- is- fy, to sat- is- fy. So why don't you
try? For the on- ly way to write one is to ^plunge right in. * * * * * * * * *
You'll de- cide that John Se- bas- _tian must have been a ver- y per- son- a-
ble, been a ver- y per- son- a- ble guy.
'''
    bass_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue, * * You've ^got the nerve to write * a * fugue. So go * a- * head,
so go * a- * head, go a- head ^and write a fugue, Go a- head, go a- head, go a-
head and write a fugue, write ^a fugue. Go a- head, write a fugue. You've ^got the
nerve to write ^a fugue. So come a- * long * and * write a * fugue. * Go a- head,
* write ^a fugue. * Oh, come ^a- long and write _a fugue * that * we * can * sing,
that we can sing. Go a- head, write a fugue that we can sing. Go a- head, write
a fugue, write a fugue _that we can sing. Write a good fugue, one that we can
sing, And write a good fugue, one that we can sing. Come a- long, write a fugue,
* that * we can * sing. Write a good fugue, one that we can * sing, that we can
sing. Come, write a fugue, come, write a fugue for sing- ing. Come, write a
fugue, come a- long and write a fugue for sing- ing. Come, write a good fugue.
Come, write a good fugue. Come, write a good fugue. Come, write ^a fugue that we
can sing. * _Come, write a good fugue, Come write a good fugue. _Come write a
fugue that we can sing. Oh, come, * * come, * * come and write one. Come write
a fugue that * we can * sing. * Come, write ^a fugue that * we can sing. * _Come,
write a fugue that * we can sing. * Come, write ^a fugue, write a fugue that we
can sing, that * we can * sing. _Come, for the on- ly way to write * one is just
to plunge right in and write * one. So just for- get the rules, * and * write
one. Have * a * _try, have a try, have a try. Plunge right in, have a try. Try to
write one. Yes, try to write a fugue. Have a try, plunge _right in and write one.
Yes, just for- get all * that we've told you. Yes, plunge right _in, have a try,
and write one. Yes, _plunge right in, have a try. Oh yes! Why don't you? Why
don't you write a fugue * now? For the on- ly way to write one is to plunge
right in. Just ig- ^nore _the rules and write one. _Have a try, * have ^a try. The
fun of it will get ^you, Joy of it will fetch you. You'll de- cide that John Se-
bas- tian was a per- son- a- ble guy.
'''

    # rendering parameters of all midi tracks in the midi file
    tracks = [
        {}, # dummy track if first track is just meta events
        { 'name': "soprano",
          'color': (0.973, 0.129, 0.093), # red
          'width': 10,
          'z-index': 4, # higher is on top
          'lyrics': soprano_lyrics
        },
        { 'name': "alto",
          'color': (0.929, 0.710, 0.137), # yellow
          'width': 10,
          'z-index': 3,
          'lyrics': alto_lyrics
        },
        { 'name': "tenor",
          'color': (0.078, 0.659, 0.129), # green
          'width': 10,
          'z-index': 2,
          'lyrics': tenor_lyrics
        },
        { 'name': "bass",
          'color': (0.098, 0.443, 1), # blue
          'width': 10,
          'z-index': 1,
          'lyrics': bass_lyrics
        },
    ]

    # for changing the block speed in the middle of an animation
    # time is in seconds from first event, speeds are in pixels per second
    speed_map = [
        {'time': 0.0, 'speed': 4},
    ]

    # dimensions of generated image files
    dimensions = 720, 480
    # the intended fps of the animation
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 34, 90

    # first and last frames to render (to save time, only render a subset
    # of frames)
    # if either are None, will default to first frame or last frame
    first_frame, last_frame = None, None

    # enough config, let's render that shit
    renderer = MusAnimRenderer()
    renderer.render(input_midi_filename, frame_save_dir, tracks, speed_map,
        dimensions, fps, min_pitch, max_pitch, first_frame, last_frame, 1)


if __name__ == '__main__':
    main()
