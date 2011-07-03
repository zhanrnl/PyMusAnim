from MusAnimRenderer import MusAnimRenderer
import string

def main():
    # the filename of the midi file to read music from
    input_midi_filename = "gould/gouldsynccut03.MID"
    # the directory to save the generated frames to
    frame_save_dir = "gould/genimg/cut02/"

    alto_lyrics = '''^So you want to write a _fugue? * * You've ^got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. * You've got the
nerve to write * a * fugue that we * can *
'''
    tenor_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue. * * You've ^got the nerve to write * a * fugue. So go * a- * head,
* so go a- head, * and write a fugue. * * * * * So go a- head and write a fugue
that we * can * _sing. Go a- head, write a fugue, and write ^a fugue that we can
^sing. Go a- head, _write a fugue that we can sing * * that we can sing * * and
write a fugue that we can
'''
    bass_lyrics = '''So you want to write a fugue? * * You've got the urge to
write a fugue, * * You've ^got the nerve to write * a * fugue. So go * a- * head,
so go * a- * head, go a- head ^and write a fugue, Go a- head, go a- head, go a-
head and write a fugue, write ^a fugue. Go a- head, write a fugue. You've ^got the
nerve to _write a fugue. So come a- * long * and * write a * fugue. * Go a- head,
* write ^a fugue. * Oh, come ^a- long and write _a fugue * that * we * can * sing,
that we can sing. Go a- head, write a fugue that we can sing. Go a- head, write
a fugue, write a fugue _that we can sing. Write a good fugue, one that we can
sing, And write a good fugue, one that we can'''

    # rendering parameters of all midi tracks in the midi file
    tracks = [
        {}, # dummy track if first track is just meta events
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
    """
    { 'name': "vln1",
      'color': (0.973, 0.129, 0.093), # red
      'width': 8,
      'z-index': 4 # higher is on top
    },
    { 'name': "vln2",
      'color': (0.929, 0.710, 0.137), # yellow
      'width': 8,
      'z-index': 3
    },

    """

    # for changing the block speed in the middle of an animation
    # time is in seconds from first event, speeds are in pixels per second
    speed_map = [
        {'time': 0.0, 'speed': 6},
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
