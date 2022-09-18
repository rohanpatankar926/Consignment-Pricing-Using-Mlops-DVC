import sys
sys.path.append("/home/dataguy/Desktop/Consignment-Pricing-Using-Mlops-DVC-main")
from app import app
import unittest
import pytest


class TestToPerform(unittest.TestCase):
    def setUp(self):
        pass
        self.app=app.test_client()
           
    def test_page(self):
        response0=self.app.get("/",follow_redirects=True)
        print(response0)
        self.assertEqual(response0.status_code,200)
    
    def test_page1(self):
        response1=self.app.get("/predict",follow_redirects=True)
        print(response1)
        self.assertEqual(response1.status_code,200)
    
    def test_page2(self):
        response2=self.app.get("/main",follow_redirects=True)
        print(response2)
        self.assertEqual(response2.status_code,200)

    def test_page3(self):
        response3=self.app.get("/data",follow_redirects=True)
        print(response3)
        self.assertEqual(response3.status_code,200)
        
    def test_page4(self):
        response4=self.app.get("/saved_models",follow_redirects=True)
        print(response4)
        self.assertEqual(response4.status_code,200)

    def test_page5(self):
        response5=self.app.get("/performance",follow_redirects=True)
        print(response5)
        self.assertEqual(response5.status_code,200)
    
    def test_page6(self):
        response6=self.app.get("/logs",follow_redirects=True)
        print(response6)
        self.assertEqual(response6.status_code,200)
        
if __name__=="__main__":
    unittest.main()