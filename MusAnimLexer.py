import sys

class MidiLexer:
    ticks_per_quarter = 0
    bpm = 120
    midi_events = []

    def __init__(self):
        pass

    def get_v_time(self, data):
        """Picks off the variable-length time from a block of data and returns
        both pieces as a tuple, with the time in seconds!"""
        i = 0
        time_bytes = []
        while (ord(data[i]) & 0x80) >> 7 == 1:
            time_bytes.append(ord(data[i]) & 0x7F)
            i += 1
        time_bytes.append(ord(data[i]) & 0x7F)
        time_bytes.reverse()
        d_time = 0
        for j in range(0, len(time_bytes)):
            d_time += (time_bytes[j] << j * 7)
        return d_time, data[i+1:]

    def read_midi_event(self, track_data, blocks, time, track_num):
        #print time, self.bpm
        if track_data[0] == '\xff':
            # event is meta event, we do nothing unless it's a tempo event
            if ord(track_data[1]) == 0x51:
                # tempo event, add to tempo_map
                bpm_temp = 60000000.0 / ((ord(track_data[3])<<16)
                    + (ord(track_data[4])<<8) + ord(track_data[5]))
                self.tempo_map.append((bpm_temp, time))
                #print self.tempo_map
                return track_data[6:], blocks
            else: # just skip past it and do nothing
                length = ord(track_data[2])
                return track_data[length+3:], blocks

        # otherwise we we assume it's a midi event
        elif ((ord(track_data[0]) & 0xF0) >> 4) == 0x8:
            # note off event
            pitch = ord(track_data[1]) # need to search for blocks with pitch
            blocks_w_pitch = [block for block in blocks
                if block['pitch'] == pitch and 'end_time' not in block]
            assert(len(blocks_w_pitch) > 0)
            blocks[blocks.index(blocks_w_pitch[0])]['end_time'] = ((time * 60.0)
                / (self.ticks_per_quarter * self.bpm))
            return track_data[3:], blocks

        elif ((ord(track_data[0]) & 0xF0) >> 4) == 0x9:
            # note on event
            blocks.append({'start_time': (time * 60.0)/(self.ticks_per_quarter
                * self.bpm), 'pitch': ord(track_data[1]),
                'track_num': track_num})
            return track_data[3:], blocks

        else:
            raise Exception("I don't want your damn lemons, " +
                            "what am I supposed to do with these")

    def set_tempo(self, time):
        """Sets self.bpm for a given time in ticks based on a tempo map in
        self.tempo_map"""
        if not self.tempo_map:
            self.bpm = 120
            return
        i = len(self.tempo_map) - 1
        while i > 1 and self.tempo_map[i][1] >= time:
            i -= 1
        self.bpm = self.tempo_map[i][0]

    def lex(self, filename):
        """Returns block list for musanim from a midi file given in filename"""
        import re

        # init stuff
        self.midi_events = []
        self.bpm = 120
        self.ticks_per_quarter = 960
        blocks = []

        # open and read file
        f = open(filename)
        s = f.read()

        # grab header
        header = s[0:14]
        f_format = ord(s[8]) << 8 | ord(s[9])
        num_tracks = ord(s[10]) << 8 | ord(s[11])
        self.ticks_per_quarter = ord(s[12]) << 8 | ord(s[13])

        tracks_chunk = s[14:]
        # individual track data as entries in list
        tracks = [track[4:] for track in re.split("MTrk", tracks_chunk)[1:]]
        track_num = 0
        for track in tracks:
            time = 0
            # parse midi events for a single track
            i = 0
            while len(track) > 0:
                if i < 10:
                    i+=1
                self.set_tempo(time) # from self.temp_map
                # get variable time that passes since last event
                d_time, track = self.get_v_time(track)
                time += d_time
                track, blocks = self.read_midi_event(track, blocks, time,
                    track_num)
            track_num += 1

        return blocks


if __name__ == '__main__':
    lexer = MidiLexer()
    blocks = lexer.lex('multitrackmidi01.MID')
    print blocks