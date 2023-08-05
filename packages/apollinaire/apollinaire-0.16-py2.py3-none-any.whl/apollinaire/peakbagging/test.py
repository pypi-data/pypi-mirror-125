from apollinaire.peakbagging import *
import apollinaire.peakbagging.templates as templates
import importlib.resources
import pandas as pd

def test_a2z (a2z_file) :

  '''
  Test a a2z file to check that it is valid. The function
  checks the bounds set for the parameters, convert the a2z
  DataFrame to pkb

  :param a2z_file: path of the a2z file to test.
  :type a2z_file: str

  :return: state of the file. If the file is valid, the function
    will return ``True``, ``False`` otherwise.    
  :rtype: bool
  '''

  df_a2z = read_a2z (a2z_file)
  check_a2z (df_a2z, verbose=True) 
  pkb = a2z_to_pkb (df_a2z)
  df_pkb = pd.DataFrame (data=pkb)
  
  print (df_a2z)
  print (df_pkb.to_string ())
  print (get_list_order (df_a2z))

  state = True

  assert ~np.any (np.isnan (pkb)), 'The pkb array contains NaN.' 

  return df_a2z, pkb


if __name__ == '__main__' :

  f = importlib.resources.path (templates, 'test.a2z')
  with f as filename :
    df_a2z, pkb = test_a2z (filename)
  assert np.all (get_list_order (df_a2z)==[5, 21, 22]), 'The list of order read from the a2z DataFrame is not correct'
  f = importlib.resources.path (templates, 'verif.pkb')
  with f as filename :
    verif_pkb = np.loadtxt (filename)
  residual = np.abs (pkb - verif_pkb)
  error = np.linalg.norm (residual.ravel(), ord=np.inf)
  assert error < 1.e-6, 'The pkb array does not contain the expected values.'
  freq = np.linspace (0, 5000, 10000)
  model = compute_model (freq, pkb)
  assert ~np.any (np.isnan (model)), 'The model built from the test pkb array contains NaN.'





