from itertools import tee, izip_longest

# midi event types
NOTE_OFF = 0x8
NOTE_ON = 0x9
KEY_AFTERTOUCH = 0xA
CONTROL_CHANGE = 0xB
PROGRAM_CHANGE = 0xC
CHANNEL_AFTERTOUCH = 0xD
PITCH_BEND = 0xE
META = 0xF

# meta event types
SEQUENCE_NUMBER = 0x00
TEXT_EVENT = 0x01
COPYRIGHT_NOTICE = 0x02
TRACK_NAME = 0x03
INSTRUMENT_NAME = 0x04
LYRICS = 0x05
MARKER = 0x06
CUE_POINT = 0x07
CHANNEL_PREFIX = 0x20
END_OF_TRACK = 0x2F
SET_TEMPO = 0x51
SMPTE_OFFSET = 0x54
TIME_SIGNATURE = 0x58
KEY_SIGNATURE = 0x59

class MidiFile():
    def __init__(self, tpqn, events=[]):
        self.tpqn = tpqn
        self.events = events

class MidiEvent():
    def __init__(self, event_type, params):
        self.event_type = event_type
        self.params = params
    
    def __str__(self):
        class_name = str(self.__class__)
        class_name = class_name[class_name.find('.') + 1:]
        return "{:20}{}".format(class_name, self.__dict__)
        
class NoteOnEvent(MidiEvent):
    def __init__(self, pitch, velocity):
        self.pitch = pitch
        self.velocity = velocity
        
class NoteOffEvent(MidiEvent):
    def __init__(self, pitch, velocity):
        self.pitch = pitch
        self.velocity = velocity
        
class ControlChangeEvent(MidiEvent):
    def __init__(self, control_number, control_value):
        self.control_number = control_number  
        self.control_value = control_value
        
class ProgramChangeEvent(MidiEvent):
    def __init__(self, program):
        self.program = program

class TrackNameEvent(MidiEvent):
    def __init__(self, name):
        self.name = name

class EndOfTrackEvent(MidiEvent):
    def __init__(self):
        pass
        
class TempoEvent(MidiEvent):
    def __init__(self, microspqn):
        self.microspqn = microspqn
        self.bpm = 60000000.0 / self.microspqn  
        
class TimeSignatureEvent(MidiEvent):
    def __init__(self, numerator, denominator_power, metronome, thirtyseconds):
        self.numerator = numerator
        self.denominator = 2 ** denominator_power
        self.metronome = metronome
        self.thirtyseconds = thirtyseconds
        
class KeySignatureEvent(MidiEvent):
    def __init__(self, num_sharps, minor):
        # convert signed byte num_sharps into int:
        self.num_sharps = num_sharps - 256 * (num_sharps > 127)
        self.major = not bool(minor)

def pop_bytes(li, num_bytes):
    """Removes num_bytes number of bytes off the left side of list, then
    returns those bytes."""
    popped_bytes = li[:num_bytes]
    del li[:num_bytes]
    return popped_bytes

def pop_all_bytes(li):
    """Pops all the bytes of the list, returns basically a clone of the list
    while leaving the original list empty.""" 
    popped_bytes = li[:]
    del li[:]
    return popped_bytes
    
def pop_byte(li):
    return pop_bytes(li, 1)[0]

def bytes_to_int(li):
    """Converts a bytearray to an int, treating all the bytes as a single
    integer most significant byte first."""
    num = 0
    for i, b in enumerate(reversed(li)):
        num += (int(b) << (8 * i)) 
    return num
        
def open_midi_file(filename):
    f = open(filename, 'rb')
    return bytearray(f.read())

def get_header(midi_data):
    """Pops off the (always) 14-byte header from the midi file."""
    return pop_bytes(midi_data, 14)

def get_tpqn(header):
    """Grabs the ticks per quarter note data from the header chunk. The number
    is the last two bytes of the chunk, compute from values in the bytearray."""
    return bytes_to_int(header[12:])

def pop_track_chunk(midi_data):
    """Pops off bytes from midi_data until MTrk is seen, to return a block of
    data for a single midi track. If a following MTrk not seen, returns data to
    the end of the midi file."""
    if midi_data[:4] != 'MTrk': return None
    del midi_data[:8] # remove 'MTrk' and 4 more bytes for track chunk size
    num_bytes = midi_data.find('MTrk')
    if num_bytes == -1:
        return pop_all_bytes(midi_data)
    else:
        return pop_bytes(midi_data, num_bytes)

def highest_bit(byte):
    return byte >> 7

def lowest_seven_bits(byte):
    return byte & 0x7F

def highest_four_bits(byte):
    return byte >> 4

def lowest_four_bits(byte):
    return byte & 0x0F
    
def pop_dtime(midi_data):
    dtime = 0
    while True:
        dtime <<= 7
        byte = pop_byte(midi_data)
        dtime += lowest_seven_bits(byte)
        if not highest_bit(byte): break
    return dtime

def pop_command_byte(midi_data):
    byte = pop_byte(midi_data)
    command = highest_four_bits(byte)
    channel = lowest_four_bits(byte)
    return command, channel

def make_midi_event_obj(event_type, params):
    if event_type == NOTE_ON:
        return NoteOnEvent(*params)
    elif event_type == NOTE_OFF:
        return NoteOffEvent(*params)
    elif event_type == CONTROL_CHANGE:
        return ControlChangeEvent(*params)
    elif event_type == PROGRAM_CHANGE:
        return ProgramChangeEvent(*params)
    elif event_type == TRACK_NAME:
        return TrackNameEvent(str(params))
    elif event_type == END_OF_TRACK:
        return EndOfTrackEvent()
    elif event_type == SET_TEMPO:
        return TempoEvent(bytes_to_int(params))
    elif event_type == TIME_SIGNATURE:
        return TimeSignatureEvent(*params)
    elif event_type == KEY_SIGNATURE:
        return KeySignatureEvent(*params)
    return MidiEvent(event_type, params)

def pop_midi_event(midi_data):
    """Pops a midi event off the midi_data bytearray after dtime has already
    been popped. Begins constructing a MidiEvent object to put in the MidiFile's
    events list."""
    command_type, channel = pop_command_byte(midi_data)
    if command_type == META:
        meta_type, num_bytes = pop_bytes(midi_data, 2)
        data = pop_bytes(midi_data, num_bytes)
        return make_midi_event_obj(meta_type, data)
    else:
        if command_type in (PROGRAM_CHANGE, CHANNEL_AFTERTOUCH):
            num_bytes = 1
        else:
            num_bytes = 2
        params = list(pop_bytes(midi_data, num_bytes))
        return make_midi_event_obj(command_type, params)

def lex(filename):
    """Does lexical analysis on a midi file, returning a MidiFile object
    that contains the midi data in Python data structures. All midi events are
    stored in the midi_file.events list. lex() first pops off the header chunk,
    then while more data is found in the midi file, continues popping off track
    chunks, from each of those alternatively popping off delta-time and midi
    event blocks. MidiEvent objects are constructed and stored in
    midi_file.events after being labelled with their time and track number.""" 
    midi_data = open_midi_file(filename)
    header = get_header(midi_data)
    tpqn = get_tpqn(header)
    midi_file = MidiFile(tpqn)
    track_num = 0
    while midi_data:
        time_ticks = 0
        track_data = pop_track_chunk(midi_data)
        while track_data:
            time_ticks += pop_dtime(track_data)
            event = pop_midi_event(track_data)
            event.time_ticks = time_ticks
            event.track = track_num
            midi_file.events.append(event)
        track_num += 1
    return midi_file

def pairwise(iterable):
    """From itertools recipes. s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return izip_longest(a, b, fillvalue=None)

def get_tempo_map(midi_file):
    return filter(lambda e: isinstance(e, TempoEvent), midi_file.events)

def ticks_to_seconds(time_ticks, tempo_event, tpqn):
    quarters = (time_ticks + 0.0) / tpqn
    micros = quarters * tempo_event.microspqn
    return micros / 1000000

def ticks_to_seconds_multi(time_ticks, tempo_map, tpqn):
    seconds = 0.0
    for cur_tempo, next_tempo in pairwise(tempo_map):
        if not next_tempo or time_ticks < next_tempo.time_ticks:
            return seconds + ticks_to_seconds(time_ticks - cur_tempo.time_ticks, 
                                              cur_tempo, tpqn)
        seconds += ticks_to_seconds(next_tempo.time_ticks, cur_tempo, tpqn)

def add_time_seconds(midi_file):
    tempo_map = get_tempo_map(midi_file)
    for event in midi_file.events:
        event.time_seconds = ticks_to_seconds_multi(event.time_ticks, tempo_map,
                                                    midi_file.tpqn)
        
if __name__ == '__main__':
    midi_file = lex("testsimplemidi01.MID")
    add_time_seconds(midi_file)
    for event in midi_file.events:
        print str(event)