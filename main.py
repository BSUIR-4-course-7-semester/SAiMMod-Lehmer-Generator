import matplotlib.pyplot as plt
from math import sqrt

from lemer import LemerGenerator, HistogramDrawer, UniformityChecker


def main():
    choice = None
    while choice != '0':
        print_menu()
        choice = input()
        if choice == '1':
            make_lemer_calculation()
        elif choice == '0':
            print('Exiting...')
        else:
            print('Incorrect choice')

        print('Enter to continue...')
        input()

def print_menu():
    print('''
        1 - Lemer Calculations
        0 - Exit
    ''')

def make_lemer_calculation():
    print('Lemer Calculations')
    m = None
    r0 = None
    a = None
    error = True
    while error:
        try:
            m = int(input('m: '))
            r0 = int(input('R0: '))
            a = int(input('a: '))
            if not m > a:
                print('m must be higher than a')
                raise ValueError()
            error = False
        except ValueError:
            print('Incorrect input values')

    generator = LemerGenerator(m, r0, a)
    sequence = [i for i in generator]
    print_generator_info(generator)
    # print('Lemer sequence: ', sequence)
    write_sequence_to_file(sequence)
    drawer = HistogramDrawer(sequence)
    uniformityChecker = UniformityChecker(sequence)
    uniformityChecker.check()
    print('Uniformity: ', uniformityChecker.is_uniform)
    drawer.draw()

def write_sequence_to_file(sequence):
    with open('result_sequence.txt', mode='w') as f:
        f.writelines(list(map(lambda v: str(v), sequence)))
        f.close()

def print_generator_info(generator):
    print('Period: ', generator.period)
    print('Aperiodic: ', generator.aperiodic)
    print('Mathematical expectation: ', generator.mathematical_expectation)
    print('Dispersion: ', generator.dispersion)
    print('Root mean square deviation: ', generator.root_mean_square_deviation)

if __name__ == "__main__":
    main()




