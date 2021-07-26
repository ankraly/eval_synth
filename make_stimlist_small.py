
# CONSONANTS #######

# context consonants
c_easy = ["f","s","j"]
c_nasal = ["m",]
c_list = c_easy+c_nasal

#target consonants split by context
c_cvc = ["p","t","k","b","d","g","l","ʁ"]
c_cv = ["ɥ"]
c_vc = ["ɲ"]


# VOWELS ###########

#context vowels
v_easy = ["i","ɛ","u","ɔ"]

#target vowels split by context
v_cvc = ["a","o","ə","y","ø",]
v_vc = ["œ"]
v_cv = ["e"]
v_nasal = ["ɔ̃","ɛ̃","ɑ̃","œ̃"]
v_lax = ["œ","ɔ"]


# PLAINTEXT ########
# choosing to represent complicated IPA (mostly vowels) by representative FR words
plaintext = {"m":"m","n":"n","f":"f","v":"v","s":"s","z":"z","ʃ":"sh","ʒ":"zh","l":"l","w":"w","j":"j",
             "p":"p","t":"t","k":"k","b":"b","d":"d","g":"g",
             "ʁ":"r","ɲ":"agneau","ɥ":"huit",
             "i":"i","ɛ":"paix","u":"u","ɔ":"or",
             "e":"e","a":"a","o":"o","ə":"schwa",
             "y":"y","ø":"eux","œ":"oeuf","ɔ̃":"on","ɛ̃":"hein","ɑ̃":"gant","œ̃":"un"}



def make_stimlist(filename):
    file = open(filename, "w", encoding="utf-8")
    file.write("filename_stem\ttarget\tcontext\tIPA\n")
    
    # C targets ###############
    # CV & VC
    for c in c_cvc:
        c_plain = plaintext[c]
        for v in v_easy:
            v_plain = plaintext[v]
            # CV
            if v not in v_lax:
                file.write(c_plain+"_"+v_plain+"\t"+c+"\t"+v+"\t"+c+v+"\n")
            # VC
            ## > "if v not in v_cv" but v_cv and v_easy don't overlap 
            file.write(v_plain+"_"+c_plain+"\t"+c+"\t"+v+"\t"+v+c+"\n")
    # CV only
    ## > this overgenerates [ɥu] but these "if" and "for" lists are long enough as is
    for c in c_cv:
        c_plain = plaintext[c]
        for v in v_easy:
            v_plain = plaintext[v]
            if v not in v_lax:
                file.write(c_plain+"_"+v_plain+"\t"+c+"\t"+v+"\t"+c+v+"\n")
    # VC only
    for c in c_vc:
        c_plain = plaintext[c]
        for v in v_easy:
            v_plain = plaintext[v]
            ## (if v not in v_cv): 
            file.write(v_plain+"_"+c_plain+"\t"+c+"\t"+v+"\t"+v+c+"\n") 
                
    # V targets ###############
    # CV & VC, non-nasal vowels
    for c in c_list:
        c_plain = plaintext[c]
        # CV & VC
        for v in v_cvc:
            v_plain = plaintext[v]
            # CV
            file.write(c_plain+"_"+v_plain+"\t"+v+"\t"+c+"\t"+c+v+"\n")
            # VC
            file.write(v_plain+"_"+c_plain+"\t"+v+"\t"+c+"\t"+v+c+"\n")
        # CV only
        for v in v_cv:
            v_plain = plaintext[v]
            file.write(c_plain+v_plain+"\t"+v+"\t"+c+"\t"+c+v+"\n")
        # VC only
        for v in v_vc:
            v_plain = plaintext[v]
            file.write(v_plain+"_"+c_plain+"\t"+v+"\t"+c+"\t"+v+c+"\n")
    # nasal vowels:
    for v in v_nasal:
        v_plain = plaintext[v]
        # CV: any consonant goes
        for c in c_list:
            c_plain = plaintext[c]
            file.write(c_plain+"_"+v_plain+"\t"+v+"\t"+c+"\t"+c+v+"\n")
        # VC: exclude nasal consonants, take c_easy only
        for c in c_easy:
            c_plain = plaintext[c]
            file.write(c_plain+"_"+v_plain+"\t"+v+"\t"+c+"\t"+c+v+"\n")            

make_stimlist("stimlist_small.txt")