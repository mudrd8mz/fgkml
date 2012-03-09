Google maps flight tracker for FlightGear
=========================================

A simple script that converts FlightGear log file to KML file that can be imported
to Google maps to visualise the flight path.

Usage
-----

Setup your FlightGear so that it logs the position of the aircraft during the flight.
Then provide the path to the created log file as a parameter for the fgkml.py script
and redirect the output to a KML file. Import the file into your Google map. Enjoy!

    python fgkml.py <file>
    python fgkml.py --trackname="KSFO to KLAX" <file>
    python fgkml.py --longpos=1 --latpos=2 --altpos=3 <file>

    --trackname, -t     The name of the track in the map
    --longpos, -n       The position of the longitude value in the log file row
    --latpos, -e        The position of the latitude value in the log file row
    --altpos, -a        The position of the altitude value in the log file row

Longitudes and latitudes must be in degrees written in decimal format like
-122.3735887 and 37.61883421, obtained from /position/longitude-deg and
/position/latitude-deg values in the FlightGear property tree.

The altitude is the altitude above sea level in feets, obtained from the
/position/altitude-ft property.

The default values for longpos, latpos and altpos are 1, 2 and 3 respectively.
Note that the position counting starts with 0 so the longpos is supposed to be
the second column in the log file by default.

Author
------

(c) 2012 David Mudrak <david@mudrak.name>

License
-------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
