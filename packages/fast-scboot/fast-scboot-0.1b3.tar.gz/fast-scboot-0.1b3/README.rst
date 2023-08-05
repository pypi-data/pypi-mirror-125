

FastScboot
==========

FastScboot is a statistics tool to perform the stratified clustered bootstrap sampling on given data. The algorithm is fast in the sense that the remaining bottleneck to the speed of the algorithm is the speed of memory access during the inplace fancy indexing operation.

Install
-------

::

	pip install fast-scboot

Getting started
---------------

First import the package and initialize the ``Sampler`` object.

.. code:: python

	from fast_scboot import Sampler

	s = Sampler()

Let's create a sample data.

.. code:: python

	import numpy as np
	import pandas as pd

	clusts = np.asarray([0, 1, 1, 2, 0, 1, 1, 0, 2, 2])
	strats = np.asarray([0, 0, 0, 0, 1, 1, 1, 2, 2, 2])
	data = np.squeeze(np.dstack([strats, clusts])).astype(np.double)
	data = pd.DataFrame(data, columns=['strat', 'clust'])

Two preparatory steps are preparing the data, and creating some data cache:

.. code:: python

	s.prepare_data(data, 'strat', 'clust')
	s.setup_cache()

After that, you can start drawing samples:

.. code:: python

	for i in range(100):

	    sampled = s.sample_data(seed=i)

How does it work?
-----------------

.. image:: https://github.com/mozjay0619/fast-scboot/blob/master/media/image1.png
	:width: 600pt

When the ``prepare_data`` method is invoked, once the original data has been sorted by strata and cluster levels, the ``make_index_matrix`` creates three auxiliary arrays: ``idx_mtx``, ``strat_arr``, and ``clust_arr``. The ``idx_mtx`` array stores information on where each cluster begins and how many rows it occupies, as well as the actual cluster value. The ``strat_arr`` is an index array that indexes the strata levels at each of the cluster level. The ``clust_arr`` does the same but for the cluster levels. The reason the values of the ``clust_arr`` are not uniformly increasing like ``strat_arr`` in this example is because internally, the unique indices are created using the Cantor pairing function for speed (and then re-cast into integer using Pandas "cateory" type).

When the ``sample_data`` method is invoked, three additional auxiliary data are created. The ``clust_cnt_arr`` array stores the number of unique cluster values in each strata, in this case, [3, 2, 2]. The total number of unique strata values is stored in the ``num_strats`` variable (3 in this case), and the same for cluster is store in the ``num_clusts`` variable (7 in this case).

.. image:: https://github.com/mozjay0619/fast-scboot/blob/master/media/imageB.png
	:width: 270pt

We produce a random array from [0, 1] uniform distribution with size equal to ``num_clusts``. It's important that we invoke random sampling function once because usually it's very expensive to call them repeatedly. Then we use the ``clust_cnt_arr`` and loop through (vectorized using Cython) the uniform random numbers and multiply them by the values in ``clust_cnt_arr``, and then cast them to integer datatype. We are effectively mapping the uniform random values from [0, 1] to appropriate range of integer values, which can be used as randomly bootstrap sampled indices (stored in ``s`` variable) for the ``idx_mtx`` array.

.. image:: https://github.com/mozjay0619/fast-scboot/blob/master/media/image5.png
	:width: 365pt

The ``s`` array is used on the ``idx_mtx``, where we are effectively sampling with replacement clusters from each stratum (i.e. from each colored area). Once we have cluster bootstrap sampled ``idx_mtx``, we can use the information stored in that matrix to construct the ``sampled_idxs`` array, which records indices of the sampled data in terms of the indicies of the original data. The final return value is produced by fancy indexing the original data using the ``sampled_idxs``. The native numpy fancy indexing is somewhat costly due to data copy, so we provide our own inplace version of fancy indexing.