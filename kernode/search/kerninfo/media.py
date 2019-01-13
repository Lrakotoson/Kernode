
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
        Ordexif = dict()
        exif = {
            PE.TAGS[cle]: val
            for cle, val in getattr(self.img, '_getexif', lambda: None)().items()
            if cle in PE.TAGS
        }

        if "GPSInfo" in exif:
            gpsinfo = dict()
            for cle in exif["GPSInfo"].keys():
                data = PE.GPSTAGS.get(cle, cle)
                gpsinfo[data] = exif["GPSInfo"][cle]
            Ordexif["GPS Informations"] = self._gpsconversion(gpsinfo)
            del exif["GPSInfo"]
        
        

        return Ordexif

    def _gpsconversion(self, gpsDMS):
        """
        Convert and sort gps informations
        gpsDMS: Dict of gpsinfo exif
        return: list of tuples (info, value)
        """
        gpsDD = list()
        if "GPSVersionID" in gpsDMS:
            version = str()
            for i in list(gpsDMS["GPSVersionID"]):
                version += "{}.".format(i)
            gpsDD.append(("GPS Version", version))

        if "GPSLatitude" in gpsDMS:
            gLtd = gpsDMS["GPSLatitude"]
            latitude = gLtd[0][0]/gLtd[0][1]+gLtd[1][0]/gLtd[1][1]/60 +\
                gLtd[2][0]/gLtd[2][1]/3600
            if gpsDMS["GPSLatitudeRef"].upper() == "S":
                latitude *= -1
            gpsDD.append(("Latitude", latitude))

        if "GPSLongitude" in gpsDMS:
            gLgt = gpsDMS["GPSLongitude"]
            longitude = gLgt[0][0]/gLgt[0][1]+gLgt[1][0]/gLgt[1][1]/60 +\
                gLgt[2][0]/gLgt[2][1]/3600
            if gpsDMS["GPSLongitudeRef"].upper() == "W":
                longitude *= -1
            gpsDD.append(("Longitude", longitude))

        if "GPSAltitude" in gpsDMS:
            gAlt = gpsDMS["GPSAltitude"]
            if int.from_bytes(gpsDMS["GPSAltitudeRef"], "big") == 1:
                level = "below"
            else:
                level = "above"
            altitude = "{} meters {} sea level".format(gAlt[0]/gAlt[1], level)
            gpsDD.append(("Altitude", altitude))

        if "GPSDateStamp" in gpsDMS:
            datestamp = dt.datetime.strptime(
                gpsDMS["GPSDateStamp"], "%Y:%m:%d").date()
            gpsDD.append(("Date Stamp", datestamp))

        if "GPSTimeStamp" in gpsDMS:
            gTstp = gpsDMS["GPSTimeStamp"]
            timestamp = dt.datetime.strptime("{}:{}:{}".format(
                int(gTstp[0][0]/gTstp[0][1]),
                int(gTstp[1][0]/gTstp[1][1]),
                int(gTstp[2][0]/gTstp[2][1])),
                "%H:%M:%S").time()
            gpsDD.append(("Time Stamp", timestamp))

        if "GPSImgDirection" in gpsDMS:
            gImg = gpsDMS["GPSImgDirection"]
            if gpsDMS["GPSImgDirectionRef"] == "M":
                ref = "Magnetic"
            else:
                ref = "True"
            imgdir = "{} : ref {} North".format(gImg[0]/gImg[1], ref)
            gpsDD.append(("Image Direction", imgdir))

        return gpsDD


    def _generalinfo(self, brutexif):
        netexif = list()
        generalist = ["ExifVersion","Make", "Model"]
        pass