# LMEDS experiment writer 
#
# assumes:
# (A) "stim" folder with concatenated pairs of sounds
# - each stim is composed of "target speaker"+500ms+"system learner"; wav+mp3+ogg
# - each stim title is [phonemes]_[targetspeaker]_and_[phonemes]_[systemname]
# (B) "sent" folder with entire sentences to rate
# - each sentence ends with [systemname] as above
# (C) "seq" folder where the resulting sequences go to live
# - resulting sequence filename is the least pleasing thing here, can/should be
# changed to something more sensible
# - at the end, move contents of (C) to LMEDS-master > tests > [EXP_NAME]
#
# (D) MOST IMPORTANT but least immediate: LMEDS-internal dictionary with names
# matching the text bits that are written to the LMEDS sequence files ! ! !

# note to self: single out "training" trials by appending "train" at end

from datetime import datetime
from itertools import product
import os,sys,random

slash = "/"
if sys.platform[:3] == "win":
    slash = "\\"
    
homedir = os.getcwd()
stim = homedir+slash+"stim"+slash
sent = homedir+slash+"sent"+slash
seq = homedir+slash+"sequences"+slash

# STATIC VARIABLES:
## experiment name (needs to be consistent w/ LMEDS folder
EXP_NAME = "eval_synth"
## default always-included system names, change as needed
GOLDH = "human"      # name of human comparison speaker, "gold-human"
GOLDS = "mono_tts"    # name of monolingual TTS system, "gold-system"
SPLIT = "split_gold" # not a system name but used as one
BASE = "baseline"    # name of dumb baseline system

# EXPERIMENTAL SYSTEM NAMES: please provide nice text file with each system
# name on a new line, not including baseline & golds
systems_list = open("systems.txt",'r') # for example
sys_ls = systems_list.readlines()
for sy in sys_ls:
    sy = sy.strip()
systems_list.close()

# THE THING ITSELF
       
def write_pairs_ls(systems=[SPLIT,BASE]):
    """
    writes up randomized media_choice section of LMEDS experiment for rating
    pairs of syllables, for a given list of systems
    
    always needs included: gold ([human,monoTTS] OR [split_gold,]) and baseline
    special case: split_gold (50/50 human/monolingual TTS stim split)
    => str output
    """ 
    t = "<randomize>\n"
    stims = os.listdir(stim)
    # just in case, clean out non-wav files to make things faster, since this
    # may be run on triple directories (wav,mp3,ogg copies of all files)
    st = []
    for s in stims:
        if s.endswith(".wav"):
            st.append(s)
    
    if SPLIT in systems:
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # remove "split_gold" from systems list as that does not exist !
        systems.remove(SPLIT)
    
    for tup in product(st,systems):
        # tup[0] = filename (incl. ".wav")
        # tup[1] = system name
        if tup[0][:-4].endswith(tup[1]):
            t += "media_choice rating_instr audio 1.5 1 1 [["+tup[0][:-4]+"]] [0 1 2 3 4 5]\n"
            # ^ the above assumes "rating_instr" as entry in LMEDS french.txt dictionary
    t += "</randomize>\n"
    return t

def write_pairs_num(num=3, split_gold=1):
    """
    writes up randomized media_choice section of LMEDS experiment for rating
    pairs of syllables, for a given number of systems
    
    split_gold: 0 = 2 entire gold systems (1 human, 1 monolingual TTS)
                1 = 1 gold system (50/50 human/monolingual TTS)
    num: number of systems to include
        >minimum with split_gold = 2 (gold and garbage)
        >minimum without split_gold = 3 (human, monoTTS, garbage)
        >systems 
    => str output
    """
    if split_gold==1:
        num -= 2 # as 1 slot taken up by 50/50 gold, 1 slot by baseline
    else:
        num -= 3 # as 2 slots taken up by gold, 1 slot by baseline
    
    # trusting the shuffle function to get a random num-long subset of systems 
    sh = random.shuffle(sys_ls)
    ls = sh[:num]
    
    # putting our default systems in and passing the list back to write_pairs_ls:
    if split_gold==1:
        ls.append([SPLIT,BASE])
    else:
        ls.extend([GOLDH,GOLDS,BASE])
    t = write_pairs_ls(ls)
    return t

def write_sent():
    """
    writes up randomized media_choice section of LMEDS experiment for rating
    entire sentences, for a given number of systems
    => str output
    """
    t = "<randomize>\n"
    sents = os.listdir(sent)
    for s in sents:
        t += "media_choice rating_sent audio 1.5 1 1 [["+s[:-4]+"]] [0 1 2 3 4 5]\n"
        # ^ the above assumes "rating_sent" as entry in LMEDS french.txt dictionary
    t += "</randomize>\n"
    return t

def write_exp(ID="time",split_gold=1,**kwargs):
    """
    writes LMEDS experiment provided user-specified parameters
    
    ID: unique user ID; if not provided, swapped for datetime string
    split_gold: 0 = 2 entire gold systems (1 human, 1 monolingual TTS)
                1 = 1 gold system (50/50 human/monolingual TTS)
    within kwargs:
        num = number of systems, OR
        systems = list of systems
    """
    num=kwargs.get('num',None)
    ls=kwargs.get('systems',None)
    # rewrite this to not be time but instead list of systems + time? or like
    # something more descriptive than just a timestamp
    if ID=="time":
        x = datetime.now()
        ID = x.strftime("%Y%m%d%_H%M%S")
    
    exp = open(seq+ID+".txt","w")
    # experiment name header: matches name of LMEDS output folder
    exp.write("*"+EXP_NAME+"\n") 
    
    # everything below this assumes a specific LMEDS dictionary, french.txt;
    # if dictionary is altered, this will need to be altered
    ## alternatively could add a couple dozen static variables to this script instead...    
    exp.write("""
    login\n\n
    consent consent\n\n
    text_page first_page bindSubmitKeyIDList=space\n
    media_test audio testing\n\n
    """)
    exp.write("""
    text_page presurvey_instructions\n
    survey presurvey\n\n
    """) # optional survey
    exp.write(""" 
    text_page remote_experiment_notice\n\n
    text_page rating_task_instructions1\n
    text_page rating_task_instructions2\n\n
    """)
    
    # training sequence: needs figured out what sound files will be used, for now
    # sound files & training from pilot
    exp.write("""
    text_page training_instructions\n\n
    text_page training_1\n
    media_choice rating_instr audio 1.5 1 1 [[sh_u_ak_and_sh_u_anon]] [0 1 2 3 4 5]\n
    text_page feedback_5\n
    media_choice rating_instr audio 1.5 1 1 [[f_ah_EN_ak_and_f_i_anon]] [0 1 2 3 4 5]\n
    text_page feedback_1_fafi\n
    media_choice rating_instr audio 1.5 1 1 [[sh_u_ak_and_sh_u_EN_ewan]] [0 1 2 3 4 5]\n
    text_page feedback_3-4\n
    media_choice rating_instr audio 1.5 1 1 [[paix_r_ak_and_paix_r_ak_bad]] [0 1 2 3 4 5]\n
    text_page feedback_quality\n
    media_choice rating_instr audio 1.5 1 1 [[sh_u_ak_and_non2_ewan]] [0 1 2 3 4 5]\n
    text_page feedback_garbled\n
    media_choice rating_instr audio 1.5 1 1 [[v_a_ak_and_m_a_anon]] [0 1 2 3 4 5]\n
    text_page feedback_1_vama\n
    text_page go_forth\n\n
    """)
    
    # adding pairs randomised block:
    if ls != None:
        pairs = write_pairs_ls(ls)
    elif num != None:
        pairs = write_pairs_num(num, split_gold)
    else:
        # write a case that handles user input if neither num or pairs is provided
        # "please input a number of systems (mind that base & gold will take up slots)
        # or a list of systems separated by commas (no spaces)"
        #
        # for now use default case of 0 experimental systems, 50/50 gold, & baseline
        pairs = write_pairs_ls()
    exp.write(pairs+"\n")
    
    # adding sentences randomised block:
    exp.write("text_page sentence_instructions\n")
    sents = write_sent()
    exp.write(sents+"\n")
    
    # conclusion, survey, etc:
    exp.write("text_page congrats\n")
    ## optional: postsurvey 
    ## (need to write a postsurvey & instructions first though; current
    ## postsurvey.txt is default LMEDS english postsurvey)
    # exp.write("survey postsurvey\n")
    exp.write("text_page debrief\n\n")
    exp.write("end\n")
    
    exp.close()