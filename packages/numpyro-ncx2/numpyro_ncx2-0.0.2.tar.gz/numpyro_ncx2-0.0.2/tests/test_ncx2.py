import jax
import numpy as np
import pytest
import scipy.stats
from jax.test_util import _dtype, tolerance

from numpyro_ncx2 import NoncentralChi2


def assert_allclose(x, y, *, atol=None, rtol=None):
    assert x.shape == y.shape
    atol = 100 * max(tolerance(_dtype(x), atol), tolerance(_dtype(y), atol))
    rtol = 100 * max(tolerance(_dtype(x), rtol), tolerance(_dtype(y), rtol))
    np.testing.assert_allclose(x, y, atol=atol, rtol=rtol)


@pytest.mark.parametrize("args", [(5, 12.0), (50, 1.1), (1, 80.0)])
def test_sample(args):
    ref = scipy.stats.ncx2(*args)
    samples = NoncentralChi2(*args).sample(jax.random.PRNGKey(4), (10_000,))
    assert scipy.stats.kstest(samples, ref.cdf).statistic < 0.01


@pytest.mark.parametrize("args", [(5, 12.0), (50, 5.1), (1, 80.0)])
def test_logp(args):
    ref = scipy.stats.ncx2(*args)
    dist = NoncentralChi2(*args)
    samples = dist.sample(jax.random.PRNGKey(4), (5000,))
    assert_allclose(ref.logpdf(samples), dist.log_prob(samples))
