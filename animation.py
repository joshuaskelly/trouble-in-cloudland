import pygame
import utility

class Animation:
    def __init__(self):
        self.sequenceDict = {}
        self.currentSequence = 0

        self.frameDict = {}
        self.currentFrame = 0

        self.isPlaying = True
        
        self.image = None
        
        self.parent = None
        
        
        
    def __repr__(self):
        return '<Animation(' + str(len(self.sequenceDict)) + ' Sequences): ' + str(self.sequenceDict.keys()) + '>'
    
    
    
    def __len__(self):
        return len(self.sequenceDict)
    
    
    
    def setParent(self, parent):
        self.parent = parent
        self.parent.image = self.sequenceDict[self.currentSequence][self.currentFrame]
    
    
    def update(self):
        if self.isPlaying:
            self.currentFrame += 1
        
        
        if self.currentFrame > (len(self.sequenceDict[self.currentSequence]) - 1):
            self.currentFrame = 0
            
        self.image = self.sequenceDict[self.currentSequence][self.currentFrame]
    
    
    def play(self, sequenceID, frameID = 0):
        self.isPlaying = True
        if self.currentSequence != sequenceID:
            self.currentSequence = sequenceID
            self.currentFrame = frameID
            
    
    
    def stop(self, sequenceID = None, frameID = 0):
        self.isPlaying = False
        
        if sequenceID:
            self.currentSequence = sequenceID
           
        if frameID:
            self.currentFrame = frameID
        
        
    
    
    def buildAnimation(self, sequenceID, frames):
        self.sequenceDict[sequenceID] = []
        if not self.currentSequence:
            self.currentSequence = sequenceID
        try:
            for frame in frames:
                try:
                    self.sequenceDict[sequenceID].append(self.frameDict[frame])
                    
                except:
                    self.frameDict[frame] = (utility.loadImage(frame))
                    self.sequenceDict[sequenceID].append(self.frameDict[frame])
        except:
            try:
                self.sequenceDict[sequenceID].append(self.frameDict[frames])
            except:
                self.frameDict[frames] = (utility.loadImage(frames))
                self.sequenceDict[sequenceID].append(self.frameDict[frames])
                
        self.image = self.sequenceDict[self.currentSequence][self.currentFrame]
        