import unittest
from time import sleep
from ddt import ddt,data

from sele_ssop_test.web_test_login import Testkeywords

@ddt
class Testkey(unittest.TestCase):
    def setUp(self) -> None:
        self.tk = tk = Testkeywords('https://www.baidu.com/', 'chrome')
    def tearDown(self) -> None:
        pass
    @data('龙','云')
    def test_case_01(self,kef_value):
        self.tk.inputs('id', 'kw', kef_value)
        self.tk.click_but('id', 'su')
        sleep(5)


    if __name__ == '__main__':
        unittest.main()