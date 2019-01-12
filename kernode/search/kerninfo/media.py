#!/usr/bin/env python
import datetime as dt
from PIL import Image as PI, ExifTags as PE

class Picture:
    def __init__(self, image):
        self.img = PI.open(image)
        self.exif = self._Pgetexif()
    
    def _Pgetexif(self):
        """
        1 - extract exif from image
        2 - extract gps info from exif
        3 - extract photograph info from exif
        return: ordered Picture exif 
        """
        Ordexif = {}
        exif = {
            PE.TAGS[cle]:val
            for cle, val in getattr(self.img, '_getexif', lambda: None)().items()
            if cle in PE.TAGS
        }
        

        if "GPSInfo" in exif:
            gpsinfo = {}
            for cle in exif["GPSInfo"].keys():
                data = PE.GPSTAGS.get(cle,cle)
                gpsinfo[data] = exif["GPSInfo"][cle]
            Ordexif["Informations GPS"] = self._gpsconversion(gpsinfo)
            del exif["GPSInfo"]
        
        return Ordexif
    
    def _gpsconversion(self, gpsDMS):
        gpsDD = {}
        if "GPSLatitude" in gpsDMS:
            gLtd = gpsDMS["GPSLatitude"]
            gpsDD["Latitude"] = gLtd[0][0]/gLtd[0][1]+gLtd[1][0]/gLtd[1][0]/60+\
                                gLtd[2][0]/gLtd[2][1]/3600
            if gpsDMS["GPSLatitudeRef"].upper() == "S": gpsDD["Latitude"] *= -1

        if "GPSLongitude" in gpsDMS:
            gLgt = gpsDMS["GPSLongitude"]
            gpsDD["Longitude"] = gLgt[0][0]/gLgt[0][1]+gLgt[1][0]/gLgt[1][0]/60+\
                                gLgt[2][0]/gLgt[2][1]/3600
            if gpsDMS["GPSLongitudeRef"].upper() == "W": gpsDD["Longitude"] *= -1
        
        if "GPSAltitude" in gpsDMS:
            gAlt = gpsDMS["GPSAltitude"]
            if int.from_bytes(gpsDMS["GPSAltitudeRef"],"big") == 1:
                level = "below"
            else:
                level = "above"
            gpsDD["Altitude"] = "{} meters {} sea level".format(gAlt[0]/gAlt[1],level)

        if "GPSTimeStamp" in gpsDMS:
            gTstp = gpsDMS["GPSTimeStamp"]
            gpsDD["Time stamp"] = dt.datetime.strptime("{}:{}:{}".format(
                                                int(gTstp[0][0]/gTstp[0][1]),
                                                int(gTstp[1][0]/gTstp[1][1]),
                                                int(gTstp[2][0]/gTstp[2][1])),
                                                "%H:%M:%S")

        if "GPSDateStamp" in gpsDMS:
            gpsDD["Date stamp"] = dt.datetime.strptime(gpsDMS["GPSDateStamp"],"%Y:%m:%d")
        
        if "GPSImgDirection" in gpsDMS:
            gImg = gpsDMS["GPSImgDirection"]
            if gpsDMS["GPSImgDirectionRef"] == "M":
                ref = "Magnetic"
            else:
                ref = "True"
            gpsDD["Image Direction"] = "{} : ref {} North".format(gImg[0]/gImg[1], ref)
        

        return gpsDD
