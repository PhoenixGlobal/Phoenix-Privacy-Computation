#!/usr/bin/env python3

from chainV3Api import *
import _thread


pContract=PrivacyContract()
# _thread.start_new_thread(pContract.runJobsLoop, (2,))
# pContract.eventMonitor()
pContract.startJobId("39259062678004918608881834022944323887093501873279290277513468832177685435234")
