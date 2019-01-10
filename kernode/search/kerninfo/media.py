#!/usr/bin/env python

from PIL import Image as PI, ExifTags as PE

class Picture:
    def __init__(self, image):
        self.img = PI.open(image)
        self.exif = {}
    
    def _Pgetexif(self):
        """
        1 - extract exif from image
        2 - extract gps info from exif
        3 - extract photograph info from exif
        return: ordered Picture exif 
        """
        exif = {
            PE.TAGS[cle]:val
            for cle, val in self.img._getexif().items()
            if cle in PE.TAGS
        }
        

        if "GPSInfo" in exif:
            gpsinfo = {}
            for cle in exif["GPSInfo"].keys():
                data = PE.GPSTAGS.get(cle,cle)
                gpsinfo[data] = exif["GPSInfo"][cle]
            self.exif["Informations GPS"] = self._gpsconversion(gpsinfo)
            del exif["GPSInfo"]
        
        pass
    
    def _gpsconversion(self, gpsDMS):
        gpsDD = {}
        if "GPSLatitude" in gpsDMS:
            gLtd = gpsDMS["GPSLatitude"]
            gpsDD["Latitude"] = gLtd[0][0]/gLtd[0][1]+gLtd[1][0]/gLtd[1][0]/60+gLtd[2][0]/gLtd[2][1]/3600
            if gpsDMS["GPSLatitudeRef"].upper() == "S": gpsDD["Latitude"] *= -1

        if "GPSLongitude" in gpsDMS:
            gLgt = gpsDMS["GPSLongitude"]
            gpsDD["Longitude"] = gLgt[0][0]/gLgt[0][1]+gLgt[1][0]/gLgt[1][0]/60+gLgt[2][0]/gLgt[2][1]/3600
            if gpsDMS["GPSLongitudeRef"].upper() == "W": gpsDD["Longitude"] *= -1
        
        if "GPSAltitude" in gpsDMS:
            gAlt = gpsDMS["GPSAltitude"]
            if int.from_bytes(gpsDMS["GPSAltitudeRef"],"big") == 0:
                level = "above"
            else:
                level = "below"
            gpsDD["Altitude"] = "{} meters {} sea level".format(gAlt[0]/gAlt[1],level)




        
        
        


        return gpsDD
