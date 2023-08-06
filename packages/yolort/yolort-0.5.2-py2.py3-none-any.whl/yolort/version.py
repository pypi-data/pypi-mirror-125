__version__ = '0.5.2'
git_version = '98869ed8a24c9481c2f61ddfce103bd6defbdf2e'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
