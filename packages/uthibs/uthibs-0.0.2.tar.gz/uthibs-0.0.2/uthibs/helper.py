import inspect
import warnings

def display_function_content(function):
    """ Display the code of the selected function

    Args:
        function ([function]): function to display
    """
    lines = inspect.getsource(function)
    for line in lines:
        print(line)

def notebook_autoreload():
    print('%load_ext autoreload')
    print('%autoreload 2')
    print('%aimport utils')

def add_kernel_to_notebook():
    print('kernel install --user --name=<any_name_for_kernel>')

def text_to_list():
    print('import ast')
    print('ma_list = ast.literal_eval(string)')

def pandas():
    print("pd.set_option('chained_assignment', None)")
    print("pd.set_option('display.max_rows', 500)")
    print("pd.set_option('display.max_columns', 100)")


def silent_warning():    
    warnings.warn('Removing warning from execution context.')
    warnings.filterwarnings("ignore")


