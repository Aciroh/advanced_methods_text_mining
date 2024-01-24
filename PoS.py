class PoS:
    pos=None
    count=0

    def __init__(self, pos, count=0) -> None:
        self.pos = pos
        if count==0:
            self.count+=1
        else:
            self.count=count
    
    def inc(self) -> None:
        self.count+=1

    def __eq__(self, other): 
        if not isinstance(other, PoS):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.pos == other.pos
    
    def __lt__(self, other): 
        return ((self.count) < (other.count)) 
  
    def __gt__(self, other): 
        return ((self.count) > (other.count)) 
  
    def __le__(self, other): 
        return ((self.count) <= (other.count)) 
  
    def __ge__(self, other): 
        return ((self.count) >= (other.count)) 
  