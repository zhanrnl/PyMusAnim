from MusAnimRenderer import MusAnimRenderer
import string

def main():
    # the filename of the midi file to read music from
    input_midi_filename = "gould/gouldsyncfull04.MID"
    # the directory to save the generated frames to, relative to this file
    frame_save_dir = "gould/1080p01/"

    soprano_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. So go * a- *
^head, go a- head and * write a fugue. * Write a fugue that * we can sing. Give
no mind to what we've told you. Give no heed to what we've told you. Pay no mind
to what we've told you, what _we've told you. Just for- get all that we've told
you and the theo- ry that you've read. Pay no mind, give no heed to * what we've
* told you. Pay no mind to what we've told you, what we've said. Come and write
one. ^Oh, do come and write one, oh, write us a fugue. Yes, write a fugue that we
can sing, that we can sing. ^For ^the on- ly way to ^write ^one is just to plunge
right in and ^write * one. ^So just for get the rules * and * write one, have _a
try. * For the on- ly way to write * one is just to plunge right in and ^write *
^one. So just ig- nore the rules * and * write one. It's * a * pleas- ure that is
bound * to * sat- is- fy. And the fun of it ^will ^get you, And the _joy of ^it will
_fetch you, it will fetch you. ^You'll de- cide ^that John Se- bas- ^tian must _have
been a ver- y per- son- a- ble guy. And * a * bit of aug- ^men- _ta- tion is a se-
ri- ous temp- ta- tion, While a stret- ti dim- in- u- * tion, is an ob- vi- ous
so- lu- * tion, While a stret- ti, stret- ti ^stret- _ti ^dim- _in- u- tion is a ver-
y, ver- y ob- vi- ous sol- u- tion. Nev- er be clev- er for the sake of show-
ing off. No, ^nev- er be clev- er for the sake of be- ing clev- ^er. But do try to
write a fugue that we can sing, * * that we can sing. * * Just write a fugue
that we * can sing. * Now, why don't you try to write ^one? Try to write a fugue
for sing- ing. Write us a ^fugue _that we can sing. Come a- long now. It's rath-
er awe- some is- n't it? Well? Yes. Now _we're going to write a fugue. * _We're
going to write a fugue _right now.
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
tian, _You'll de- cide that _John Se- bas- _tian was a per- son- a- ble guy.
But nev- er be clev- er for the sake of be- ing clev- er, For a can- on in in-
ver- sion is a dan- ger- ous di- ver- sion. A bit of aug- ^men- _ta- tion is a se-
ri- ous temp- ta- * tion. Nev- er be clev- er for _the sake of show- * ing off.
But nev- er be clev- er for the sake of be- ing clev-
er, for the sake of * show- * * * * * * * * * * ing _off. Now, ^why don't you
write _a ^fugue, * * _why don't ^you try to ^write * one? * Write us a fugue * that
we * can sing. * Now come a- long. And when you've fin- ished writ- ing it I
think you'll ^find a great joy in it. Well? Why not? Now _we're going to write a
fugue. * _We're going to write a fugue _right now.
'''
    tenor_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. So go * a- * ^head,
* so go a- head, * and write a fugue. * * * * * So go a- head and ^write ^a fugue
that we * can * _sing. Go a- head, write a fugue, and write ^a fugue that we can
^sing. Go a- head, _write _a fugue that _we can sing * * that we can sing * * and
write a fugue that we can sing. Come a- long, go a- head, write a _fugue ^that we
can sing. Go a- head, write a fugue * that * we can sing, * * * * and write a
fugue that we can _sing. Write _a good fugue, one for sing- ing. Write a fugue
that we can sing. So * go a- head * and write a fugue, and ^write a fugue that *
we can sing. _Come, write a good fugue. Come, write ^a good fugue. _Come, write a
good fugue. Pay no mind to what we've told you. Just for- get all that we've
told you and the theo- ry * that you've * read, the theo- ry that you've ^read.
* _Pay no * mind, give no heed to * what we've * told you. ^For the on- ly way _to
write * one is just to plunge right in and write * one. So just for- get the
rules * and * write one. Have * a * try, have a try, * have a _try. For the on
ly way to write one is to plunge right _in and write one. Just ig- nore the rules
* and * try. And the fun of it will get you, _And the joy of it will fetch _you,
It's a pleas- ure that ^is bound to sat- is- fy, to sat- is- fy. So why don't you
try? For the on- ly way to write one is to ^plunge right in. * * * * * * * * *
You'll _de- cide that John Se- bas- _tian must have been a ver- y per- son- a-
ble, been a ver- y per- son- a- ble guy. So nev- er be clev- er For the sake of
be- ing clev- er, For the sake of show- ing off. Nev- er be clev- er for the
sake of show- ing off. ^So you want _to write a fugue. * * You've got the urge to
write a fugue. * * _You've got the nerve to write * a * fugue. * You've got ^the
urge to write * a * fugue that we * can * ^sing. _So write a fugue _that ^we can
sing. Why _don't you _try to write _one? _Write a fugue _that we can _sing. * Write
a fugue that we can sing. * Oh, come a long. Well? Yes. Now _We're going to write
a good _one. _We're going to write a fugue _right now.
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
^a fugue that * we can * sing. * Come, write ^a fugue that * we can sing. * _Come,
write a fugue that * we can sing. * Come, write ^a fugue, write a fugue that we
can sing, that * we can * sing. _Come, for the on- ly way to write * one is just
to plunge right in and write * one. So just for- get the rules, * and * write
one. Have * a * _try, have a try, have a try. Plunge ^right in, have a try. Try to
write one. Yes, try to write a fugue. Have a try, plunge _right in and write one.
Yes, just for- get all * that we've told you. Yes, plunge right _in, have a try,
and write one. Yes, _plunge right in, have _a try. Oh yes! Why don't you? Why
don't you write a fugue * now? For the on- ly way to write one is to plunge
right in. Just ig- ^nore _the rules ^and write one. _Have a try, * have ^a try. The
fun of it will get ^you, Joy of it will fetch you. You'll de- cide that John Se-
bas- tian was a per- son- a- ble guy. So nev- er be clev- er For the sake of
be- ing clev- er, For the sake of show- ing off. Nev- er be clev- * er for the
sake of show- ing off. So you want to write a fugue? * * _You've got the urge to
write a fugue. * * _You've got the nerve to write * a * fugue. So go * a- * head
and try to * write one, try to * write one. _Write us a good fugue, one that * we
* can * sing. Oh, come * and try. Oh, why don't you try? Oh, _won't you try to
write one * we can sing? Yes, come, let's try. Write us a fugue right now.
(Hope so.) _Well, noth- ^ing ven- tured noth- ing gained, _they say. But still it
is rath- er hard to start. Let us try. Right now? _We're going to write a good
_one. _We're going to write a fugue _right now.
'''

    # rendering parameters of all midi tracks in the midi file
    tracks = [
        {}, # dummy track if first track is just meta events
        { 'name': "soprano",
          'color': (0.973, 0.129, 0.093), # red
          'width': 25,
          'z-index': 4, # higher is on top
          'lyrics': soprano_lyrics
        },
        { 'name': "alto",
          'color': (0.929, 0.710, 0.137), # yellow
          'width': 25,
          'z-index': 3,
          'lyrics': alto_lyrics
        },
        { 'name': "tenor",
          'color': (0.078, 0.659, 0.129), # green
          'width': 25,
          'z-index': 2,
          'lyrics': tenor_lyrics
        },
        { 'name': "bass",
          'color': (0.098, 0.443, 1), # blue
          'width': 25,
          'z-index': 1,
          'lyrics': bass_lyrics
        },
        { 'name': "vln1",
          'color': (0.917, 0.384, 0.149), # red
          'width': 25,
          'z-index': 0,
        },
        { 'name': "vln2",
          'color': (0.776, 0.769, 0.098), # yellow
          'width': 25,
          'z-index': -1,
        },
        { 'name': "viola",
          'color': (0.075, 0.568, 0.353), # green
          'width': 25,
          'z-index': -2,
        },
        { 'name': "cello",
          'color': (0.188, 0.153, 0.945), # blue
          'width': 25,
          'z-index': -3,
        },
    ]

    # for changing the block speed in the middle of an animation
    # time is in seconds from first event, speeds are in pixels per second
    speed_map = [
        {'time': 0.0, 'speed': 12},
    ]

    # dimensions of generated image files
    dimensions = 1920, 1080
    # the intended fps of the animation
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 34, 86

    # debugging options
    first_frame, last_frame = None, None
    every_nth_frame = 1
    do_render = True

    # enough config, let's render that shit
    renderer = MusAnimRenderer()
    renderer.render(input_midi_filename, frame_save_dir, tracks, speed_map=speed_map,
        dimensions=dimensions, first_frame=first_frame, last_frame=last_frame,
        every_nth_frame=every_nth_frame, do_render=do_render)


if __name__ == '__main__':
    main()
