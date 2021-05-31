import itertools

# sequences_dict = {
#     10: '<(bd)cb(ac)>',
#     20: '<(bf)(ce)b(fg)>',
#     30: '<(ah)(bf)abf>',
#     40: '<(be)(ce)d>',
#     50: '<a(bd)bcb(ade)>'
# }


# Removed -2 as the end of a sequence
database = [
    "1 -1 1 2 3 -1 1 3 -1 4 -1 3 6 -1",
    "1 4 -1 3 -1 2 3 -1 1 5 -1",
    "5 6 -1 1 2 -1 4 6 -1 3 -1 2 -1",
    "5 -1 7 -1 1 6 -1 3 -1 2 -1 3 -1"
]
minimum_support = 2


def generate_freq_elements_of_len(k, elements):
    generated = []
    for i in database:
        splitted = i.split(' ')
        for j in splitted:
            if not(j in generated) and not(j == '-1'):
                generated.append(j)

    return generated


def find_freq_elements_reject_on_minmum_support(generated_items):
    result = {}
    for gen_item in generated_items:
        result[gen_item] = sum(x.count(gen_item) for x in database)

    # reject all elements that have lower support than min support
    result_final = { k: v for k, v in result.items() if v >= minimum_support } 

    return list(result_final.keys())

def prepare_tupled_data(database):
    sequence_tuples = []
    for sequence in database:
        tuple_inner_sequence = []
        splitted_tuples = list(map(lambda x: x.replace(' ', ''), sequence.split('-1')))
        splitted_tuples.remove('') # remove empty strings
        for j in splitted_tuples:
            tuple_inner_sequence.append(tuple(j))

        sequence_tuples.append(tuple_inner_sequence)


    return sequence_tuples


tupled_input_data = prepare_tupled_data(database)

print('witam witam witam')
print(tupled_input_data)
print('END witam witam witam')

generated = generate_freq_elements_of_len(1, database)

result = find_freq_elements_reject_on_minmum_support(generated)




# # generate permutations
# k = 2
# while not(find_freq_elements_from_candidates(list(itertools.permutations(result, k)))
#     k = k + 1
# print('RESULT RESULT')
# print()
# print('END RESULT RESULT')

# def find_frequent_el(items)
