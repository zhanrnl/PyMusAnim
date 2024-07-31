# -*- coding: utf-8 -*-
from MusAnimRenderer import MusAnimRenderer
from MusAnimLexer import MidiLexer
import sys,os.path

PITCH_GRACE=5
TRACK_WIDTH=24

def main():
    tracks = [
	  { 'name': "track0",
	  'color': (0.000, 0.996, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track1",
	  'color': (0.996, 0.000, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track2",
	  'color': (0.004, 0.996, 0.992),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track3",
	  'color': (0.996, 0.855, 0.398),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track4",
	  'color': (0.563, 0.980, 0.570),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track5",
	  'color': (0.000, 0.461, 0.996),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track6",
	  'color': (0.832, 0.996, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track7",
	  'color': (0.996, 0.574, 0.492),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track8",
	  'color': (0.992, 0.535, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track9",
	  'color': (0.520, 0.660, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track10",
	  'color': (0.000, 0.680, 0.492),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track11",
	  'color': (0.738, 0.773, 0.996),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track12",
	  'color': (0.738, 0.824, 0.574),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track13",
	  'color': (0.000, 0.723, 0.090),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track14",
	  'color': (0.004, 0.813, 0.996),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track15",
	  'color': (0.566, 0.813, 0.793),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track16",
	  'color': (0.730, 0.531, 0.000),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track17",
	  'color': (0.867, 0.996, 0.453),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track18",
	  'color': (0.000, 0.996, 0.773),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track19",
	  'color': (0.996, 0.895, 0.008),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track20",
	  'color': (0.594, 0.996, 0.320),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track21",
	  'color': (0.000, 0.996, 0.469),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track22",
	  'color': (0.996, 0.430, 0.254),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track23",
	  'color': (0.645, 0.996, 0.820),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track24",
	  'color': (0.996, 0.691, 0.402),
	  'width': TRACK_WIDTH,
	  },
	  { 'name': "track25",
	  'color': (0.000, 0.605, 0.996),
	  'width': TRACK_WIDTH,
	  },
    ]
    
    ntracks=len(tracks)
    for i in range(ntracks):
      tracks[i]['z-index']=ntracks-i

    if len(sys.argv)<3:
      print("Usage: python MusAnimLauncher.py input.mid outputDirectory [--dynamic]")
      sys.exit(1)
      return

    mid=sys.argv[1]

    lexer = MidiLexer()
    lexer.lex(mid)

    frames_dir = sys.argv[2]+os.sep
    if not os.path.isdir(frames_dir):
        os.makedirs(frames_dir)
    
    dynamic=len(sys.argv)>=4 and sys.argv[3]=='--dynamic'

    speed_map = [{'time': 0.0, 'speed': 4}]

    dimensions = 1920, 1080
    #dimensions = 720, 480
    #dimensions = 426, 240

    fps = 25

    renderer=MusAnimRenderer()
    renderer.introduction=False
    renderer.render(mid,frames_dir,tracks,speed_map=speed_map,dimensions=dimensions,min_pitch=lexer.minPitch-PITCH_GRACE,max_pitch=lexer.maxPitch+PITCH_GRACE,fps=fps,dynamicmode=dynamic)

if __name__ == '__main__':
    main()
