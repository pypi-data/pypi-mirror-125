import os
import time
import pkg_resources
from casaconfig import measures_update


########################################################################
## Setup the runtime operation data directories
########################################################################
datapath = [pkg_resources.resource_filename('casaconfig', '__data__/')]
rundata = os.path.expanduser("~/.casa/measures")

# execute only when casatools is initialized
if __name__ == 'casatoolrc':
    # make parent folder (ie .casa) if necessary
    if ('/' in rundata) and (rundata.rindex('/') > 0) and (not os.path.exists(rundata[:rundata.rindex('/')])):
        os.system('mkdir %s' % rundata[:rundata.rindex('/')])

    from casatools import casalog
    measures_update(rundata, logger=casalog)

########################################################################
## Default CASA configuration parameters
########################################################################
logfile='casalog-%s.log' % time.strftime("%Y%m%d-%H",time.localtime())
telemetry_enabled = True
crashreporter_enabled = True
nologfile = False
log2term = True
nologger = True
nogui = False
colors = "LightBG"
agg = False
pipeline = False
iplog = True
user_site = False
telemetry_log_directory = "~/tmp"
telemetry_log_limit = 1650
telemetry_log_size_interval = 30
telemetry_submit_interval = 20

