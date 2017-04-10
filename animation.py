import pygame
import utility


class Animation:
    def __init__(self):
        self.sequence_dict = {}
        self.current_sequence = 0
        self.frame_dict = {}
        self.current_frame = 0
        self.is_playing = True
        self.image = None
        self.parent = None

    def __repr__(self):
        return '<Animation(' + str(len(self.sequence_dict)) + ' Sequences): ' + str(self.sequence_dict.keys()) + '>'

    def __len__(self):
        return len(self.sequence_dict)

    def set_parent(self, parent):
        self.parent = parent
        self.parent.image = self.sequence_dict[self.current_sequence][self.current_frame]

    def update(self):
        if self.is_playing:
            self.current_frame += 1
        
        if self.current_frame > (len(self.sequence_dict[self.current_sequence]) - 1):
            self.current_frame = 0
            
        self.image = self.sequence_dict[self.current_sequence][self.current_frame]

    def play(self, sequenceID, frameID = 0):
        self.is_playing = True
        if self.current_sequence != sequenceID:
            self.current_sequence = sequenceID
            self.current_frame = frameID

    def stop(self, sequenceID = None, frameID = 0):
        self.is_playing = False
        
        if sequenceID:
            self.current_sequence = sequenceID
           
        if frameID:
            self.current_frame = frameID

    def buildAnimation(self, sequenceID, frames):
        self.sequence_dict[sequenceID] = []
        if not self.current_sequence:
            self.current_sequence = sequenceID
        try:
            for frame in frames:
                try:
                    self.sequence_dict[sequenceID].append(self.frame_dict[frame])
                    
                except:
                    self.frame_dict[frame] = (utility.loadImage(frame))
                    self.sequence_dict[sequenceID].append(self.frame_dict[frame])
        except:
            try:
                self.sequence_dict[sequenceID].append(self.frame_dict[frames])
            except:
                self.frame_dict[frames] = (utility.loadImage(frames))
                self.sequence_dict[sequenceID].append(self.frame_dict[frames])
                
        self.image = self.sequence_dict[self.current_sequence][self.current_frame]
        