import MidiLexer

if __name__ == '__main__':
    midi_file = MidiLexer.lex("simplescale.MID")
    MidiLexer.add_time_seconds(midi_file)
    for event in midi_file.events:
        print str(event)