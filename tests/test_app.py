import tempfile, unittest
from pathlib import Path
import app as site
class TestSite(unittest.TestCase):
    def test_flow(self):
        with tempfile.TemporaryDirectory() as d:
            site.DB=Path(d)/'test.db'
            with site.app.test_client() as c:
                self.assertEqual(c.get('/').status_code,200)
                self.assertEqual(c.get('/health').json,{'status':'ok'})
                self.assertEqual(c.post('/contact').status_code,400)
                with c.session_transaction() as s: token=s['csrf']
                data=dict(csrf=token,name='Test',email='test@example.com',business='Test',message='Inquiry')
                self.assertEqual(c.post('/contact',data=data).status_code,303)
                self.assertEqual(c.post('/contact',data=data).status_code,429)
                with site.connect() as db: self.assertEqual(db.execute('SELECT count(*) FROM leads').fetchone()[0],1)
