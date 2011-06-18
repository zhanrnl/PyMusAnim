import os, sys, colorsys
import Image, ImageDraw, ImageColor
from MusAnimLexer import *

def color_tuple_to_ImageColor(color_tuple):
    color = [int(val * 255) for val in color_tuple]
    return "rgb(" + str(color)[1:-1] + ")"

def blockify(midi_events):
    blocks = []
    bpm = 120.0
    time_seconds = 0
    time_beats = 0
    tracks_mode = ['normal'] * 5
    for event in midi_events:
        # increment times based on elapsed time in beats
        d_time_beats = event['time'] - time_beats
        time_seconds += (d_time_beats * 60.0) / bpm
        time_beats = event['time']
        if event['type'] == 'tempo': # set tempo
            bpm = event['bpm']
        elif event['type'] == 'note_on': # create new block in list
            blocks.append({'start_time': time_seconds, 'pitch': event['pitch'],
                'track_num': event['track_num']})
            # set shape of block to bar or circle
            if tracks_mode[event['track_num']] == 'normal':
                blocks[-1]['shape'] = 'bar'
            elif tracks_mode[event['track_num']] == 'pizz':
                blocks[-1]['shape'] = 'circle'
            else:
                raise Exception('Unknown track mode')
        elif event['type'] == 'note_off': # add end_time to existing block
            pitch = event['pitch']
            blocks_w_pitch = [block for block in blocks
                if block['pitch'] == pitch and 'end_time' not in block]
            assert(blocks_w_pitch) # assume it has at least one element
            blocks_w_pitch[0]['end_time'] = time_seconds
        elif event['type'] == 'keyswitch':
            tracks_mode[event['track_num']] = event['mode']
        else:
            raise Exception('Unknown midi event')
    return blocks

def add_block_info(blocks, tracks, fps, speed_map, dimensions, min_pitch,
    max_pitch):
    """Adds essential information to each block dict in blocks, also returns
    last_block_end to tell when animation is over"""
    # need: start_time (seconds), end_time (seconds), pitch, track_num for each
    # block
    last_block_end = 0
    cur_speed = get_speed(speed_map, 0.0)

    for block in blocks:
        width = tracks[block['track_num']]['width']
        cur_speed = get_speed(speed_map, block['start_time'])
        x_offset = calc_offset(speed_map, block['start_time'], fps)
        block['start_x'] = x_offset + dimensions[0]
        block['length'] = block['end_time'] - block['start_time'] + 0.0
        if block['shape'] == 'circle':
            x_length = width
        else:
            x_length = block['length'] * fps * cur_speed
        block['end_x'] = block['start_x'] + x_length
        if block['end_x'] > last_block_end:
            last_block_end = block['end_x']
        y_middle = ((0.0 + max_pitch - block['pitch']) / (max_pitch -
            min_pitch)) * dimensions[1]
        block['top_y'] = y_middle - (width / 2)
        block['bottom_y'] = y_middle + (width / 2)
        block['z-index'] = tracks[block['track_num']]['z-index']

    return blocks, last_block_end

def calc_offset(speed_map, time_offset, fps):
    x_offset = 0
    i = 0
    # speed is a dict with a speed and a time when we switch to speed
    speeds = [speed for speed in speed_map if speed['time'] < time_offset][0:-1]
    # add offsets from previous speed intervals
    if speeds:
        for speed in speeds:
            x_offset += ((speed_map[i+1]['time'] - speed_map[i]['time'])
                * fps * speed_map[i]['speed'])
            i += 1
    # add offset from current speed
    if time_offset > 0:
        x_offset += ((time_offset - speed_map[i]['time']) * fps
            * speed_map[i]['speed'])
    return x_offset

def get_speed(speed_map, time):
    """Retrieves the correct block speed for a given point in time from the
    speed map."""
    i = len(speed_map) - 1
    while time < speed_map[i]['time'] and i > 0:
        i -= 1
    return speed_map[i]['speed']

def draw_block(block, tracks, dimensions, draw, draw_mask=None):
    if block['start_x'] < (dimensions[0] / 2) and (block['end_x'] >
        (dimensions[0] / 2)):
        color = color_tuple_to_ImageColor(tracks[block['track_num']]
            ['high_color'])
    else:
        color = color_tuple_to_ImageColor(tracks[block['track_num']]['color'])
    if block['shape'] == 'circle':
        draw.ellipse((block['start_x'], block['top_y'], block['end_x'],
            block['bottom_y']), color)
        if draw_mask:
            draw_mask.ellipse((block['start_x'], block['top_y'], block['end_x'],
                block['bottom_y']), "grey")
    else:
        draw.rectangle((block['start_x'], block['top_y'], block['end_x']-1,
            block['bottom_y']), color)
        if draw_mask:
            draw_mask.rectangle((block['start_x'], block['top_y'],
                block['end_x']-1, block['bottom_y']), "grey")

def main():
    tracks = [
        {}, # dummy track if first track is just meta events
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
        { 'name': "vla",
          'color': (0.078, 0.659, 0.129), # green
          'width': 8,
          'z-index': 2
        },
        { 'name': "vc",
          'color': (0.098, 0.443, 1), # blue
          'width': 8,
          'z-index': 1
        },
    ]

    input_midi_file = "simplescale.MID"
    frame_save_dir = "genimg/testspeedchange/"

    dimensions = 720, 480
    speed = 3 # in pixels per frame
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 30, 90

    blocks = []
    lexer = MidiLexer()
    midi_events = lexer.lex(input_midi_file)

    blocks = blockify(midi_events) # convert into list of blocks

    # speed change events, time given in seconds
    speed_map = [
        {'time': 0.0, 'speed': 5},
        {'time': 0.5, 'speed': 8},
        {'time': 1.0, 'speed': 3},
        {'time': 1.25, 'speed': 9},
        {'time': 1.75, 'speed': 2},
        {'time': 2.25, 'speed': 20}
    ]

    for track in tracks:
        if 'color' in track:
            base_color = colorsys.rgb_to_hls(*track['color'])
            track['high_color'] = colorsys.hls_to_rgb(base_color[0], 0.9,
                base_color[2])

    # do some useful calculations on all blocks
    blocks, last_block_end = add_block_info(blocks, tracks, fps, speed_map,
        dimensions, min_pitch, max_pitch)

    # following used for calculating percentage done to print to console
    original_end = last_block_end
    percent = 0
    last_percent = -1

    # sort by z-index descending
    blocks.sort(lambda a, b: cmp(b['z-index'], a['z-index']))

    # for naming image files:
    frame = 0
    # for keeping track of speed changes:
    time = -dimensions[0]/(2.0*fps*speed_map[0]['speed'])

    # generate frames while there are blocks on the screen:
    while last_block_end > (0 - speed):
        im = Image.new("RGBA", dimensions, "black")
        # overlay is for second drawing pass
        im_overlay = Image.new("RGBA", dimensions, "black")
        draw = ImageDraw.Draw(im)
        draw_overlay = ImageDraw.Draw(im_overlay)
        # greyscale mask for compositing
        mask = Image.new("L", dimensions, "black")
        draw_mask = ImageDraw.Draw(mask)

        # need to do two passes of drawing blocks, once in reverse order in full
        # opacity, and a second time in ascending order in half-opacity to get
        # fully-colored bars that blend together when overlapping

        # get list of blocks that are on screen
        on_screen_blocks = [block for block in blocks
            if block['start_x'] < dimensions[0] and block['end_x'] > 0]

        # do first drawing pass
        for block in on_screen_blocks:
            draw_block(block, tracks, dimensions, draw, draw_mask)

        # do second drawing pass
        on_screen_blocks.reverse()
        for block in on_screen_blocks:
            draw_block(block, tracks, dimensions, draw_overlay)

        # stick two drawing passes on top of each other
        im.paste(im_overlay, None, mask)

        im.save(frame_save_dir + ("frame%05i.png" % frame))
        frame += 1
        # need to set speed
        speed = get_speed(speed_map, time)
        for block in blocks: # move blocks to left
            block['start_x'] -= speed
            block['end_x'] -= speed
        last_block_end -= speed # move video endpoint left as well
        percent = int(min((original_end - last_block_end) * 100.0
            / original_end, 100))
        if percent != last_percent:
            print percent, "% done"
        last_percent = percent

        time += (1/fps)

    print "Done!"

if __name__ == '__main__':
    main()
