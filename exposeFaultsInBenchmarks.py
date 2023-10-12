import os
import re
import shutil
import csv
import filecmp
import glob

def testsuite_faultexpose(cur_dir,benchmarks,criteria_types,prioritization_methods):
    faultyversion_vfolder = re.compile(r"^v[0-9]+$")
    os.chdir(cur_dir)
    with open('testsuite_faultexpose.csv', 'w', newline='') as csvfile:
        columns = ['benchmark', 'criteria', 'method', 'faults_exposed']
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        i=0
        while i < len(benchmarks):
            benchmark = benchmarks[i]    
            benchmark_path = os.path.join("../benchmarks",benchmark)
            for criteria in criteria_types:
                for method in prioritization_methods:
                    executed_benchmark = os.path.join(benchmark_path,'testsuite_runs/'+method+'-'+criteria+'-executed.txt')
                    faults = 0
                    for subdir in glob.glob(os.path.join(benchmark_path, "v*", "testsuite_runs")):
                        faulty_executed_path = os.path.join(subdir,method+'-'+criteria+'-executed.txt')
                        if os.path.isfile(faulty_executed_path) and not filecmp.cmp(executed_benchmark, faulty_executed_path):
                            faults += 1
                    writer.writerow({'benchmark': benchmark, 'criteria':criteria, 'method': method,'faults_exposed':faults})
            i+=1        

