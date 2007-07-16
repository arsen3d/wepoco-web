#include <Python.h>
#include <structmember.h>
#include "proj_api.h"

/*
 * Author: mike@saunby.net  
 * URL: http://mike.saunby.net
 * $Date$
 * $Id$
 */

/*
 * Prototypes for the methods.
 * These are accessed from Python scripts as, e.g. "proj4.init(...)"
 */
typedef struct {
  PyObject_HEAD
  projPJ pj;
} Projection;

static int
Projection_init(Projection *self, PyObject *args, PyObject *keywds);

static PyObject *
Projection_fwd(Projection *self, PyObject *args);

static PyObject *
Projection_inv(Projection *self, PyObject *args);


static PyMemberDef Projection_members[] = {
  {"pj", T_OBJECT_EX, offsetof(Projection, pj), 0,
   "pj ptr"},
  {NULL} /* Sentinel */
};


const double NO_VALUE = 0.0;

static void
Projection_dealloc(Projection* self)
{
  self->ob_type->tp_free((PyObject*)self);
}


static PyObject *
Projection_new(PyTypeObject *type, PyObject *args, PyObject kwds)
{
  Projection *self;
  self = (Projection *)type->tp_alloc(type, 0);
  if (self != NULL) {
    self->pj  = NULL;
  }
  return (PyObject *)self;
}


static int
Projection_init(Projection *self, PyObject *args, PyObject *keywds)
{
  /* 
   * The following variables are equivalent to the +{something} args for the proj
   * command, e.g. +proj=nsper is given as proj="nsper"
   */
  char *proj = NULL, *ellps = NULL, *datum = NULL;
  double lat_0 = NO_VALUE, lon_0 = NO_VALUE, lat_ts = NO_VALUE, a = NO_VALUE, h = NO_VALUE;
  double b =  NO_VALUE, f =  NO_VALUE, rf =  NO_VALUE, e =  NO_VALUE, es =  NO_VALUE;
  double x_0 = NO_VALUE, y_0 = NO_VALUE, to_meter = NO_VALUE, azi = NO_VALUE, tilt = NO_VALUE;
  double  lat_1 = NO_VALUE, lat_2 = NO_VALUE, lat_3 = NO_VALUE, lat_b = NO_VALUE;
  double lsat = NO_VALUE, path = NO_VALUE, theta = NO_VALUE, alpha = NO_VALUE, lonc = NO_VALUE; 
  double lon_1 = NO_VALUE, lon_2 = NO_VALUE, lon_3 = NO_VALUE, zone = NO_VALUE;
  double m = NO_VALUE, n = NO_VALUE, q = NO_VALUE, alphi = NO_VALUE, W = NO_VALUE, M = NO_VALUE;

  static char *kwlist[] = {"proj", "ellps", "datum",
			   "lat_0", "lon_0", "lat_ts", "a", "h",
			   "b", "f", "rf", "e", "es",
			   "x_0", "y_0", "to_meter", "azi", "tilt",
			   "lat_1", "lat_2", "lat_3", "lat_b",
			   "lsat", "path", "theta", "alpha", "lonc", 
			   "lon_1", "lon_2", "lon_3", "zone",
			   "m", "n", "q", "alphi", "W", "M",
			   NULL};

  char *pargs[50];
  int pargnum;

  /* Even if this call fails part way through it is important to
   * ensure that calls to fwd() only succeed if everything went well.
   * So clear any earlier pj.
   */

  if(self->pj){
    free(self->pj);
    self->pj = NULL;
  }
  /*
   * Get args from Python in the form that gives most functionality and best
   * error checking.  i.e. although we need to pass strings to the Proj4 code
   * it is best to ensure that e.g. lat_0, is a floating point value.
   */
  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|ssdddddddddddddddddddddddddddddddddd", kwlist, 
				   &proj, &ellps, &datum, 
				   &lat_0, &lon_0, &lat_ts, /* 3 */
				   &a, &h, &b, &f, &rf, &e, &es, /* 7 */
				   &x_0, &y_0, &to_meter, &azi, &tilt, /* 5 */
				   &lat_1, &lat_2, &lat_3, &lat_b, /* 4 */
				   &lsat, &path, &theta, &alpha, &lonc, /* 5 */
				   &lon_1, &lon_2, &lon_3, &zone, /* 4 */
				   &m, &n, &q, &alphi, &W, &M /* 6 */  
				   /* total 'd's = 34 */
				   ))
    return -1;

  /*
   * Now convert to strings.
   */

  pargnum = 0;
  pargs[pargnum] = calloc(20, 1);
  sprintf(pargs[pargnum], "proj=%s", proj);
  pargnum++;
  if(ellps){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "ellps=%s", ellps);
    pargnum++;
  }
  if(datum){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "datum=%s", datum);
    pargnum++;
  }
  if(lat_0 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_0=%g", lat_0);
    pargnum++;
  }
  if(lon_0 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lon_0=%g", lon_0);
    pargnum++;
  }
  if(lat_ts != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_ts=%g", lat_ts);
    pargnum++;
  }
  if(a != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "a=%g", a);
    pargnum++;
  }
  if(h != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "h=%g", h);
    pargnum++;
  }
  if(b != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "b=%g", b);
    pargnum++;
  }
  if(f != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "f=%g", f);
    pargnum++;
  }
  if(rf != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "rf=%g", rf);
    pargnum++;
  }
  if(e != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "e=%g", e);
    pargnum++;
  }
  if(es != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "es=%g", es);
    pargnum++;
  }
  if(x_0 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "x_0=%g", x_0);
    pargnum++;
  }
 if(y_0 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "y_0=%g", y_0);
    pargnum++;
  }
 if(to_meter != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "to_meter=%g", to_meter);
    pargnum++;
  }
 if(azi != NO_VALUE){
   pargs[pargnum] = calloc(20, 1);
   sprintf(pargs[pargnum], "azi=%g", azi);
   pargnum++;
 }
 if(tilt != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "tilt=%g", tilt);
    pargnum++;
  }
 if(lat_1 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_1=%g", lat_1);
    pargnum++;
  }
 if(lat_2 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_2=%g", lat_2);
    pargnum++;
  }
 if(lat_3 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_3=%g", lat_3);
    pargnum++;
  }
 if(lat_b != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lat_b=%g", lat_b);
    pargnum++;
  }
 if(lsat != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lsat=%g", lsat);
    pargnum++;
  }
 if(path != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "path=%g", path);
    pargnum++;
  }
 if(theta != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "theta=%g", theta);
    pargnum++;
  }
 if(alpha != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "alpha=%g", alpha);
    pargnum++;
  }
 if(lonc != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lonc=%g", lonc);
    pargnum++;
  }
 if(lon_1 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lon_1=%g", lon_1);
    pargnum++;
  }
 if(lon_2 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lon_2=%g", lon_2);
    pargnum++;
  }
 if(lon_3 != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "lon_3=%g", lon_3);
    pargnum++;
  }
 if(zone != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "zone=%g", zone);
    pargnum++;
  }
 if(m != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "m=%g", m);
    pargnum++;
  }
 if(n != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "n=%g", n);
    pargnum++;
  }
 if(q != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "q=%g", q);
    pargnum++;
  }
 if(alphi != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "alphi=%g", alphi);
    pargnum++;
  }
 if(W != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "W=%g", W);
    pargnum++;
  }
 if(M != NO_VALUE){
    pargs[pargnum] = calloc(20, 1);
    sprintf(pargs[pargnum], "M=%g", M);
    pargnum++;
  }
 if (!(self->pj = pj_init(pargnum, pargs))){
   PyErr_SetString(PyExc_RuntimeError, "Proj4: init failed");
   return -1;
 }
 return 0;
}

static PyObject *
Projection_fwd(Projection *self, PyObject *args)
{
  projUV p;
  double u = NO_VALUE, v = NO_VALUE;

  /* Check that a valid proj_init() has been performed. */ 
  if(!self->pj){
    PyErr_SetString(PyExc_RuntimeError, "Proj4: a valid init() must preceed a call to fwd()");
    return NULL;
  }

  /* No need to give error value as PyArg_ParseTuple handles that. */
  if (!PyArg_ParseTuple(args, "(dd)", &u, &v)){
    return NULL;
  }

  p.u = u;
  p.v = v;
  p = pj_fwd(p, self->pj);

  if ((p.u == HUGE_VAL)||(p.v == HUGE_VAL)){
    Py_INCREF(Py_None);
    return Py_None;
  }
  return Py_BuildValue("(dd)", p.u, p.v);
}

static PyObject *
Projection_inv(Projection *self, PyObject *args)
{
  projUV p;
  double u = NO_VALUE, v = NO_VALUE;

  /* Check that a valid proj_init() has been performed. */ 
  if(!self->pj){
    PyErr_SetString(PyExc_RuntimeError, "Proj4: a valid init() must preceed a call to inv()");
    return NULL;
  }

  /* No need to give error value as PyArg_ParseTuple handles that. */
  if (!PyArg_ParseTuple(args, "(dd)", &u, &v)){
    return NULL;
  }

  p.u = u;
  p.v = v;
  p = pj_inv(p, self->pj);
  p.u = p.u;
  p.v = p.v;

  return Py_BuildValue("(dd)", p.u, p.v);
}

static PyMethodDef
Projection_methods[] = {
  {"init", (PyCFunction)Projection_init, METH_VARARGS|METH_KEYWORDS,
   "See manpage py_init"
  },
  {"fwd", (PyCFunction)Projection_fwd, METH_VARARGS,
  "See manpage py_init"
  },
  {"inv", (PyCFunction)Projection_inv, METH_VARARGS,
  "See manpage py_init"
  },
  {NULL}
};



static PyTypeObject ProjectionType = {
  PyObject_HEAD_INIT(NULL)
  0, /*ob_size*/
  "proj4.Projection", /*tp_name*/
  sizeof(Projection), /*tp_basicsize*/
  0, /*tp_itemsize*/
  (destructor)Projection_dealloc, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  0, /*tp_as_number*/
  0, /*tp_as_sequence*/
  0, /*tp_as_mapping*/
  0, /*tp_hash */
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  0, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "Projection objects", /* tp_doc */
  0, /* tp_traverse */
  0, /* tp_clear */
  0, /* tp_richcompare */
  0, /* tp_weaklistoffset */
  0, /* tp_iter */
  0, /* tp_iternext */
  Projection_methods, /* tp_methods */
  Projection_members, /* tp_members */
  0, /* tp_getset */
  0, /* tp_base */
  0, /* tp_dict */
  0, /* tp_descr_get */  
  0, /* tp_descr_set */
  0, /* tp_dictoffset */
  (initproc)Projection_init, /* tp_init */
  0, /* tp_alloc */
  Projection_new, /* tp_new */
};

static PyMethodDef module_methods[] = {
  {NULL} /* Sentinel */
};


/*
 * This func called to load the mappings when this module is imported.
 * The Python distutils package expects a package called proj4 to have a
 * initproj4() func.
 */

PyMODINIT_FUNC
initproj4(void)
{
  PyObject* m;

  if (PyType_Ready(&ProjectionType) <0)
    return;

  m = Py_InitModule3("proj4", module_methods, "Proj4");
  if (m == NULL)
    return;

  Py_INCREF(&ProjectionType);
  PyModule_AddObject(m, "Projection", (PyObject *)&ProjectionType);
}
