import numpy as np

def arrange_data(file_path, **kwargs):
    header = '#'
    
    for key, value in kwargs.items():
        header += '\t {}'.format(key)     
    header += '\n'

    with open(file_path, 'w') as write_file:
        write_file.write(header)

        nbSimus = len(list(kwargs.values())[0])

        for i in range(0, nbSimus):
            data = '{}\t'.format(i)
            for key, value in kwargs.items():
                data += '\t {}'.format("{0:8.4f}".format(value[i])) 
            data += '\n'
            write_file.write(data)

        

    
