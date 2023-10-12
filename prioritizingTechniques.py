import abc

class prioritizingTechniques():
    def __init__(self, test_cases, criteria):
        self.test_cases = test_cases
        self.criteria = criteria

    @abc.abstractmethod
    def coverage(self):
        raise NotImplementedError
    
    def get(self, test_cases,criteria):
        selected_tests = []
        total = set()
        covered = set()

        for test_case in test_cases:
            coverage_info = self.get_coverage(test_case,criteria)
            total.update(coverage_info['lines'])
            print("done with total update ")

        for test_case in test_cases:
            if len(covered) >= len(total):
                break
            coverage_info = self.get_coverage(test_case,criteria)
            print("got coverage info")
            if len(covered.union(coverage_info["lines"])) == len(covered):
                continue
            covered.update(coverage_info["lines"])
            selected_tests.append(test_case)

        #print(len(covered),len(total))
        return selected_tests

    @classmethod
    def get_coverage(self,testcase,criteria):
        if criteria == "statement":
            return dict({"lines":testcase[3],"count":testcase[1]})
        if criteria == "branch":
            return dict({"lines":testcase[4],"count":testcase[2]})

	