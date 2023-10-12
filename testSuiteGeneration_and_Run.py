import os
import re
import shutil
import csv
import filecmp

class testSuiteGeneration_and_Run:

    def benchmark_testSuite_dir_creation(benchmark, criteria, technique, selected_tests):
        benchmarks_path = os.path.join("..", "benchmarks", benchmark)
        test_num = [int(test_case[0]) for test_case in selected_tests] # Get the test case numbers
        test_inputs = []
        with open(os.path.join(benchmarks_path, 'universe.txt'), 'r') as reader:
            for line_num, line in enumerate(reader.readlines(), 1):
                if line_num in test_num:
                    test_inputs.append(line)
        test_suite_path = os.path.join(benchmarks_path, 'testsuites')
        os.makedirs(test_suite_path, exist_ok=True)
        test_input_path = os.path.join(test_suite_path,technique+'-'+criteria+'-suite.txt')
        with open(test_input_path, 'w') as f:
            f.writelines(test_inputs)



    def run_testsuites(benchmarks,criteria_types,prioritization_methods):
        faultyversion_vfolder = re.compile(r"^v[0-9]+$")
        for benchmark in benchmarks:
            benchmark_path = os.path.join("../benchmarks",benchmark)
            os.chdir(benchmark_path)
            if os.path.exists('testsuite_runs'):
                shutil.rmtree('testsuite_runs')
            os.mkdir('testsuite_runs')
            for criteria in criteria_types:
                for technique in prioritization_methods:
                    for subdir, dirs, files in os.walk(os.getcwd()):
                        for dir in dirs:
                            if faultyversion_vfolder.match(dir):    
                                filename = dir+'/testsuite_runs/'+technique+'-'+criteria+'-executed.txt'
                                if not os.path.exists(os.path.dirname(filename)):
                                    os.mkdir(os.path.dirname(filename))
                                if os.path.exists(filename):
                                    os.remove(filename)
                                with open(filename, 'w'): pass
                    with open(os.path.join('testsuites',technique+'-'+criteria+'-suite.txt'), 'r') as reader:
                        for line in reader.readlines():
                            os.system('./'+benchmark+' '+line.strip()+' >> ./testsuite_runs/'+technique+'-'+criteria+'-executed.txt 2>&1') 
                            for subdir, dirs, files in os.walk(os.getcwd()):
                                for dir in dirs:
                                    if faultyversion_vfolder.match(dir):    
                                        os.system('./'+dir+'/'+benchmark+' '+line.strip()+' >> ./'+dir+'/testsuite_runs/'+technique+'-'+criteria+'-executed.txt 2>&1')
            os.chdir('..')
        os.chdir('..')