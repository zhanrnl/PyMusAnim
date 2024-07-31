# -*- coding: utf-8 -*-
#fills missing freepats.cfg tones with existing one from same group
import sys

GROUP_START=[0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120]

def addLine(line):
  print line + " #filled"

def write(line):
  sys.stdout.write(line)

def getTone(split):
  return split[1][:-1]

def fillLine(number,file):
  addLine(' ' + str(number) + '\t' + file)

class FillFreepats:
  process=False
  tone=0
  last=False

  def nextTone(self):
    self.tone+=1
    if self.tone in GROUP_START:
      self.last=False
      print

  def readLine(self,line):
    if line=="\n":
      return
    if not (line.startswith('dir') or line.startswith('#')):
      if line.startswith('bank'):
	self.process=True
      elif self.process:
	split=line.split('\t')
	lineTone=split[0].lstrip()
	if str(self.tone)!=lineTone:
	  while self.tone<int(lineTone):
	    if self.last:
	      tone=self.last
	    else:
	      tone=getTone(split)
	    fillLine(self.tone,tone)
	    self.nextTone()
	self.last=getTone(split)
	self.nextTone()
    write(line)

if len(sys.argv)<2:
  print "Usage: python FillFreepats.py path_to_freepats.cfg"

fill=FillFreepats();
for line in open(sys.argv[1],'r'):
  fill.readLine(line)
for tone in range(fill.tone,128):
  fillLine(tone,fill.last)
for drumset in range(1,49):
  addLine('drumset ' + str(drumset))
  addLine(' #extension copydrumset 0')