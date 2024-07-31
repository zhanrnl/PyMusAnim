# -*- coding: utf-8 -*-
import os
import sys
import colorsys
import cairo
import math
from collections import deque
from MusAnimLexer import MidiLexer

class MusAnimRenderer:
    first_highlight = False
  
    def lyrics_deque(self, lyrics):
        """Turns lyrics as a string into a lyrics deque, splitting by spaces and
        removing newlines."""
        lyrics = lyrics.replace("\n", " ")
        lyrics_list = lyrics.split(" ")
        lyrics_list2 = []
        for word in lyrics_list:
            """
            if word and word[-1] == '-':
                word = word[0:-1] + ' -'"""
            lyrics_list2.append(word)
        return deque(lyrics_list2)

    def blockify(self, midi_events):
        """Converts list of midi events given by the lexer into block data used
        for animating."""
        blocks = []
        bpm = 120.0
        time_seconds = 0
        time_beats = 0
        tracks_mode = ['normal'] * 100
        for event in midi_events:
            # increment times based on elapsed time in beats
            d_time_beats = event['time'] - time_beats
            time_seconds += (d_time_beats * 60.0) / bpm
            time_beats = event['time']
            if event['type'] == 'tempo': # set tempo
                bpm = event['bpm']
            elif event['type'] == 'note_on': # create new block in list
                blocks.append({'start_time': time_seconds, 'pitch':
                    event['pitch'], 'track_num': event['track_num']})
                # set shape of last block to bar or circle
                if tracks_mode[event['track_num']] == 'normal':
                    blocks[-1]['shape'] = 'bar'
                elif tracks_mode[event['track_num']] == 'pizz':
                    blocks[-1]['shape'] = 'circle'
                else:
                    raise Exception('Unknown track mode')
            elif event['type'] == 'note_off': # add end_time to existing block
                pitch = event['pitch']
                track_num = event['track_num']
                blocks_w_pitch = [block for block in blocks
                    if block['pitch'] == pitch and block['track_num']
                        == track_num and 'end_time' not in block]
                assert(blocks_w_pitch) # assume it has at least one element
                # otherwise we have a faulty midi file!
                blocks_w_pitch[0]['end_time'] = time_seconds
            elif event['type'] == 'keyswitch':
                tracks_mode[event['track_num']] = event['mode']
            else:
                raise Exception('Unknown midi event')
        return blocks

    def add_block_info(self, blocks, tracks, fps, speed_map, dimensions,
        min_pitch, max_pitch):
        """Adds essential information to each block dict in blocks, also returns last_block_end to tell when animation is over"""
        # need: start_time (seconds), end_time (seconds), pitch, track_num for
        # each block
        last_block_end = 0
        cur_speed = self.get_speed(speed_map, 0.0)

        for block in blocks:
            # get track object that corresponds to block
            track = tracks[block['track_num']]
            block['width'] = track['width'] # set width
            # get speed and calculate x offset from functions
            cur_speed = self.get_speed(speed_map, block['start_time'])
            x_offset = self.calc_offset(speed_map, block['start_time'], fps)
            block['start_x'] = x_offset + dimensions[0]
            # length of the block in time (time it stays highlighted)
            block['length'] = block['end_time'] - block['start_time'] + 0.0
            # if a circle, length is same as width, otherwise length
            # corresponds to time length
            if block['shape'] == 'circle':
                block['x_length'] = block['width']
            else:
                block['x_length'] = block['length'] * fps * cur_speed
            block['end_x'] = block['start_x'] + block['x_length']
            # set last_block_end as the end_x of the very rightmost block
            if block['end_x'] > last_block_end:
                last_block_end = block['end_x']
            # figure out draw coordinates
            y_middle = ((0.0 + max_pitch - block['pitch']) / (max_pitch -
                min_pitch)) * dimensions[1]
            block['top_y'] = y_middle - (block['width'] / 2)
            block['bottom_y'] = y_middle + (block['width'] / 2)
            if 'z-index' not in track:
                track['z-index'] = 0
            block['z-index'] = track['z-index']
            if 'layer' not in track:
                track['layer'] = 0
            block['layer'] = track['layer']
            # round stuff for crisp rendering
            #block['x_length'] = round(block['x_length'])
            block['top_y'] = round(block['top_y'])
            #block['start_x'] = round(block['start_x'])

        # sort by track_num so we get proper melisma length counting
        blocks.sort(key=lambda a: a['track_num'])

        # can't add lyrics until we add in end_x for all blocks
        block_num = 0
        for block in blocks:
            track_num = block['track_num']
            track = tracks[block['track_num']]
            if 'lyrics' in track and track['lyrics'][0]:
                lyrics_text = track['lyrics'][0]
                if lyrics_text[0] == '^':
                    lyrics_text = lyrics_text[1:]
                    block['lyrics_position'] = 'above'
                elif lyrics_text[0] == '_':
                    lyrics_text = lyrics_text[1:]
                    block['lyrics_position'] = 'below'
                else:
                    block['lyrics_position'] = 'middle'

                if track['lyrics'][0] != '*':
                    # for detecting melismas (* in lyrics text)
                    i = 0
                    while (len(track['lyrics']) > (i + 1)
                        and track['lyrics'][i+1] == '*'):
                        i += 1
                    block['lyrics_end_x'] = blocks[block_num+i]['end_x']
                    block['lyrics'] = lyrics_text

                track['lyrics'].popleft()

            block_num += 1

        # go back to sorting by start time
        blocks.sort(key=lambda a: a['start_time'])

        return blocks, last_block_end

    def calc_offset(self, speed_map, time_offset, fps):
        """Calculates the x-offset of a block given its time offset and a speed map. Needed for laying out blocks because of variable block speed in the animation."""
        x_offset = 0
        i = 0
        # speed is a dict with a speed and a time when we switch to speed
        speeds = ([speed for speed in speed_map if speed['time'] < time_offset]
            [0:-1])
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

    def get_speed(self, speed_map, time):
        """Retrieves the correct block speed for a given point in time from the
        speed map."""
        i = len(speed_map) - 1
        while time < speed_map[i]['time'] and i > 0:
            i -= 1
        return speed_map[i]['speed']

    def draw_block_cairo(self, block, tracks, dimensions, cr, transparent=False):
        middle=dimensions[0] / 2
        start=block['start_x']
        if start< middle and block['end_x'] > middle:
            color = tracks[block['track_num']]['color' if self.dynamicmode else 'high_color']
            self.first_highlight = True
        else:
            color = tracks[block['track_num']]['color']
            transparent=transparent or self.dynamicmode
        if transparent:
            alpha=0.5
            if self.dynamicmode:
              alpha=block['end_x']#block position
              alpha=2*(middle-alpha)#distance from middle
              alpha=1-(alpha/middle)#percentage
              alpha=alpha/3.0#force past blocks to be at most 33% opaque
            cr.set_source_rgba(color[0], color[1], color[2], alpha)
        else:
            cr.set_source_rgb(*color)
        if block['shape'] == 'circle':
            halfwidth=block['width']/2
            cr.arc(start + halfwidth, block['top_y'] + halfwidth, halfwidth, 0, 2 * math.pi)
        else:
            cr.rectangle(start, block['top_y'], block['x_length'],
                block['width'])
        cr.fill()

    def draw_lyrics_cairo(self, block, tracks, dimensions, cr):
        cr.set_font_size(1.9*block['width'])
        text = block['lyrics']
        x_bearing, y_bearing, width, height = cr.text_extents(text)[:4]
        cr.set_source_rgba(0, 0, 0, 0.5)
        if block['lyrics_position'] == 'above':
            rect = (block['start_x'], int(block['top_y'])-0.7*block['width'], width + 2, block['width']+1)
        elif block['lyrics_position'] == 'below':
            rect = (block['start_x'], int(block['top_y'])+0.7*block['width'], width + 2, block['width']+1)
        else:
            rect = (block['start_x'], int(block['top_y']), width + 2, block['width']+1)
        cr.rectangle(*rect)
        cr.fill()
        if block['start_x'] < (dimensions[0] / 2) and (block['lyrics_end_x'] >
            (dimensions[0] / 2)):
            color = (1, 1, 1)
        else:
            color = tracks[block['track_num']]['lyrics_color']
        cr.set_source_rgb(*color)
        if block['lyrics_position'] == 'above':
            corner = (block['start_x'] + 1, block['top_y']+0.18*block['width'])
        elif block['lyrics_position'] == 'below':
            corner = (block['start_x'] + 1, block['top_y']+1.58*block['width'])
        else:
            corner = (block['start_x'] + 1, block['top_y']+0.88*block['width'])
        cr.move_to(*corner)
        cr.show_text(text)

    speed_map=[{'time':0.0,'speed':4}]
    width=720
    height=480
    fps=29.97
    min_pitch=34
    max_pitch=86
    first_frame=None
    last_frame=None
    every_nth_frame=1
    do_render=1
    introduction=True
  
    def render(self, input_midi_filename, frame_save_dir, tracks, speed_map=speed_map,dimensions=(width, height), fps=fps, min_pitch=min_pitch, max_pitch=max_pitch, first_frame=first_frame,last_frame=last_frame, every_nth_frame=every_nth_frame, do_render=do_render,dynamicmode=False):
        self.dynamicmode=dynamicmode
        """Render the animation!"""
        print("Beginning render...")
        speed = speed_map[0]['speed']
        if first_frame == None:
            first_frame = 0
        if last_frame == None:
            last_frame = 10000000 # just a large number

        print("Lexing midi...")
        blocks = []
        lexer = MidiLexer()
        midi_events = lexer.lex(input_midi_filename)

        print("Blockifying midi...")
        blocks = self.blockify(midi_events) # convert into list of blocks
        print(str(len(blocks))+" blocks")

        for track in tracks:
            if 'color' in track:
                base_color = colorsys.rgb_to_hls(*track['color'])
                track['high_color'] = colorsys.hls_to_rgb(base_color[0], 0.95,
                    base_color[2])
                track['lyrics_color'] = colorsys.hls_to_rgb(base_color[0], 0.7,
                    base_color[2])
            if 'lyrics' in track:
                track['lyrics'] = self.lyrics_deque(track['lyrics'])

        # do some useful calculations on all blocks
        blocks, last_block_end = self.add_block_info(blocks, tracks,
            fps, speed_map, dimensions, min_pitch, max_pitch)

        # following used for calculating percentage done to print to console
        original_end = last_block_end
        percent = 0
        last_percent = -1

        # sort by z-index descending
        blocks.sort(key=lambda a: a['z-index'],reverse=True)

        # for naming image files:
        frame = 0
        framefile = 0
        # for keeping track of speed changes:
        # need to initialize time
        time = -dimensions[0]/(2.0*fps*speed_map[0]['speed'])

        if not do_render:
            print("Skipping render pass, Done!")
            return

        print("Rendering frames...")
        # generate frames while there are blocks on the screen:
        while last_block_end > -speed:
            # code only for rendering blocks
            if first_frame < frame and frame <= last_frame and frame % every_nth_frame == 0:
                # cairo setup stuff
                filename = frame_save_dir + ("frame%05i.png" % framefile)
                surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *dimensions)
                cr = cairo.Context(surface)
                cr.set_antialias(cairo.ANTIALIAS_GRAY)
                cr.select_font_face("Garamond", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size(19)
                # add black background
                cr.set_source_rgb(0, 0, 0)
                cr.rectangle(0, 0, *dimensions)
                cr.fill()

                '''need to do two passes of drawing blocks, once in reverse order in full opacity, and a second time in ascending order in half-opacity to get fully-colored bars that blend together when overlapping'''

                # get list of blocks that are on screen
                on_screen_blocks = [block for block in blocks
                    if block['start_x'] < dimensions[0]]
                
                for layer in {block['layer'] for block in on_screen_blocks}:
                    layer_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *dimensions)
                    layer_context = cairo.Context(layer_surface)
                    
                    in_layer_blocks = [block for block in on_screen_blocks if block['layer'] == layer]
                        
                    # do first drawing pass
                    for block in in_layer_blocks:
                        block=self.makedynamic(block, dimensions)
                        if block==None:
                          continue
                        self.draw_block_cairo(block, tracks, dimensions, layer_context)

                    # do second drawing pass
                    on_screen_blocks.reverse()
                    for block in in_layer_blocks:
                        block=self.makedynamic(block, dimensions)
                        if block==None:
                          continue
                        self.draw_block_cairo(block, tracks, dimensions, layer_context, transparent=True)
                        
                    cr.set_source_surface(layer_surface)
                    cr.paint()

                # do lyrics pass, sort by start x so starts of words are on top
                on_screen_blocks.sort(key=lambda a: a['start_x'])
                for block in on_screen_blocks:
                    if ('lyrics' in block):
                        self.draw_lyrics_cairo(block, tracks, dimensions, cr)

                if self.introduction or self.first_highlight:
                    framefile += 1
                    surface.write_to_png(filename)

            # other code needed to advance animation
            frame += 1
            # need to set speed
            speed = self.get_speed(speed_map, time)
            for block in list(blocks): # move blocks to left
                end=block['end_x']-speed
                if end<0: 
                  '''trash blocks no longer needed. benchmark shows this causes a 2% increase in processing time in medium-sized files (~1000 blocks) but up to 15% redution in big files (~10000 blocks)'''
                  blocks.remove(block)
                  continue
                block['end_x'] = end
                block['start_x'] -= speed
                if 'lyrics_end_x' in block:
                    block['lyrics_end_x'] -= speed
            last_block_end -= speed # move video endpoint left as well
            percent = min(int((original_end - last_block_end) * 100.0
                / original_end), 100)
            if percent != last_percent:
                print(percent, "% done")
            last_percent = percent

            time += (1/fps)

        print("Done!")


    def makedynamic(self, block, dimensions):
        if self.dynamicmode:
          middle=dimensions[0] / 2
          if block['start_x'] > middle:
            return None
          if block['end_x'] > middle:
            block=block.copy()
            shorten=block['end_x']-(middle+1)
            block['end_x']-=shorten
            block['x_length']-=shorten
            return block
        return block

if __name__ == '__main__':
    print ("Sorry, I don't really do anything useful as an executable, see "
        "RunAnim.py for usage")
