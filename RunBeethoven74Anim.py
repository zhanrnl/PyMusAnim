from MusAnimRenderer import MusAnimRenderer

def main():
    # the filename of the midi file to read music from
    input_midi_filename = "beethoven74/beethoven74fin02.MID"
    # the directory to save the generated frames to
    frame_save_dir = "beethoven74/full01/"

    # rendering parameters of all midi tracks in the midi file
    tracks = [
        {}, # dummy track if first track is just meta events
    	{ 'name': "vln1",
          'color': (0.973, 0.129, 0.093), # red
          'width': 24,
          'z-index': 4 # higher is on top
        },
        { 'name': "vln2",
          'color': (0.929, 0.710, 0.137), # yellow
          'width': 24,
          'z-index': 3
        },
        { 'name': "vla",
          'color': (0.078, 0.659, 0.129), # green
          'width': 24,
          'z-index': 2
        },
        { 'name': "vc",
          'color': (0.098, 0.443, 1), # blue
          'width': 24,
          'z-index': 1
        },
    ]

    # for changing the block speed in the middle of an animation
    speed_map = [
        {'time': 0.0, 'speed': 5}, # time is in seconds from first event
        {'time': 99.217, 'speed': 12}
    ]

    # dimensions of generated image files
    dimensions = 1920, 1080
    # the intended fps of the animation
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 34, 98
	
	# debugging options
    first_frame, last_frame = None, None
    every_nth_frame = 1
    do_render = True

    # enough config, let's render that shit
    renderer = MusAnimRenderer()
    renderer.render(input_midi_filename, frame_save_dir, tracks, speed_map=speed_map,
        dimensions=dimensions, first_frame=first_frame, last_frame=last_frame,
		min_pitch=min_pitch, max_pitch=max_pitch,
        every_nth_frame=every_nth_frame, do_render=do_render)


if __name__ == '__main__':
    main()