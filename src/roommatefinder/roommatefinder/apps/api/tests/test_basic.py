import unittest

class TestBasic(unittest.TestCase):
  """ Basic tests """
  def test_basic(self):
    a = 1
    self.assertEquals(1, a)