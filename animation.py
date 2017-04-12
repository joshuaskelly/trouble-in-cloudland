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
        return '<Animation({0} Sequences): {1}>'.format(self.length, self.keys)

    def __len__(self):
        return len(self.sequence_dict)

    @property
    def length(self):
        return len(self.sequence_dict)

    @property
    def keys(self):
        return self.sequence_dict.keys()

    def set_parent(self, parent):
        self.parent = parent
        self.parent.image = self.sequence_dict[self.current_sequence][self.current_frame]

    def update(self):
        if self.is_playing:
            self.current_frame += 1
        
        if self.current_frame > len(self.sequence_dict[self.current_sequence]) - 1:
            self.current_frame = 0
            
        self.image = self.sequence_dict[self.current_sequence][self.current_frame]

    def play(self, sequence_id, frame_id=0):
        self.is_playing = True

        if self.current_sequence != sequence_id:
            self.current_sequence = sequence_id
            self.current_frame = frame_id

    def stop(self, sequence_id=None, frame_id=0):
        self.is_playing = False
        
        if sequence_id:
            self.current_sequence = sequence_id
           
        if frame_id:
            self.current_frame = frame_id

    def build_animation(self, sequence_id, frames):
        self.sequence_dict[sequence_id] = []
        if not self.current_sequence:
            self.current_sequence = sequence_id

        try:
            for frame in frames:
                try:
                    self.sequence_dict[sequence_id].append(self.frame_dict[frame])
                    
                except:
                    self.frame_dict[frame] = (utility.load_image(frame))
                    self.sequence_dict[sequence_id].append(self.frame_dict[frame])

        except:
            try:
                self.sequence_dict[sequence_id].append(self.frame_dict[frames])

            except:
                self.frame_dict[frames] = (utility.load_image(frames))
                self.sequence_dict[sequence_id].append(self.frame_dict[frames])
                
        self.image = self.sequence_dict[self.current_sequence][self.current_frame]
