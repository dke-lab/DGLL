from sklearn.preprocessing import LabelEncoder, OneHotEncoder

classes_list_str = ["Case_Based","Genetic_Algorithms","Neural_Networks","Probabilistic_Methods","Reinforcement_Learning","Rule_Learning","Theory"]

def labelEncoding(classes_list):
    # "Generate label encoder for a specific list"
    label_encoder = LabelEncoder()
    label_encoder.fit(classes_list)
    return label_encoder

    # def oneHotEncoding(integer_encoded):
    #     "Generate one hot encoding for a specific integer set"
    #     onehot_encoder = OneHotEncoder(sparse=False)
    #     integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    #     onehot_encoded = onehot_encoder.fit(integer_encoded)
    #     return onehot_encoder
    #

# label_encoder = labelEncoding.labelEncoding(classes_list_str)
label_encoder = LabelEncoder()
label_encoder.fit(classes_list_str)
i = 3
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = label_encoder.reshape(len(label_encoder), 1)
onehot_encoder = onehot_encoder.fit(integer_encoded)

print("classes_list_str[i]", classes_list_str[i])
classes_list_intEncoded = label_encoder.transform(classes_list_str)
print("classes_list_intEncoded[i]:", classes_list_intEncoded[i])

onehot_encoder = labelEncoding.oneHotEncoding(classes_list_intEncoded)
onehot_encoder.transform([[classes_list_intEncoded[i]]])
# print(onehot_encoder.transform([classes_list_intEncoded[i]]))
# print("le.transform()", le.transform([classes_list[i]]))
# print("le.inverse_transform([i])", le.inverse_transform([i]))

# reference : https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
# https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html

