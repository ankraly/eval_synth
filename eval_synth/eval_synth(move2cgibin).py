#!/usr/bin/env python
# -*- coding: utf-8 -*-

import experiment_runner
experiment_runner.runExperiment("eval_synth",
                                "sequence_pilot.txt",
                                "french.txt",
                                disableRefresh=False,
                                audioExtList=[".wav"],
                                allowUtilityScripts=True,
                                allowUsersToRelogin=True,
                                individualSequences=True)
