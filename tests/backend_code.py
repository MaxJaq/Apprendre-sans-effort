import re


def compare_input_wt_expected(input_expected, input_entered, split_args=[' '], keywords_categories=None, keywords_constraints=None, verbose=False):
    """
    Compares two inputs: the expected answer with the entered one. The goal is to enable a more advanced comparison than an exact match:
    1. Comparison methods (keywords_categories):
    - The simplest comparison is the exact method (inputs are identical).
    - More advanced comparisons involve keywords that can be variable (the name of a constant) or bonuses (the right indentation, i.e. spaces). It is thus specified within a dictionary, e.g. {'exact':[for, to], 'variable':[1, 10], 'bonus', ['   ']}
    2. keywords_constraints:
    - Some keywords should remain identical along the text although the comparison method is variable.

    Warning: for now the function is fully case sensitive. But it isn't sensitive to indentation.
    """
    #TODO: transform into an object (that will have different properties for the different domains)

    # Transform split args list for into a regex-readable list
    split_args_re = '|'.join(split_args)

    # Split keywords
    split_expected = re.split(split_args_re, input_expected)
    split_entered = re.split(split_args_re, input_entered)
    
    if verbose:
        print(split_expected)
        print(split_entered)
        
    diff = 0


    # ----- Exact method -----
    #TODO: transform into a list comprehension command
    #TODO: add the list indicating the penalty for each word
    for i, _ in enumerate(split_entered):
        if split_entered[i] != split_expected[i]:
            diff += 1 # should be different for some keywords
        

    # TODO: To implement later
    # elif keywords_categories['exact'] or keywords_categories['variable'] or keywords_categories['bonus']:
    #     # ----- Variables and bonuses methods -----
    #     print("dic")
    #     for i, _ in enumerate(split_entered):
    #         # Treat exact keywords
    #         if split_entered[i] != split_expected[i] and split_expected[i] in keywords_categories['exact']:
    #             diff += 1
    #         # Treat bonus keywords
    #         elif split_entered[i] == split_expected[i] and split_expected[i] in keywords_categories['bonus']:
    #             diff -= 1
    #         #TODO: see how to check the identation
    #         elif split_entered[i] == split_expected[i] and split_expected[i] in keywords_categories['variable']:
    #             #TODO: concerning constraints, in this case, the name of the variable should remain the same
    #             #TODO: also, it should refer to constraints to check which values the variable name can be, since it mostly is anything but signs like '=' or '-'. But that holds only for coding courses.
    #             None
        
    return diff



if __name__ == '__main__':

    # Website:
    # "How to create a for loop with 10 prints of 'ok'?"
    INPUT_ENTERED = "For i = 1 to 11   print('ok')   Next i"
    
    # The question should be built up-front with the following specificities (filling a form).
    # Thus, these should later (when implemented) come from the data base.
    INPUT_EXPECTED = "For i = 1 to 11   print('ok')   Next i"
    KEYWORDS_CATEGORIES={
            'exact':['For', '=', 'to', 'Next'],
            'variable':['i'],
            'bonus':[' ']
            }

    # Compute the difference
    diff = compare_input_wt_expected(
        input_expected = INPUT_EXPECTED,
        input_entered = INPUT_ENTERED,
        split_args = [' '],
        keywords_categories = KEYWORDS_CATEGORIES)

    # Display the result
    print('\nDiff is', diff)

