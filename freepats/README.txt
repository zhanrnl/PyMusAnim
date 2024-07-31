This is a utility you can use to help fill missing sound patches for Timidity's Freepats in case your output or log files shows they are missing. An example file is provided that already fills some missing instruments with similar ones.

Unfortunately Freepats hasn't been updated since 2006 so unless you're willing to create or find new sound patches yourself this is the best workaround that I could find.

In Debian the following paths are relevant:

  /etc/timidity/ (where to place your new freepats.cfg)
  /usr/share/midi/freepats/ (location of .pat files - you may need to update the freepats.cfg if this is different in your system)
