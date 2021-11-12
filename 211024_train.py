import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

def make_dataset(file_path):
    x_data = [] # img's pixel value (data)
    y_data = [] # go and turn's value (label)

    # load data
    file_list = os.listdir(file_path)
    for index, tmp_file in enumerate(file_list):

        # make img's data (pixel)
        tmp_x_data = cv2.imread(file_path + tmp_file, cv2.IMREAD_COLOR)
        x_data.append(tmp_x_data/255)
        
        # make label (go, turn)
        tmp_split = tmp_file.split('_')
        tmp_y_data = [float(tmp_split[2]), float(tmp_split[3])] # go, turn
        y_data.append(tmp_y_data)  

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    print("x_data[0] : {}".format(x_data[0]))
    print("y_data[0] : {}".format(y_data[0]))    

    print("x_data_shape : {}".format(x_data.shape))
    print("y_data_shape : {}".format(y_data.shape))

    return x_data, y_data 

def LeNet(input_shape, num_actions):
    model = models.Sequential()

    model.add(layers.Conv2D(32, kernel_size=(5, 5), strides=(1,1),
        padding="same", activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D(pool_size=(2,2), strides=(2,2)))
    model.add(layers.Conv2D(64, kernel_size=(2,2), activation='relu', padding="same"))
    model.add(layers.MaxPooling2D(pool_size = (2,2)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Flatten())
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.Dense(num_actions, activation='linear'))

    print("LeNet's Build Finish")
    
    return model    

if __name__ == "__main__":
    ### input parameter ###############################################
    data_path = "/home/my_nano/211025_data/" # data folder's path
    save_model_path = '211025_mobile_robot.h5' # CNN model's save path
    data_shape = (24, 24, 3) # data(img)'s shpae = Network's input shape
    num_actions_of_data = 2 # Number of actions : go and turn -> 2

    total_epoch = 50 # epoch for Train
    batch_size = 1 # batch size for Train
    split_ratio = 0.2 # Train/Validation's Split Ratio
    ################################################################### 

    # make dataset (data, label)
    x_data, y_data = make_dataset(file_path=data_path)

    # build & compile the Model : LeNet
    model = LeNet(input_shape=data_shape, num_actions=num_actions_of_data)
    model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    
    # Training
    hist = model.fit(x_data, y_data, epochs=total_epoch, batch_size=batch_size, validation_split=split_ratio)
    
    # Save Train Model
    model.save(save_model_path)