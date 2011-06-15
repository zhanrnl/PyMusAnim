import os, sys, colorsys
import Image, ImageDraw, ImageColor
from MusAnimLexer import *

def color_tuple_to_ImageColor(color_tuple):
    color = [int(val * 255) for val in color_tuple]
    return "rgb(" + str(color)[1:-1] + ")"

def add_block_info(blocks, tracks, fps, speed, dimensions, min_pitch, max_pitch):
    """Adds essential information to each block dict in blocks, also returns
    last_block_end to tell when animation is over"""
    # need: start_time (seconds), end_time (seconds), pitch, track_num for each
    # block
    last_block_end = 0
    for block in blocks:
        time_offset = block['start_time'] + 0.0
        frame_offset = time_offset * fps
        x_offset = frame_offset * speed
        block['start_x'] = x_offset + dimensions[0]
        block['length'] = block['end_time'] - block['start_time'] + 0.0
        x_length = block['length'] * fps * speed
        block['end_x'] = block['start_x'] + x_length
        if block['end_x'] > last_block_end:
            last_block_end = block['end_x']
        y_middle = ((0.0 + max_pitch - block['pitch'])
                    / (max_pitch - min_pitch)) * dimensions[1]
        width = tracks[block['track_num']]['width']
        block['top_y'] = y_middle - (width / 2)
        block['bottom_y'] = y_middle + (width / 2)
    return blocks, last_block_end

def main():
    tracks = [
        {}, # dummy track if first track is just meta events
    	{ 'name': "t1",
          'color': (1, 0.3, 0.2),
          'width': 6
        },
        { 'name': "t2",
          'color': (0.13, 0.42, 1),
          'width': 6
        },
    ]

    input_midi_file = "tempochangetest01.MID"
    frame_save_dir = "genimg/contra101/"

    dimensions = 720, 480
    speed = 1.4 # in pixels per frame
    fps = 29.97
    # pitches to be displayed at bottom and top of screen
    min_pitch, max_pitch = 40, 80

    blocks = []
    lexer = MidiLexer()
    midi_events = lexer.lex(input_midi_file)
    print midi_events

    """for track in tracks:
        if 'color' in track:
            base_color = colorsys.rgb_to_hls(*track['color'])
            track['high_color'] = colorsys.hls_to_rgb(base_color[0], 0.9, base_color[2])

    # do some useful calculations on all blocks
    blocks, last_block_end = add_block_info(blocks, tracks, fps, speed,
        dimensions, min_pitch, max_pitch)
    original_end = last_block_end
    percent = 0
    last_percent = -1

    frame = 0 # for naming image files
    while last_block_end > (0 - speed): # generate frames while there are blocks on the screen
        im = Image.new("RGBA", dimensions, "black")
        draw = ImageDraw.Draw(im)
        for block in blocks:
            if block['start_x'] < dimensions[0] and block['end_x'] > 0: # test whether to draw block at all
                if block['start_x'] < (dimensions[0] / 2) and block['end_x'] > (dimensions[0] / 2):
                    # draw bright color
                    color = color_tuple_to_ImageColor(tracks[block['track_num']]['high_color'])
                else:
                    color = color_tuple_to_ImageColor(tracks[block['track_num']]['color'])
                draw.rectangle((block['start_x'], block['top_y'], block['end_x']-1, block['bottom_y']), color)
        im.save(frame_save_dir + ("frame%05i.png" % frame))
        frame += 1
        for block in blocks: # move blocks to left
            block['start_x'] -= speed
            block['end_x'] -= speed
        last_block_end -= speed # move video endpoint left as well
        percent = int(min((original_end - last_block_end) * 100.0 / original_end, 100))
        if percent != last_percent:
            print percent, "% done"
            pass
        last_percent = percent"""

    print "Done!"

if __name__ == '__main__':
    main()
