# LMEDS audio prep
#
# requires:
# - "audio" folder: individual sound files, all systems & all phoneme combinations
# - systems.txt: list of all systems used (excl. golds, baseline, and target)
# - stimlist.txt: list of all stimuli produced by systems
# > combining chunk uses stimlist to produce new filenames in orderly fashion
# - "stim" folder: output for combined pairs of stimuli (target + learner)
# > converting chunk adds .mp3 and .ogg copies of pairs to stim folder
#

import os, sys
from pydub import AudioSegment

slash = "/"
if sys.platform[:3] == "win":
    slash = "\\"
    
homedir = os.getcwd()
audio = homedir+slash+"audio"+slash
stim = homedir+slash+"stim"+slash

# list of system names
## STATIC: always included, change name as needed
TGT = "speaker"     # speaker ID of target human speaker
GOLDH = "human"     # name of human comparison speaker, "gold-human"
GOLDS = "mono_tts"  # name of monolingual TTS system, "gold-system"
BASE = "baseline"   # name of dumb baseline system
## malleable: edit newline-separated text file to add/remove new
systems_list = open("systems.txt",'r') # for example
sys_ls = systems_list.readlines()
for sy in sys_ls:
    sy = sy.strip()
sy.extend([GOLDH,GOLDS,BASE]) # adding the default systems back in
systems_list.close()

# combining pairs:

silence = AudioSegment.silent(duration=500)

stims = (open("stimlist.txt")).readlines() 

for line in stims:
    l = (line.strip()).split("\t")
    one = AudioSegment.from_wav(audio+l[0]+"_"+TGT+".wav")
    for sy in sys_ls:
        two = AudioSegment.from_wav(audio+l[0]+"_"+sy+".wav")
        new = one + silence + two
        new.export(stim+l[0]+TGT+"_and_"+l[0]+"_"+sy+".wav", format="wav")
    
# converting wav to mp3 + ogg:
## not very clean as takes end_dir of previous operation, assuming there's nothing
## except wavs in that directory; would need manual cleaning between runs

src = os.listdir(stim)

for f in src:
    new_mp3 = f[:-3]+"mp3"
    new_ogg = f[:-3]+"ogg"
    sound = AudioSegment.from_wav(stim+f)
    sound.export(stim+"{}".format(new_mp3), format="mp3")
    sound.export(stim+"{}".format(new_ogg), format="ogg")
