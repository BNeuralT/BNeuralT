'''

Anonymous Author(s)

'''
from data_retrival import SettingParamter
from data_loader import data_evaluation
from data_loader import data_partition
from data_processing import DataProcessing
import numpy as np
import os
from datetime import datetime
import time

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)


from datetime import datetime

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
#%%Clasification
#DATA PREPARATION
data_file_set = [
                'iris',     # 0 
                'wisconsin',# 1
                'wine',     # 2
                'heart.csv',# 3
                'ionosphere.csv',# 4
                'australian.csv',# 5
                'pima.csv',   # 6 
                'glass.csv',  # 7
                'vehicle.csv',# 8 
                #
                'dee.csv',    # 9 
                'diabetese.csv',# 10 
                'baseball.csv', # 11 
                'mpg6.csv',     # 12 
                'friedman.csv' # 13
                ]


# set_running = 9

# n_problem_type = 'Classification'
# if (set_running > 8 ):
#     n_problem_type = 'Regression'

# data_file_set = [data_file_set[set_running]]    

# print('\n running : ',data_file_set,'\n')   

solver=['DT']

EPOCHS=500 # 500 
EXP_RUN = 30 # 30

#%%
for runOpt in solver:
    data_results = []
    for j in range(len(data_file_set)):
        print('\n running : ',data_file_set,'\n')      
        if j < 9:
            n_problem_type = 'Classification' # 'Regression' # 'Classification'
        else:
            n_problem_type = 'Regression' # 'Regression' # 'Classification'
        
        data_results_coll = {}
        for exp_num in range(EXP_RUN):    
            data_file = data_file_set[j]
            is_norm = True
            isOptimizeParam = False
            normalize = [0.0, 1.0]
            keep_raw_target = True
            params = SettingParamter.getDataFile(data_file, n_problem_type, is_norm, normalize, keep_raw_target)
            
            dataProcessing = DataProcessing()
            dataProcessing.setParams(params) 
            data_input_values, data_target_values, random_sequence = data_partition(dataProcessing, params.n_validation_method)
            X_train, X_test, y_train, y_test = data_evaluation(params, data_input_values, data_target_values, params.n_validation_method)
            
            inputs = params.n_max_input_attr
            outputs = params.n_max_target_attr
            
            start_time = time.time()
            if n_problem_type == 'Classification':
                model = DecisionTreeClassifier(random_state=0)

                # Train model
                history = model.fit(X_train, y_train)
                
                #prediction            
                #Time computation start
                start_timeFun = time.time()
                y_pred = model.predict(X_train)
                errorTrn =  accuracy_score(y_train, y_pred)
                funcEvltime = (time.time() - start_timeFun) / len(X_train)
                
                #Report Test
                y_pred = model.predict(X_test)
                errorTst =  accuracy_score(y_test, y_pred)
                
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time,' ',exp_num, data_file,' ',runOpt,' test accuracy:', errorTst)
                #collection                
                error = [errorTrn, errorTst, model.get_n_leaves(), funcEvltime, 'empty']
                data_results_coll.update({str(data_file.split('.')[0])+"_"+str(exp_num)+"_"+runOpt: error})
            else:
                model = DecisionTreeRegressor(random_state=0)

                # Train model
                history = model.fit(X_train, y_train)
                
                #prediction            
                #Time computation start
                start_timeFun = time.time()
                y_pred = model.predict(X_train)
                errorTrn =  mean_squared_error(y_train, y_pred)
                funcEvltime = (time.time() - start_timeFun) / len(X_train)
                r2Trn = r2_score(y_train, y_pred)
                
                #Report Test
                y_pred = model.predict(X_test)
                errorTst =  mean_squared_error(y_test, y_pred)
                r2Tst = r2_score(y_test, y_pred)
                
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time,' ',exp_num, data_file,' ',runOpt,' test accuracy:', r2Tst)
                #collection
                error = [errorTrn, errorTst, r2Trn, r2Tst, model.get_n_leaves(), funcEvltime, 'empty']
                data_results_coll.update({str(data_file.split('.')[0])+"_"+str(exp_num)+"_"+runOpt: error})
            #collect all SGDs
            #end for all solve
        #end for each runs
        data_results_coll.update({'model_config':model.get_params()})
        np.save(os.getcwd()+os.sep+'outputs'+os.sep+data_file.split('.')[0]+'_Ep_'+str(EPOCHS)+'_B_All_'+runOpt, data_results_coll)
    #end for each dataum
    #%% save np.load
print('All experiments end. for')
print(data_file_set)
#a = np.load('outputs'+os.sep+'mlp_friedman_Ep_500_B1Sig_l2.npy.npy').item()

#%%
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
clf = DecisionTreeClassifier(random_state=0)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
clf.get_depth()
clf.get_n_leaves()

iris = load_iris()
iris.data
iris.target

#%%
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
regressor = DecisionTreeRegressor(random_state=0)

regressor.fit(X_train,y_train)
y_pred = regressor.predict(X_test)
regressor.get_depth()
regressor.get_n_leaves()

