import base64
import bz2
import numpy as np
from cPickle import loads



models = """
"""

model = loads(bz2.decompress(base64.b64decode(models)))
nb_ptc, nb_pc, nb_classes, tk_nextmove, tk_output = model
nb_numfeats = len(nb_ptc) / len(nb_pc)

# reconstruct pc and ptc
nb_pc = np.array(nb_pc)
nb_ptc = np.array(nb_ptc).reshape(len(nb_ptc)/len(nb_pc), len(nb_pc))

print cls(nb_ptc, nb_pc, nb_numfeats, nb_classes, tk_nextmove,
           tk_output, *args, **kwargs)