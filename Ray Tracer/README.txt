This program is designed to model and trace the propagation of a bundle of rays through refractive media (e.g. through a lens).

List of files included:

'raytracer' -- contains classes and methods for handling the ray, lens and output plane objects used in this model
'genpolar' -- contains functions used for plotting spot diagrams
'planoconvex' -- uses the raytracer model to output graphs and perform some analysis of the optical setup


Using this model:

The 'raytracer' file shows how each optical object should be initialised, how they are defined and what methods can be used with them, but does not produce results on its own.

Running 'planoconvex' makes use of the model to propagate a ray through a planoconvex lens and outputs its focal length, RMS radius and diffraction limit. Two orientations of the lens have already been initialised, but these definitions can be altered to consider different setups.