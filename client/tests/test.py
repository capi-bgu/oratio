import unittest

if __name__ == '__main__':
    use_input = True

    auto_tests = [
        'collection.KeyboardCollectorTest',
        'collection.MouseCollectorTest',

        'processing.CameraProcessorTest',
        'processing.KeyboardProcessorTest',
        'processing.MouseProcessorTest',
        'processing.SessionMetaProcessorTest',

        'database.sqlite_db.SqliteManagerTest',
        # 'database.sqlite_db.SessionDataHandlerTest',
        'database.sqlite_db.CameraDataHandlerTest',
        'database.sqlite_db.KeyboardDataHandlerTest',
        'database.sqlite_db.MouseDataHandlerTest',
        'dabases.sqlite_db.SessionMetaDataHandlerTest',

        'integration.collecting_processing.KeyboardTest',
        'integration.collecting_processing.MouseTest',

        'integration.processing_db.CameraTest',
        'integration.processing_db.KeyboardTest',
        'integration.processing_db.MouseTest',
        'integration.processing_db.SessionMetaTest',

        'integration.collecting_processing_db.KeyboardTest',
        'integration.collecting_processing_db.MouseTest'
    ]
    input_test = [
        'collection.CameraCollectorTest',
        'collection.SessionMetaCollectorTest',
        'integration.collecting_processing.CameraTest',
        'integration.collecting_processing.SessionMetaTest',
        'integration.collecting_processing_db.CameraTest',
        'integration.collecting_processing_db.SessionMetaTest'
    ]

    if use_input:
        for test in input_test:
            auto_tests.append(test)

    suite = unittest.TestSuite()
    for test in auto_tests:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(test, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))

    unittest.TextTestRunner().run(suite)
