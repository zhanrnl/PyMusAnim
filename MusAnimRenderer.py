import os, sys, colorsys
import Image, ImageDraw, ImageColor, ImageFont
from MusAnimLexer import MidiLexer
from collections import deque

class MusAnimRenderer:
    def lyrics_deque(self, lyrics):
        """Turns lyrics as a string into a lyrics deque, splitting by spaces and
        removing newlines."""
        lyrics = lyrics.replace("\n", " ")
        lyrics_list = lyrics.split(" ")
        lyrics_list2 = []
        for word in lyrics_list:
            if word and word[-1] == '-':
                word = word[0:-1] + ' -'
            lyrics_list2.append(word)
        return deque(lyrics_list2)

    def color_tuple_to_ImageColor(self, color_tuple):
        color = [int(val * 255) for val in color_tuple]
        return "rgb(" + str(color)[1:-1] + ")"

    def blockify(self, midi_events):
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
        """Adds essential information to each block dict in blocks, also returns
        last_block_end to tell when animation is over"""
        # need: start_time (seconds), end_time (seconds), pitch, track_num for
        # each block
        last_block_end = 0
        cur_speed = self.get_speed(speed_map, 0.0)

        for block in blocks:
            # get track object that corresponds to block
            track = tracks[block['track_num']]
            width = track['width'] # set width
            # get speed and calculate x offset from functions
            cur_speed = self.get_speed(speed_map, block['start_time'])
            x_offset = self.calc_offset(speed_map, block['start_time'], fps)
            block['start_x'] = x_offset + dimensions[0]
            # length of the block in time (time it stays highlighted)
            block['length'] = block['end_time'] - block['start_time'] + 0.0
            # if a circle, length is same as width, otherwise length
            # corresponds to time length
            if block['shape'] == 'circle':
                x_length = width
            else:
                x_length = block['length'] * fps * cur_speed
            block['end_x'] = block['start_x'] + x_length
            # set last_block_end as the end_x of the very rightmost block
            if block['end_x'] > last_block_end:
                last_block_end = block['end_x']
            # figure out draw coordinates
            y_middle = ((0.0 + max_pitch - block['pitch']) / (max_pitch -
                min_pitch)) * dimensions[1]
            block['top_y'] = y_middle - (width / 2)
            block['bottom_y'] = y_middle + (width / 2)
            block['z-index'] = track['z-index']

        # sort by track_num so we get proper melisma length counting
        blocks.sort(lambda a, b: cmp(a['track_num'], b['track_num']))

        # can't add lyrics until we add in end_x for all blocks
        block_num = 0
        for block in blocks:
            track_num = block['track_num']
            track = tracks[block['track_num']]
            if track['lyrics'][0]:

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
        blocks.sort(lambda a, b: cmp(a['start_time'], b['start_time']))

        return blocks, last_block_end

    def calc_offset(self, speed_map, time_offset, fps):
        """Calculates the x-offset of a block given its time offset and a speed
        map. Needed for laying out blocks because of variable block speed in the
        animation."""
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

    def draw_block(self, block, tracks, dimensions, draw, draw_mask=None):
        """Draws a block onto an ImageDraw object given in draw from data in
        block dict."""
        if block['start_x'] < (dimensions[0] / 2) and (block['end_x'] >
            (dimensions[0] / 2)):
            color = self.color_tuple_to_ImageColor(tracks[block['track_num']]
                ['high_color'])
        else:
            color = self.color_tuple_to_ImageColor(tracks[block['track_num']]
                ['color'])
        if block['shape'] == 'circle':
            draw.ellipse((block['start_x'], block['top_y']-1, block['end_x']+2,
                block['bottom_y']+1), color)
            if draw_mask:
                draw_mask.ellipse((block['start_x'], block['top_y']-1,
                    block['end_x']+2, block['bottom_y']-1), "grey")
        else:
            draw.rectangle((block['start_x'], block['top_y'], block['end_x']-1,
                block['bottom_y']), color)
            if draw_mask:
                draw_mask.rectangle((block['start_x'], block['top_y'],
                    block['end_x']-1, block['bottom_y']), "grey")

    def draw_lyrics(self, block, tracks, dimensions, draw, mask, font):
        if block['lyrics_position'] == 'above':
            corner = (block['start_x'] + 2, block['top_y']-14)
        elif block['lyrics_position'] == 'below':
            corner = (block['start_x'] + 2, block['top_y'])
        else:
            corner = (block['start_x'] + 2, block['top_y']-7)
        text = block['lyrics']
        if block['start_x'] < (dimensions[0] / 2) and (block['lyrics_end_x'] >
            (dimensions[0] / 2)):
            color = "white"
        else:
            color = self.color_tuple_to_ImageColor(tracks[block['track_num']]
                ['lyrics_color'])
        draw.text(corner, text, font=font, fill=color)
        text_size = draw.textsize(text, font=font)
        if block['lyrics_position'] == 'above':
            rect = (block['start_x'], block['top_y']-7,
                block['start_x'] + text_size[0] + 3, block['bottom_y']-7)
        elif block['lyrics_position'] == 'below':
            rect = (block['start_x'], block['top_y']+7,
                block['start_x'] + text_size[0] + 3, block['bottom_y']+7)
        else:
            rect = (block['start_x'], block['top_y'],
                block['start_x'] + text_size[0] + 3, block['bottom_y'])
        mask.rectangle(rect, "grey")
        mask.text(corner, text, font=font, fill="white")

    def render(self, input_midi_filename, frame_save_dir, tracks, speed_map,
        dimensions, fps, min_pitch, max_pitch, first_frame=None,
        last_frame=None, do_render=1):

        print "Beginning render..."
        speed = speed_map[0]['speed']
        if first_frame == None:
            first_frame = 0
        if last_frame == None:
            last_frame = 1000000 # just a large number

        print "Lexing midi..."
        blocks = []
        lexer = MidiLexer()
        midi_events = lexer.lex(input_midi_filename)

        print "Blockifying midi..."
        blocks = self.blockify(midi_events) # convert into list of blocks

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
        blocks.sort(lambda a, b: cmp(b['z-index'], a['z-index']))

        # for naming image files:
        frame = 0
        # for keeping track of speed changes:
        # need to initialize time
        time = -dimensions[0]/(2.0*fps*speed_map[0]['speed'])

        if not do_render:
            print "Skipping render pass, Done!"
            return

        print "Rendering frames..."
        font = ImageFont.truetype('IMFePIrm29P.ttf', 18)
        # generate frames while there are blocks on the screen:
        while last_block_end > (0 - speed):
            if frame >= first_frame and frame <= last_frame:
                im = Image.new("RGBA", dimensions, "black")
                # overlay is for second drawing pass
                im_overlay = Image.new("RGBA", dimensions, "black")
                im_lyrics = Image.new("RGBA", dimensions, "black")

                draw = ImageDraw.Draw(im)
                draw_overlay = ImageDraw.Draw(im_overlay)
                lyrics_draw = ImageDraw.Draw(im_lyrics)

                # greyscale mask for compositing
                mask = Image.new("L", dimensions, "black")
                draw_mask = ImageDraw.Draw(mask)

                lyrics_mask = Image.new("L", dimensions, "black")
                lyrics_draw_mask = ImageDraw.Draw(lyrics_mask)

                # need to do two passes of drawing blocks, once in reverse order
                # in full opacity, and a second time in ascending order in half-
                # opacityto get fully-colored bars that blend together when
                # overlapping

                # get list of blocks that are on screen
                on_screen_blocks = [block for block in blocks
                    if block['start_x'] < dimensions[0] and block['end_x'] > 0]

                # do first drawing pass
                for block in on_screen_blocks:
                    self.draw_block(block, tracks, dimensions, draw, draw_mask)

                # do second drawing pass
                on_screen_blocks.reverse()
                for block in on_screen_blocks:
                    self.draw_block(block, tracks, dimensions, draw_overlay)

                # do lyrics pass
                for block in on_screen_blocks:
                    if ('lyrics' in block):
                        self.draw_lyrics(block, tracks, dimensions, lyrics_draw,
                            lyrics_draw_mask, font)

                # stick two drawing passes on top of each other
                im.paste(im_overlay, None, mask)
                im.paste(im_lyrics, None, lyrics_mask)

                im.save(frame_save_dir + ("frame%05i.png" % frame))
            frame += 1
            # need to set speed
            speed = self.get_speed(speed_map, time)
            for block in blocks: # move blocks to left
                block['start_x'] -= speed
                block['end_x'] -= speed
                if 'lyrics_end_x' in block:
                    block['lyrics_end_x'] -= speed
            last_block_end -= speed # move video endpoint left as well
            percent = int(min((original_end - last_block_end) * 100.0
                / original_end, 100))
            if percent != last_percent:
                print percent, "% done"
            last_percent = percent

            time += (1/fps)

        print "Done!"


if __name__ == '__main__':
    print ("Sorry, I don't really do anything useful as an executable, see "
        "RunAnim.py for usage")