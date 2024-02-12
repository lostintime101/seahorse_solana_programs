
from seahorse.prelude import *

declare_id('')


@instruction
def hello(signer: Signer):
    print('Hello, World!')

