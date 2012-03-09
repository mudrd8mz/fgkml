"""Converts FlightGear log file to KML Google map file

Usage: python fgkml.py <file>
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

(c) 2012 David Mudrak <david@mudrak.name>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
"""

import sys

def parse_log(filename, longpos, latpos, altpos):
    """Extracts longitude, latitude and altitude from the csv log file
    """
    import csv

    path = []
    reader = csv.reader(open(filename, "rb"), delimiter=",", quotechar='"')
    # the first line contains the csv header
    next(reader)
    for row in reader:
        path.append({"longitude":float(row[longpos]), "latitude":float(row[latpos]),
            "altitude":float(row[altpos])/3.280839895})
    return path

def make_kml(path, trackname):
    points = []
    for point in path:
        points.append("{0:.8f},{1:.8f},{2:8f}".format(point["longitude"], point["latitude"], point["altitude"]))
    coordinates = "        " + "\n        ".join(points)
    kmldata = {
            "mapname":"Flight track",
            "mapdescription":"",
            "trackname":trackname,
            "trackdescription":"",
            "startname":trackname + " - start",
            "startdescription":"Initial position",
            "startcoordinates":points[0],
            "coordinates":coordinates}
    return """ <?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<Document>
  <name>{mapname}</name>
  <description><![CDATA[{mapdescription}]]></description>
  <Style id="style1">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/mapfiles/ms2/micons/plane.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Style id="style2">
    <LineStyle>
      <color>73FF0000</color>
      <width>5</width>
    </LineStyle>
  </Style>
  <Placemark>
    <name>{trackname}</name>
    <description><![CDATA[<div dir="ltr">{trackdescription}</div>]]></description>
    <styleUrl>#style2</styleUrl>
    <LineString>
      <tessellate>0</tessellate>
      <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
      <coordinates>
{coordinates}
      </coordinates>
    </LineString>
  </Placemark>
  <Placemark>
    <name>{startname}</name>
    <description><![CDATA[<div dir="ltr">{startdescription}</div>]]></description>
    <styleUrl>#style1</styleUrl>
    <Point>
      <coordinates>{startcoordinates}</coordinates>
    </Point>
  </Placemark>
</Document>
</kml>""".format(**kmldata)

def main(argv=None):
    import getopt

    # check if explicit arguments were passed or not (eg in the interactive shell)
    if argv is None:
        argv = sys.argv
    # parse command line options
    try:
        opts, args = getopt.getopt(argv[1:], "ht:n:e:a:", ["help", "trackname=", "longpos=", "latpos=", "altpos="])
    except getopt.error, msg:
        print >>sys.stderr, msg
        print >>sys.stderr, "for help use --help"
        return 2
    # process options
    trackname = "Flight track"
    langpos = 1
    latpos = 2
    altpos = 3
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            return 0
        if o in ("-t", "--trackname"):
            trackname = a
        if o in ("-n", "--longpos"):
            langpos = a
        if o in ("-e", "--latpos"):
            latpos = a
        if o in ("-a", "--altpos"):
            altpos = a
    # process arguments
    if not args:
        print >>sys.stderr, "missing input CSV file"
        print >>sys.stderr, "for help use --help"
        return 2
    path = parse_log(args[0], langpos, latpos, altpos)
    if not path:
        print >>sys.stderr, "no path found"
        return 3
    print make_kml(path, trackname)

if __name__ == "__main__":
    sys.exit(main())
