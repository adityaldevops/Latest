#from adapter_keras import KerasAdapter
import os
import json

from model_manager.utils.services.Adapter.adapter_sklearn import SklearnAdapter


class Adapter:

    def __init__(self) -> None:
        pass

    def import_model(self,weights_path):
        
        self.weights_path = weights_path
        self.loaded_model = self.__load_model(weights_path)
        self.model_details = self.__get_model_framework(self.loaded_model)

        if self.model_details["Framework"] == 'sklearn' or self.model_details["Framework"] == 'xgboost' or self.model_details["Framework"] == 'lightgbm':
            if self.model_details["file_type"] == 'dict':
                h,p,a = SklearnAdapter().get_architecture_from_sklearn(self.loaded_model['model object'])
            else:
                h,p,a = SklearnAdapter().get_architecture_from_sklearn(self.loaded_model)
            return h,p,a,self.model_details
        elif self.model_details["Framework"]  == 'tensorflow' or self.model_details["Framework"]  == 'keras':
            pass
        #elif self.model_details["Framework"]  == 'torch':
        #    return self.get_architecture_from_torch()

    def export_model(self, hyperparameters , parameters , attributes, model_details, output_format, export_path, model_name):

        modelfile_name= os.path.join(export_path,model_name)
        model_dictionary = self.__create_model_dict(hyperparameters, parameters, attributes)


        if self.model_details["Framework"] == 'sklearn' or self.model_details["Framework"] == 'xgboost':
            SklearnAdapter().export_to_sklearn(model_dictionary, model_details, output_format, modelfile_name)


    ############################
    ''' Private Functions '''
    ############################

    def __extract_extension(self,weights_path):
        
        split_path = os.path.splitext(weights_path)
  
        # extract the file name and extension
        return split_path[1]
  

    def __load_model(self, weights_path):
        
        extension = self.__extract_extension(weights_path).lower()
        if extension == '.pkl':
            import pickle
            model = pickle.load(open((weights_path).strip("'"),'rb'))
            return model

        elif extension == '.joblib':
            import joblib
            model = joblib.load(open((weights_path).strip("'"),'rb'))
            return model

        elif extension == '.bst':
            import xgboost as xgb
            model = xgb.Booster().load_model(weights_path)

        elif extension == '.h5' or extension == '.hdf5':
            import h5py
            model_file = h5py.File(open((weights_path).strip("'"),'rb'))
            if model_file.attrs.get("backend") == "tensorflow":
                import tensorflow as tf
                model = tf.keras.models.load_model(open((weights_path).strip("'"),'rb'))
                return model

        else:
            print("Unrecognized file type")
            return ""
        

    def __get_model_framework(self,loaded_model):
        """ get model framework whether (tf, sklearn, torch)"""

        model_details = {"file_type":"Empty"}
        model_type = str(type(loaded_model))
        

        model_type = model_type[8:-2]
        print("model-type: ", model_type)
        if model_type == 'dict':
            model_details["file_type"] = 'dict'
            model_type = str(type(loaded_model['model object']))
            model_type = model_type[8:-2]
        model_framework = list(model_type.split("."))
        model_import = list(model_type.rsplit(".",1))
        
        print('\nFramework : ', model_framework[0])
        print('Import statement : ', model_import[0])
        print('Algorithm : ', model_import[1])
        
        model_details["Framework"]= model_framework[0]
        model_details["Library"]=model_import[0]
        model_details["Algorithm"]=model_import[1]

        return model_details

    def __create_model_dict(self,hyperparameters, parameters, attributes):
        model_data_dict = {}
        model_data_dict.update(hyperparameters)
        model_data_dict.update(parameters)
        model_data_dict.update(attributes)

        return model_data_dict
