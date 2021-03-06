import math

class SpectralData(object):
    """Stores and processes Spectral Data
        Attributes:
            darkWavelengths : float[]
                An array of wavelengths taken from the background
            darkSpectra : float[]
    """
    def __init__(self, darkWavelengths = [], darkSpectra = [], referenceWavelengths = [],
    referenceSpectra = [], sampleWavelengths = [], sampleSpectra = [], isReferenceAdjusted = False):
        self.darkWavelengths = darkWavelengths
        self.darkSpectra = darkSpectra
        if len(self.darkSpectra) > 0 and len(self.darkWavelengths) > 0:
            self.hasBackground = True
        else:
            self.hasBackground = False

        self.referenceWavelengths = referenceWavelengths
        self.referenceSpectra = referenceSpectra
        if len(self.referenceSpectra) > 0 and len(self.referenceWavelengths) > 0:
            self.hasReference = True
        else: 
            self.hasReference = False

        self.sampleWavelengths = sampleWavelengths
        self.sampleSpectra = sampleSpectra
        if len(self.sampleSpectra) > 0 and len(self.sampleWavelengths) > 0:
            self.hasSample = True
        else:
            self.hasSample = False

        self.isReferenceAdjusted = isReferenceAdjusted

    def setDark(self, spectra, wavelengths):
        print("1")
        self.darkSpectra = spectra
        print("2")
        self.darkWavelengths = wavelengths
        print("3")
        self.hasBackground = True
        self.isReferenceAdjusted = False

    def setReference(self, spectra, wavelengths):
        self.referenceSpectra = spectra
        self.referenceWavelengths = wavelengths
        self.hasReference = True

    def setSample(self, spectra, wavelengths):
        self.sampleSpectra = spectra
        self.sampleWavelengths = wavelengths
        self.hasSample = True

    @staticmethod
    def createJson(testMode, errorCode, spectra, wavelengths):
        stringBuilder = []
        stringBuilder.append("{\n\t\"testMode\": ")
        stringBuilder.append("\"")
        stringBuilder.append(str(testMode))
        stringBuilder.append("\",\n\t\"errorCode\": ")
        stringBuilder.append(str(errorCode))
        stringBuilder.append(",\n\t\"wavelengths\": [")
        for i in range(len(wavelengths) - 1):
            stringBuilder.append(str(wavelengths[i]))
            stringBuilder.append(", ")
        
        stringBuilder.append(str(wavelengths[len(wavelengths) - 1]))
        stringBuilder.append("],\n\t\"spectra\": [")
        for i in range(len(spectra) - 1):
            stringBuilder.append(str(spectra[i]))
            stringBuilder.append(", ") 

        stringBuilder.append(str(spectra[len(spectra) - 1]))
        stringBuilder.append("]\n}")
        sendString = ''.join(stringBuilder)
        return sendString

    def subtractBackground(self, collectionType = "Reference"):
        if collectionType == "Reference":
            if self.hasBackground and self.hasReference:
                for i in range(0, len(self.referenceSpectra)):
                    self.referenceSpectra[i] = self.referenceSpectra[i] - self.darkSpectra[i]

                self.isReferenceAdjusted = True        

        elif collectionType == "Sample":
            if self.hasBackground and self.hasSample:
                for i in range(0, len(self.sampleSpectra)):
                    self.sampleSpectra[i] = self.sampleSpectra[i] - self.darkSpectra[i]            

    def calculateGraph(self, testMode = "Background"):
        if testMode == "Background":
            return [self.darkSpectra, self.darkWavelengths]

        elif testMode == "Reference":
            self.subtractBackground()
            return [self.referenceSpectra, self.referenceWavelengths]

        elif testMode == "Absorbance":
            if not self.hasReference:
                return
            
            if not self.isReferenceAdjusted:
                self.subtractBackground()

            if self.hasBackground and self.hasSample:
                for i in range(0, len(self.sampleSpectra)):
                    tmpPoint = (self.sampleSpectra[i] - self.darkSpectra[i])
                    if self.referenceSpectra[i] == 0:
                        tmpPoint = 1
                    else:
                        tmpPoint = float(tmpPoint) / float(self.referenceSpectra[i])
                        if tmpPoint != 0:
                            tmpPoint = 20 * math.log10(abs(tmpPoint))
                    self.sampleSpectra[i] = tmpPoint
                    
        elif testMode == "Reflectance":
            if not self.hasReference:
                return
            
            if not self.isReferenceAdjusted:
                self.subtractBackground()

            if self.hasBackground and self.hasSample:
                for i in range(0, len(self.sampleSpectra)):
                    tmpPoint = (self.sampleSpectra[i] - self.darkSpectra[i])
                    if self.referenceSpectra[i] == 0:
                        tmpPoint = 1
                    else:
                        tmpPoint = float(tmpPoint) / float(self.referenceSpectra[i])
                    self.sampleSpectra[i] = tmpPoint
                    
        elif testMode == "Transmission":
            if not self.hasReference:
                return
            
            if not self.isReferenceAdjusted:
                self.subtractBackground()

            if self.hasBackground and self.hasSample:
                for i in range(0, len(self.sampleSpectra)):
                    tmpPoint = (self.sampleSpectra[i] - self.darkSpectra[i])
                    if self.referenceSpectra[i] == 0:
                        tmpPoint = 1
                    else:
                        tmpPoint = float(tmpPoint) / float(self.referenceSpectra[i])
                    self.sampleSpectra[i] = tmpPoint
                    
        elif testMode == "Fluorescence":
            if self.hasBackground and self.hasSample:
                for i in range(0, len(self.sampleSpectra)):
                    tmpPoint = (self.sampleSpectra[i] - self.darkSpectra[i])
                    self.sampleSpectra[i] = tmpPoint
