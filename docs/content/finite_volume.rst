.. _finite_volume_index:

Intoduction to Finite Volume
****************************

What is the Finite Volume Method?
---------------------------------

The finite volume method is a method for numerically solving partial differential
equations. Implementation of the finite volume method requires the discretization
of continuous functions, resulting in discrete approximations. The discrete
approximations are typically organized on a numerical grid (or mesh),
which defines the domain, its boundaries, and the locations of discrete quantities.
The final product of the approach is a linear system of equations :math:`\boldsymbol{A \phi=q}`
that can be solved to compute the discrete approximation of a desired quantity.

.. image:: ../images/finitevolumeschematic.png
   :width: 700
   :align: center

In SimPEG, we have implemented a staggered mimetic finite volume approach (`Hyman and
Shashkov, 1999 <https://cnls.lanl.gov/~shashkov/papers/maxjcp.pdf>`_). This
approach requires the definitions of variables at either cell-centers, nodes,
faces, or edges. This method is different from finite difference methods,
as the final linear system is constructed by approximating the inner products between
test functions and partial differential equations.


Examples
--------

Below are several examples of the final linear system obtained using the finite volume approach.
A comprehensive derivation of the final result is not provided here. It in instead parsed into
a set of theory sections which include:

	- :ref:`discrete differential operators <differential_operators>`
	- :ref:`inner products <inner_products>`

Direct Current Resistivity
^^^^^^^^^^^^^^^^^^^^^^^^^^

The governing equation for the direct current resistivity problem is given by:

.. math::
	\nabla \cdot \sigma \nabla \phi = -q_s

where

	- :math:`\phi` is the electric potential
	- :math:`\sigma` is the electrical conductivity within the domain
	- :math:`q_s` is a general representation of the source term
	- :math:`\nabla` is the gradient operator
	- :math:`\nabla \cdot` is the divergence operator

If we choose to define the discrete representation of the electric potential on the nodes,
the solution for the electric potentials after applying the finite volume approach is given by:

.. math::
	\boldsymbol{[G^T M_{\sigma e} G ]} \boldsymbol{\phi} = \mathbf{q_s}

where :math:`\boldsymbol{G^T M_{\sigma e} G }` is a sparse matrix and

	- :math:`\boldsymbol{\phi}` is the discrete approximation to the electric potentials on the nodes
	- :math:`\boldsymbol{G}` is a discrete gradient operator
	- :math:`\boldsymbol{G^T}` is the transpose of :math:`\boldsymbol{G}` but acts as a divergence operator
	- :math:`\boldsymbol{M_{\sigma e}}` is the mass matrix
	- :math:`\boldsymbol{q_s}` is the discrete representation of the source term on the nodes


Frequency Domain Electromagnetics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The governing equations for the frequency domain electromagnetic problems,
for a source current, can be expressed using Maxwell's equations:

.. math::
	\begin{align}
	&\nabla \times \mu^{-1} \vec{B} - \sigma \vec{E} = \vec{J}_s \\
	&\nabla \times \vec{E} = - i\omega \vec{B}
	\end{align}

where

	- :math:`\vec{E}` is the electric field
	- :math:`\vec{B}` is the magnetic flux density
	- :math:`\vec{J}_s` is a general representation of the source term
	- :math:`\sigma` is the electrical conductivity within the domain
	- :math:`\mu` is the magnetic permeability within the domain
	- :math:`\omega` is the angular frequency
	- :math:`\nabla \times` is the curl operator

Here we choose to define the discrete representation of the electric field on edges
and the discrete representation of the magnetic flux density on faces.
The solution for the electric potentials after applying the finite volume approach is given by:

.. math::
	\begin{align}
	\boldsymbol{C^T M_{\mu f} \, b } - \boldsymbol{M_{\sigma e} \, e} = \mathbf{j_s} \\
	\mathbf{C \, e} = -i \omega \mathbf{b}
	\end{align}

which can be combined to form a single linear system:

.. math::
	\boldsymbol{[C^T M_{\mu f} C } + i\omega \boldsymbol{M_{\sigma e}]} \mathbf{e} = -i \omega \mathbf{j_s}

where :math:`\boldsymbol{C^T M_{\mu f} C } + i\omega \boldsymbol{M_{\sigma e}}` is a sparse matrix and

	- :math:`\boldsymbol{e}` is the discrete approximation to the electric field on edges
	- :math:`\boldsymbol{b}` is the discrete approximation to the magnetic flux density on faces
	- :math:`\boldsymbol{C}` is a discrete curl operator from edges to faces
	- :math:`\boldsymbol{M_{\sigma e}}` is the mass matrix for electrical conductivity
	- :math:`\boldsymbol{M_{\mu f}}` is the mass matrix for inverse of the magnetic permeability
	- :math:`\boldsymbol{j_s}` is the discrete representation of the source term on the edges

