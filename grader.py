#!/usr/bin/python

from optparse import OptionParser
import sys
import os
import time
from subprocess import STDOUT, check_output as qx


program_file = 'Task'
grader_file = 'Grader'
output_user_file = 'output_user.txt'
compile_command = '/usr/bin/g++ -DEVAL -static -O2 -std=c++0x -o ' # + source_file

def main(argv):
    parser = OptionParser()
    parser.add_option('-i', '--input_dir', action='store', type='string', dest='input_dir', default='test_data')
    parser.add_option('-o', '--output_dir', action='store', type='string', dest='output_dir', default='test_data')
    parser.add_option('-s', '--source', action='store', type='string', dest='source_file', default=None)
    parser.add_option('-g', '--grader', action='store', type='string', dest='grader', default=None)
    parser.add_option('-t', '--timeout', action='store', type='float', dest='timeout', default=2)

    (opts, args) = parser.parse_args(argv)
    source, dir_in, dir_out, grader = opts.source_file, opts.input_dir, opts.output_dir, opts.grader
    print (source, dir_in, dir_out, grader)
    global timeout_seconds
    timeout_seconds = opts.timeout
    if source is None or \
            not os.path.isfile(source) or \
            not os.path.isdir(dir_in) or \
            (grader is None and not os.path.isdir(dir_out)) or \
            (grader is not None and not os.path.isfile(grader)):
        parser.print_help()
        return -1

    if os.path.exists(program_file): os.remove(program_file)
    os.system(compile_command + program_file + ' ' + source)

    if not os.path.exists(program_file):
        print "Compilation Error"
        return -1

    if grader is not None:
        if os.path.exists(grader_file): os.remove(grader_file)
        os.system(compile_command + grader_file + ' ' + grader)
        if not os.path.exists(grader_file):
            print "Grader Compilation Error"
            return -1

    if grader is None and dir_in != dir_out:
        print evaluate_two_dir(dir_in, dir_out)
    elif grader is None:
        print evaluate_one_dir(dir_in)
    else:
        print evaluate_grader(dir_in)

def seperate_in_out(files):
    files_in, files_out = [],[]
    for file in files:
        files_in.append(file) if 'in' in str(file) else files_out.append(file)
    return (files_in, files_out)

def evaluate_one_dir(dir):
    files_in, files_out = seperate_in_out(os.listdir(dir))
    files_in = [dir + '/' + file for file in files_in]
    files_out = [dir + '/' + file for file in files_out]
    return evaluate(files_in,files_out)

def evaluate_two_dir(dir_in, dir_out):
    files_in = [dir_in + '/' + file for file in os.listdir(dir_in)]
    files_out = [dir_out + '/' + file for file in os.listdir(dir_out)]
    return evaluate(files_in,files_out)

def evaluate_grader(dir_in):
    counter = 0
    files_in = [dir_in + '/' + file for file in os.listdir(dir_in)]
    for file in files_in:
        if score_grader(file):
            counter+=1
    return str(counter) + ' Ok out of ' + str(len(files_in))

def evaluate(files_in, files_out):
    counter = 0
    files_in.sort()
    files_out.sort()
    for i in range(len(files_in)):
        if score_file(files_in[i],files_out[i]):
            counter+=1
    return str(counter) + ' Ok out of ' + str(len(files_in))

def score_file(input_file,answer_file):
    output_user = execute_once('./'+program_file+ ' < '+ input_file).replace('\n',' ').replace(' ','')
    answer = open(answer_file, 'r').read().replace('\n',' ').replace(' ','')
    return output_user == answer

def score_grader(input_file):
    output_user = execute_once('./'+program_file+ ' < '+ input_file)
    open(output_user_file,'w').write(output_user)
    output_grader = execute_once('./'+grader_file+ ' < '+ output_user_file)
    return( 'yes' in output_grader or 'Yes' in output_grader or
                    'YES' in output_grader or 'true' in output_grader or
                    '1' in output_grader or 'OK' in output_grader or
                    'ok' in output_grader or 'Ok' in output_grader)

def execute_once(command):
    command = "timeout "+ str(timeout_seconds)+ "s " + command
    start_time = time.clock()
    res = os.popen(command).read()
    if(time.clock()-start_time >= timeout_seconds):
        return "Time Limit Exceeded"
    return res
    #return qx(command, stderr=STDOUT, timeout=timeout_seconds)



if __name__ == "__main__":
    main(sys.argv)