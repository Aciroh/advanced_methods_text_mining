class Evaluation:
    pos=None
    tp=0
    tn=0
    fp=0
    fn=0

    def checkEvaluation(self, predictedPOS, realPOS):
        if self.pos == predictedPOS:
            if self.pos == realPOS:
                self.tp+=1
            else:
                self.fp+=1
        else:
            if self.pos == realPOS:
                self.fn+=1
            else:
                self.tn+=1

    def getAccuracy(self):
        return (self.tp+self.tn)/(self.tp+self.fn+self.fp+self.tn)
    
    def getPrecision(self):
        try:
            return self.tp/(self.tp+self.fp)
        except ZeroDivisionError:
            return 0
    
    def getRecall(self):
        return self.tp/(self.tp+self.fn)
    
    def getSpecificity(self):
        return self.tn/(self.fp+self.tn)
    
    def reset(self):
        self.tp=0
        self.tn=0
        self.fp=0
        self.fn=0

    def __init__(self, pos) -> None:
        self.pos = pos