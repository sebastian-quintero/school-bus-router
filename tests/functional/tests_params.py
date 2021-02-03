import unittest

from models.params import Params


class TestsParams(unittest.TestCase):
    """Tests for the Params class"""

    def test_from_dict_complete(self):
        """
        Asserts a Params class is correctly instantiated from
        a complete dict
        """

        params_dict = {
            'GEOHASH_PRECISION_GROUPING': 8,
            'FIRST_SOLUTION_STRATEGY': 'AUTOMATIC',
            'SEARCH_METAHEURISTIC': 'AUTOMATIC',
            'SEARCH_TIME_LIMIT': 4,
            'SEARCH_SOLUTIONS_LIMIT': 3000,
        }
        params = Params.from_dict(params_dict)
        self.assertTrue(
            params,
            msg='Params could not be instantiated from dict.'
        )

        keys = Params.__dataclass_fields__.keys()
        for k in keys:
            self.assertEqual(
                params_dict[k], params.__getattribute__(k),
                msg=f'Key {k} does not match in Params class.'
            )

    def test_from_dict_empty(self):
        """
        Asserts a Params class is correctly instantiated from
        an empty dict
        """

        params = Params.from_dict({})
        self.assertTrue(
            params,
            msg='Params could not be instantiated from dict.'
        )
        keys = Params.__dataclass_fields__.keys()
        default_params = Params()
        for k in keys:
            self.assertEqual(
                default_params.__getattribute__(k), params.__getattribute__(k),
                msg=f'Key {k} does not match in Params class.'
            )

    def test_from_dict_partial(self):
        """
        Asserts a Params class is correctly instantiated from
        a partial dict
        """

        params_dict = {
            'GEOHASH_PRECISION_GROUPING': 4
        }
        params = Params.from_dict(params_dict)
        self.assertTrue(
            params,
            msg='Params could not be instantiated from dict.'
        )
        keys = Params.__dataclass_fields__.keys()
        default_params = Params()
        for k in keys:
            if k in params_dict.keys():
                self.assertEqual(
                    params_dict[k],
                    params.__getattribute__(k),
                    msg=f'Key {k} does not match in Params class.'
                )
            else:
                self.assertEqual(
                    default_params.__getattribute__(k),
                    params.__getattribute__(k),
                    msg=f'Key {k} does not match in Params class.'
                )
