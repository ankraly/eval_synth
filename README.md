# eval_synth
post-pilot version of speech synthesis evaluation task

**audio_prep.py** -------------------------------------------
* start:
    - "audio" folder with list of individual system & human stimuli (.wav)
* end: 
    - "stim" folder with wav, mp3, ogg versions of concatenated pairs (target+(other speaker))  
* will probably be split into "combine" and "convert" separately as the sentences need to be converted to mp3+ogg too

**write_exp.py** --------------------------------------------
* start:
    - "stim" folder as output by audio_prep.py
    - "sent" folder with individual sentences (not affected by audio_prep.py)
    - "systems.txt" with list of systems (except defaults: 2nd human, monolingual TTS, dumb multilingual baseline)
    - "split.txt" indicating which stimuli to take from 2nd human and which from monolingual TTS in the event that a "split_gold" condition is chosen
* end:
    - "seq" folder where resulting sequences land
    - **! "seq" contents should then be copied to LMEDS-master > tests > eval_synth (wherever that may end up being)**
      
*running write_exp.py:*

  **write_exp.py(ID="time",split_gold=1,**kwargs{ls,num})**
 
* ID determines sequence name, will default to "YYYYMMDD_HHMMSS.txt"
* split_gold determines whether the "gold" condition is 50/50 human/monoTTS or 2 entire separate assortiments of human and monoTTS
    - (default is 50/50 as that is smaller)
* ls & num specify the array/number of experimental systems to be used, both optional
    - ls should contain experimental systems' IDs as present in filenames
        - gold and baseline will be added to system list internally later on
    - num must >= 3 (or >= 2 if split_gold==1)
        - minimal condition = gold_human, gold_monoTTS, baseline OR gold_50/50, baseline
        - system shuffles list of all experimental systems and chooses [num] of them
    - if neither num nor ls are specified, will create experiment with 50/50 gold and baseline
