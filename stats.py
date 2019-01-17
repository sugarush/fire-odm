import unittest
import cProfile
import pstats
import io

#from test.test_modelmeta import ModelMetaTest
#from test.test_model import ModelTest
#from test.test_rethinkdb import RethinkDBModelTest

#suite = unittest.TestLoader().discover('./test')

#def run_tests():
#    unittest.TextTestRunner().run(suite)

#profile = cProfile.run('run_tests()', sort='cumtime', strip_dirs=True)

profile = cProfile.Profile()
profile.enable()

suite = unittest.TestLoader().discover('./test')
unittest.TextTestRunner().run(suite)
#unittest.main()

output = io.StringIO()

stats = pstats.Stats(profile, stream=output)
stats.strip_dirs()
stats.sort_stats('cumtime')
stats.print_callees()
stats.print_stats()
stats.dump_stats('.profile')
print(output.getvalue())
