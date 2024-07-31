#!/bin/bash
#Check batch.sh logs. Comment/uncomment/add lines to your needs.
if [ ! $1 ]; then
  echo "Usage: checklogs.sh logsDirectory"
  exit 1
fi

out=''
for log in $1/*.log; do
  error="`cat $log|grep -e"Aborting pymusanim.sh" -e"this instrument will not be heard" -e"Drum set .* is undefined"`"
  if [ "$error" ]; then
    #echo "$log: `echo $error|tail -n1`" #shows filename and first error (default, leave as only uncommented line upon commit)

    echo -e "${error}\n${log}\n\n`cat $log|grep -v '% done'|perl -ne '$H{$_}++ or print'`"|less #analyze each log showing error and filename as header and cleaning progress and duplicate lines

    #out=`echo -e "${out}\n${error}"|sort -u` #list each individual error
  fi
done
if [ "$out" ]; then
  echo "$out"
fi