from SimpleCV.base import *
from SimpleCV.ImageClass import Image
from SimpleCV.Features.HaarLikeFeature import *
from SimpleCV.Features.FeatureExtractorBase import *

class HaarLikeFeatureExtractor(FeatureExtractorBase):
    """
    This is used generate Haar like features from an image.  These
    Haar like features are used by a the classifiers of machine learning
    to help identify objects or things in the picture by their features,
    or in this case haar features.

    For a more in-depth review of Haar Like features see:
    http://en.wikipedia.org/wiki/Haar-like_features
    """

    mFeatureSet = None
    mDo45 = True
    def __init__(self, fname=None, do45=True):
        """
        fname - The feature file name
        do45 - if this is true we use the regular integral image plus the
        45 degree integral image
        """
        #we define the black (positive) and white (negative) regions of an image
        #to get our haar wavelet
        self.mDo45 = True
        self.mFeatureset=None;
        if(fname is not None):
            self.readWavelets(fname)

    def readWavelets(self, fname,nfeats=-1):
        """
        fname = file name
        nfeats = number of features to load from file -1 -> All features
        """
        # We borrowed the wavelet file from  Chesnokov Yuriy
        # He has a great windows tutorial here:
        # http://www.codeproject.com/KB/audio-video/haar_detection.aspx
        # SimpleCV Took a vote and we think he is an all around swell guy!
        # nfeats = number of features to load
        # -1 loads all
        # otherwise loads min(nfeats,features in file)
        self.mFeatureSet = []
        with open(fname,'r') as f:
            #line = f.readline()
            #count = int(line)
            temp = f.read()
        data = temp.split()
        count = int(data.pop(0))
        self.mFeatureset = []
        if(nfeats > -1):
            count = min(count,nfeats)
        while len(data) > 0:
            name = data.pop(0)
            nRegions = int(data.pop(0))
            region = []
            for _ in range(nRegions):
                region.append(tuple(map(float, data[:5])))
                data = data[5:]

            feat = HaarLikeFeature(name,region)
            self.mFeatureSet.append(feat)
        return None

    def saveWavelets(self, fname):
        """
        Save wavelets to file
        """
        with open(fname,'w') as f:
            f.write(str(len(self.mFeatureSet))+'\n\n')
            for i in range(len(self.mFeatureSet)):
                self.mFeatureSet[i].writeToFile(f)
        return None

    def extract(self, img):
        """
        This extractor takes in an image, creates the integral image, applies
        the Haar cascades, and returns the result as a feature vector.
        """
        regular = img.integralImage()
        retVal = [
            self.mFeatureSet[i].apply(regular)
            for i in range(len(self.mFeatureSet))
        ]


        if self.mDo45:
            slant = img.integralImage(tilted=True)
            retVal.extend(
                self.mFeatureSet[i].apply(regular)
                for i in range(len(self.mFeatureSet))
            )

        return retVal

    def getFieldNames(self):
        """
        This method gives the names of each field in the feature vector in the
        order in which they are returned. For example, 'xpos' or 'width'
        """
        retVal = [self.mFeatureSet[i].mName for i in range( len(self.mFeatureSet))]
        if self.mDo45:
            for i in range( len(self.mFeatureSet)):
                name = f"Angle_{self.mFeatureSet[i].mName}"
                retVal.append(name)
        return retVal


    def getNumFields(self):
        """
        This method returns the total number of fields in the feature vector.
        """
        mult = 2 if self.mDo45 else 1
        return mult*len(self.mFeatureset)
