# -*- coding: utf-8 -*-
import sys

class MidiLexer:
    ticks_per_quarter = 0
    bpm = 120
    # midi events just stores all relevant midi events and their global time in
    # beats, without making any pretenses about figuring out timing in seconds.
    # That has to be done later, once we have all the timing events sorted
    midi_events = []
    minPitch = sys.maxsize
    maxPitch = -sys.maxsize-1

    def debug(self, event):
        print('Unknown event: ' + bin(event) + " (" + hex(event) + ")")

    def get_v_time(self, data):
        """Picks off the variable-length time from a block of data and returns
        both pieces as a tuple, with the time in ticks"""
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

    def read_midi_event(self, track_data, time, track_num):
        # have to read off vtime first!
        d_time, track_data = self.get_v_time(track_data)
        time += d_time
        #print time
        event=((ord(track_data[0]) & 0xF0) >> 4)

        if track_data[0] == '\xff':
            # event is meta event, we do nothing unless it's a tempo event
            if ord(track_data[1]) == 0x51:
                # tempo event
                mpqn = ((ord(track_data[3]) << 16) + (ord(track_data[4]) << 8)
                    + ord(track_data[5])) # microseconds per quarter note
                bpm = 60000000.0 / mpqn
                self.midi_events.append({'type': 'tempo', 'time': time,
                    'bpm': bpm})
                return track_data[6:], time
            else: # just skip past it and do nothing
                length = ord(track_data[2])
                return track_data[length+3:], time

        # otherwise we we assume it's a midi event
        elif event == 0x8:
            # note off event
            # don't add a note off event if keyswitch (pitch below 12)
            pitch = ord(track_data[1])
            if pitch >= 12:
                self.midi_events.append({'type': 'note_off', 'time': time,
                    'pitch': pitch, 'track_num': track_num})
            return track_data[3:], time

        elif event == 0x9:
            # note on event
            pitch = ord(track_data[1])
            if pitch < 12: # it's a keyswitch!
                if pitch == 0:
                    mode = "normal"
                elif pitch == 1:
                    mode = "pizz"
                else:
                    print(("Unknown keyswitch: "+str(pitch)))
                    pitch=False
                if pitch != False:
                  self.midi_events.append({'type': 'keyswitch', 'time': time,
                      'track_num': track_num, 'mode': mode})
            else:
                if pitch > self.maxPitch:
                    self.maxPitch = pitch
                if pitch < self.minPitch:
                    self.minPitch = pitch
                self.midi_events.append({'type': 'note_on', 'time': time,
                    'pitch': ord(track_data[1]), 'track_num': track_num})
            return track_data[3:], time
        elif event == 0xC:
            return track_data[2:], time # ignore some other events
        elif event == 0xB:
            return track_data[3:], time
        #kek
        elif event == 0xF or event == 0xD:
            self.debug(event)
            return track_data[2:], time
        else:
            self.debug(event)
            return track_data[3:], time

    def lex(self, filename):
        """Returns block list for musanim from a midi file given in filename"""
        import re

        # init stuff
        self.midi_events = []
        self.bpm = 120
        self.ticks_per_quarter = 960
        blocks = []

        # open and read file
        f = open(filename, 'rb')
        s = f.read().decode('latin-1')

        # grab header
        header = s[0:14]
        f_format = ord(s[8]) << 8 | ord(s[9])
        self.num_tracks = ord(s[10]) << 8 | ord(s[11])
        self.ticks_per_quarter = ord(s[12]) << 8 | ord(s[13])

        tracks_chunk = s[14:]
        # individual track data as entries in list
        tracks = [track[4:] for track in re.split("MTrk", tracks_chunk)[1:]]
        track_num = 0
        for track in tracks:
            time = 0
            # parse midi events for a single track
            while len(track) > 0:
                # read off midi events and add to midi_events
                track, time = self.read_midi_event(track, time, track_num)
            track_num += 1

        # convert all times from ticks to beats, for convenience
        for event in self.midi_events:
            event['time'] = (event['time'] + 0.0) / self.ticks_per_quarter #960

        self.midi_events.sort(key=lambda a: a['time'])
        return self.midi_events


if __name__ == '__main__':
    lexer = MidiLexer()
    blocks = lexer.lex('multitrackmidi01.MID')
    print(blocks)
