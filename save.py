import pickle

with open('save.pickle', 'rb') as f:
    save = pickle.load(f)
    print(save['ants'][0].all_vector_positions)