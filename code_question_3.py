# =============================================================================
# Question 3 - Multilayer perceptron for regression
# =============================================================================
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# =============================================================================
# Main function
# =============================================================================
# This function defines and returns a regression model with 4x4 hidden layers
# It takes in 1 parameter: the number of input nodes (n_cols)

def regression_model (n_cols):
    
    # create the model
    model = Sequential()
    model.add(Dense(4, activation='relu', input_shape=(n_cols,)))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1))
    
    # compile model
    model.compile(optimizer='adam', loss='mean_squared_error',
                  metrics=['mean_squared_error'])
    
    return model

# =============================================================================
# read input files into pandas dataframe
train_data = pd.read_csv('train_data.txt', sep='\t')
train_truth = pd.read_csv('train_truth.txt')
test_data = pd.read_csv('test_data.txt', sep='\t')

# split training dataset into random train and test subsets
X_train, X_test, y_train, y_test = train_test_split(
        train_data, train_truth, test_size=0.2, random_state=1)

# normalize the training and testing subsets and testing data
X_train_norm = (X_train - X_train.mean()) / X_train.std()
X_test_norm = (X_test - X_train.mean()) / X_train.std()
test_data_norm = (test_data - X_train.mean()) / X_train.std()

# obtain the number of features / columns in the training dataset
n_cols = train_data.shape[1]

# construct the Multi Layer Perceptron (MLP) model
model = regression_model(n_cols)

# train the MLP model with training dataset
model.fit(X_train_norm, y_train, validation_data=(X_test_norm, y_test), 
          epochs=100, verbose=2)

# predict output for testing dataset using trained model
test_pred = model.predict(test_data_norm)
test_pred_df = pd.DataFrame(test_pred, columns=['y'])
test_pred_df.to_csv('test_predicted.txt', header=['y'], index=None)

# =============================================================================