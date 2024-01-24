import string
from xmlrpc.client import Boolean


class Word:
    text=None
    pos=None
    count=0

    @staticmethod
    def strip_pos(pos) -> string:
        pos=''.join(e for e in pos if e.isalnum())
        print(pos)
        return pos
    
    @staticmethod
    def ignored_pos(pos) -> Boolean:
        ignore_list = ['tl', 'hl', 'nc', 'nil', 'fw', 'ql']
        if pos in ignore_list:
            return True
        else:
            return False
        
    @staticmethod
    def cast_pos(pos) -> string:
        noun_list=["NOUN","nn","nna","nnc","nn$","nns","nns$","np","np$","nps","nr","nrs","nnp","nnpc","nr$","nps$"]
        verb_list=["VERB","vb","vba","vbd","vbg","vbn","vbz","hv","hvd","hvg","hvn","hvz","be","bed","bedz","beg","bem","ben","ber","bez","do","dod","doz"]
        conjunction_list=["CONJUNCTION","cc","cd","cs","cd$"]
        determiner_list=["DETERMINER","dt" ,"dti" ,"dts","dtx","wdt" ,"ap" ,"ap$" ,"dt$"]
        adjective_list=["ADJECTIVE","jj" ,"jja" ,"jjc","jjcc" ,"jjr" ,"jjs","jjf" ,"jjt" ,"jjm" ,"jj$"]
        article_list=["article","at"]
        preposition_list=["PREPOSITION","in"]
        pronoun_list=["PRONOUN","wp$" ,"wpo" ,"wps","pn" ,"pn$" ,"pp$","pp$$" ,"ppl" ,"ppls","ppo" ,"pps" ,"ppss","prp" ,"prps" ,"prp$"]
        adverb_list=["ADVERBN","wrb" ,"rb" ,"rbr","rbs" ,"rbt" ,"rn","rp" ,"abl" ,"rb$"]
        number_list=["NUMBER","od"]
        modal_auxiliary_list=["MODAL_AUXILIARY","md" ,"md*"]
        symbol_list=["SYMBOL","\"" ,"." ,",","(" ,")" ,"*" "--",":" ,"PU","SY" ,"``" ,"'" ,"''"]
        other_list=["OTHER","to" ,"*" ,"ex" ,"wql","abn" ,"abx" ,"uh","qlp" ,"t" ,""]
        if pos in noun_list:
            return "NOUN"
        elif pos in verb_list:
            return "VERB"
        elif pos in conjunction_list:
            return "CONJUNCTION"
        elif pos in determiner_list:
            return "DETERMINER"
        elif pos in adjective_list:
            return "ADJECTIVE"
        elif pos in article_list:
            return "ARTICLE"
        elif pos in preposition_list:
            return "PREPOSITION"
        elif pos in pronoun_list:
            return "PRONOUN"
        elif pos in adverb_list:
            return "ADVERB"
        elif pos in number_list:
            return "NUMBER"
        elif pos in modal_auxiliary_list:
            return "MODAL_AUXILIARY"
        elif pos in symbol_list:
            return "SYMBOL"
        elif pos in other_list:
            return "OTHER"
        else:
            return None


    def __init__(self, text, pos, count=0) -> None:
        print("Checking {}".format(pos))
        pos = self.strip_pos(pos)
        pos = self.cast_pos(pos.strip())
        if self.ignored_pos(pos) or pos == 'None' or pos is None:
            print(pos)
            raise ValueError()
        else:
            self.text = text.strip().lower()
            self.pos = self.cast_pos(pos.strip())
            if count == 0:
                self.count = 1
            else:
                self.count+=1

    def inc(self) -> None:
        self.count+=1

    def __eq__(self, other): 
        if not isinstance(other, Word):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.text == other.text and self.pos == other.pos