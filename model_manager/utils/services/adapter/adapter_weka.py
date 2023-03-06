import inspect
import importlib
import os
import re
from io import StringIO
# import pandas as pd
import numpy as np

class WekaAdapter:

    def __init__(self) -> None:
        pass

    """ Weights, hyperparameters, attribute from the sklearn model """
    def get_architecture_from_weka(self,loaded_model):

        return self.__parameters(loaded_model), self.__hyperparameters(loaded_model)
    
    def export_to_weka(self,model_train_dict, model_details, output_format, modelfile_path):

        model = self.__import_model_objects(model_details)

        model.__dict__=model_train_dict

        self.__create_serialized_object(model , output_format, modelfile_path)

        print("Model exported to {} in {} format".format(model_details["Framework"], output_format))
    


    #########################
    ''' Private Functions '''
    #########################
        
    def __parameters(self,model):
        
        weights_str = model.__repr__()
        weights_list = list(weights_str.split("\n"))
        weights_extract = []
        weights = {}

        for i,j in enumerate(weights_list):
            if j.startswith("="):
                for k in range(i+1,len(weights_list)):
                    if weights_list[k]=='':
                        i=k
                        break
                    else:
                        weights_extract.append(weights_list[k])
                break

        for i,j in enumerate(weights_extract):
            weights_extract[i]=re.sub('\s+', ';',j)
        
        weights_str = '\n'.join(weights_extract)

        StringData = StringIO(weights_str)
        df = pd.read_csv(StringData, sep =";" , header=None)

        header = weights_list[3]
        header=re.sub('\s+', ';',header)
        header=header.split(";")
        header = header[1:]

        weights_dict = df.to_dict('list')
        coef_ , intercept_ = [] , []

        for key,value in weights_dict.items():
            if key==0:
                continue
            else:
                coef_.append(value[:-1])
                intercept_.append(value[-1])

        weights["feature_names_in_"] = weights_dict[0][:-1]
        weights["n_features_in_"] = len(weights_dict[0])-1
        weights["coef_"] = np.array(coef_)
        weights["intercept_"] = np.array(intercept_)
        weights["classes_"] = np.array([x for x in range(len(header)+1)])

        #print("parameters : ",weights)
        return weights
        
    def __methods(self,loaded_model):
        model_schema = inspect.unwrap(loaded_model)
        print("Algorithm : ",model_schema,"\n")
        model_attributes = [x for x in dir(model_schema) if not x.startswith('__')]
        #print("There are {} Model Attributes ".format(len(model_attributes)),"\n")
        
        return model_attributes

        
    def __hyperparameters(self,model):
        hyperparameters_dict = dict()

        hyperparameters = model.options

        for i in range(0,len(hyperparameters),2):
            hyperparameters_dict[hyperparameters[i]]=hyperparameters[i+1]

        #print("hyperparameters : ",hyperparameters_dict)
        return hyperparameters_dict

    def __import_model_objects(self,model_details):
        module_framework = importlib.import_module(model_details["Library"])
        loader = getattr(module_framework, model_details["Algorithm"])
        
        return loader()

    def __create_serialized_object(self,model , output_format, modelfile_name):
        
        if output_format == 'pickle':
            import pickle
            pickle.dump(model, open(modelfile_name+".pkl", 'wb'))
        elif output_format == 'joblib':
            import joblib
            joblib.dump(model, open(modelfile_name+".joblib", 'wb'))

