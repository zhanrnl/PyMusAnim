from MusAnimRenderer import MusAnimRenderer

def main():
    # the filename of the midi file to read music from
    input_midi_filename = "shostakovich10/shostakovich10midi01.MID"
    # the directory to save the generated frames to
    frame_save_dir = "shostakovich10/cut01/"

    # rendering parameters of all midi tracks in the midi file
    tracks = [
        {}, # dummy track if first track is just meta events
    	{ 'name': "picc",
          'color': (0.725, 0.871, 1.0), 
          'width': 20,
          'layer': 3,
        },
		{ 'name': "fl",
          'color': (0.475, 0.749, 1.0), 
          'width': 20,
          'layer': 3,
        },
		{ 'name': "ob",
          'color': (0.231, 0.431, 1.0), 
          'width': 20,
          'layer': 2,
        },
		{ 'name': "ebclar",
          'color': (0.31, 0.82, 1.0), 
          'width': 20,
          'layer': 2,
        },
		{ 'name': "bbclar",
          'color': (0.0, 0.643, 0.933), 
          'width': 20,
          'layer': 2,
        },
        { 'name': "bsn",
          'color': (0.098, 0.118, 1.0), 
          'width': 20,
          'layer': 2,
        },
        { 'name': "cbsn",
          'color': (0.102, 0.118, 0.784), 
          'width': 20,
          'layer': 2,
        },
        { 'name': "horn",
          'color': (1, .611, .098), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "horn2",
          'color': (1, .360, .004), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "tpt",
          'color': (1.0, 0.824, 0.176), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "tpt1",
          'color': (0.902, 0.667, 0.0), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "tbn",
          'color': (0.992, 0.157, 0.075), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "tbn2",
          'color': (0.886, 0.0, 0.086), 
          'width': 22,
          'layer': 2,
        },
        { 'name': "timp",
          'color': (0.659, 0.318, 0.212), 
          'width': 36,
          'layer': 0,
        },
        { 'name': "xyl",
          'color': (0.945, 0.671, 1.0), 
          'width': 22,
          'layer': 6,
        },
		{ 'name': "snare",
          'color': (0.816, 0.631, 0.361), 
          'width': 20,
          'layer': 0,
        },
		{ 'name': "vln1",
          'color': (0.725, .796, .043), 
          'width': 12,
          'layer': 5,
        },
		{ 'name': "vln2",
          'color': (0.53, .8, .054), 
          'width': 12,
          'layer': 5,
        },
		{ 'name': "vla",
          'color': (0.164, .67, .082), 
          'width': 12,
          'layer': 5,
        },
		{ 'name': "vc",
          'color': (0.016, .509, .180), 
          'width': 12,
          'layer': 5,
        },
		{ 'name': "cb",
          'color': (0.031, .463, .317), 
          'width': 12,
          'layer': 5,
        },
    ]

    # for changing the block speed in the middle of an animation
    speed_map = [
        {'time': 0.0, 'speed': 10}, # time is in seconds from first event
    ]

    # dimensions of generated image files
    dimensions = 1920, 1080
    # the intended fps of the animation
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 28, 108
	
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