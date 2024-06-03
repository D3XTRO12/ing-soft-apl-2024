import requests

class AtomicProcess:
    def execute_ms1(self):
        result = requests.get('http://localhost:5001/api/v1')
        if result.status_code != 200:
            result = self.compensation_ms1()
        return result
    
    def compensation_ms1(self):
        result = requests.get('http://localhost:5001/api/v1/compensation')
        return result
    
    def execute_ms2(self):
        result = requests.get('http://localhost:5002/api/v1')
        if result.status_code != 200:
            result = self.compensation_ms2()
        return result
    
    def compensation_ms2(self):
        result = requests.get('http://localhost:5002/api/v1/compensation')
        self.compensation_ms1()
        return result
    
    def execute_ms3(self):
        result = requests.get('http://localhost:5003/api/v1')
        if result.status_code != 200:
            result = self.compensation_ms3()
        return result
    
    def compensation_ms3(self):
        result = requests.get('http://localhost:5003/api/v1/compensation')
        self.compensation_ms2()
        self.compensation_ms1()
        return result
    
    def execute(self):
        ms1 = self.execute_ms1()
        ms2 = self.execute_ms2()
        ms3 = self.execute_ms3()
        if ms1.status_code == 200 and ms2.status_code == 200 and ms3.status_code == 200:
            return ms3
        else:
            return self.compensation_ms3()