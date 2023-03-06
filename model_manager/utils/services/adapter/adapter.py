#from adapter_keras import KerasAdapter
import os
import json

from model_manager.utils.services.adapter.adapter_sklearn import SklearnAdapter
from model_manager.utils.services.adapter.adapter_weka import WekaAdapter
# import weka.core.jvm as jvm
import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
class Adapter:

    def __init__(self) -> None:
        self.model_details = dict()
        # jvm.start()

    def __del__(self):
        # jvm.stop()
        pass

    def import_model(self,weights_url):
        
        self.weights_path = self.__download_blob_from_url(weights_url)
        self.loaded_model = self.__load_model(self.weights_path)
        model_details = self.__get_model_framework(self.loaded_model)

        if self.model_details["Framework"] == 'sklearn' or self.model_details["Framework"] == 'xgboost' or self.model_details["Framework"] == 'lightgbm':
            if model_details["file_type"] == 'dict':
                h,p = SklearnAdapter().get_architecture_from_sklearn(self.loaded_model['model object'])
            else:
                h,p = SklearnAdapter().get_architecture_from_sklearn(self.loaded_model)
            return h,p,model_details
        elif self.model_details["Framework"]  == 'tensorflow' or self.model_details["Framework"]  == 'keras':
            pass
        elif self.model_details["Framework"] == 'weka':
            p,h=  WekaAdapter().get_architecture_from_weka(self.loaded_model)
            return p,h,self.model_details
        #elif self.model_details["Framework"]  == 'torch':
        #    return self.get_architecture_from_torch()

    def export_model(self, hyperparameters , parameters, model_details , output_framework, output_format, export_path, model_name):

        export_base_path = "."
        modelfile_name= os.path.join(export_base_path,model_name)
        model_dictionary = self.__create_model_dict(hyperparameters, parameters)


        if output_framework == 'sklearn' or output_framework == 'xgboost':
            model_details["Framework"] = output_framework
            model_details["Library"] = "sklearn.linear_model._logistic"
            model_details["Algorithm"]= "LogisticRegression"

            print("Got training dictionary: {} \n".format(model_dictionary))

            file_name = SklearnAdapter().export_to_sklearn(model_dictionary, model_details, output_format, modelfile_name)

        local_path = os.path.join(export_base_path,file_name)
        self.upload_to_url(export_path, local_path)





    ############################
    ''' Private Functions '''
    ############################

    def __extract_extension(self,weights_path):
        
        split_path = os.path.splitext(weights_path)
  
        # extract the file name and extension
        return split_path[1]

    def __extract_filename(self,url):
        
        filename = os.path.split(url)[1]
        return filename

    def __download_blob_from_url(self,url):
        blob_name = self.__extract_filename(url)
        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cortexstorageaccount3597;AccountKey=UvEDsaZj7tqLFemPeTnUCjxbYrUINHv1ANh38rcybgeB+vsYYd/ct+VvIXrgQ0nPvkcLF/A6192S+AStunHvXw==;EndpointSuffix=core.windows.net")
        container_client = blob_service_client.get_container_client("content")
        blob_client = container_client.get_blob_client(blob_name)

        # download the blob and save to a file
        with open(blob_name, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

        return blob_name

    def upload_to_url(self, url,local_path):

        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cortexstorageaccount3597;AccountKey=UvEDsaZj7tqLFemPeTnUCjxbYrUINHv1ANh38rcybgeB+vsYYd/ct+VvIXrgQ0nPvkcLF/A6192S+AStunHvXw==;EndpointSuffix=core.windows.net")

        # Create a ContainerClient object
        container_client = blob_service_client.get_container_client("content")

        # Set the path to your file
        #local_path = "/Users/lakshikaparihar/Documents/Jio-Project/cortex/adapter/exported_models"
        file_name = os.path.basename(local_path)

        # Create a BlobClient object for your file
        blob_client = container_client.get_blob_client(file_name)

        # Upload the file to Blob Storage
        with open(local_path, "rb") as data:
            print('data', '\n', data)
            blob_client.upload_blob(data)

        print("Model Uploaded to Azure Blob Storage")


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

        elif extension == '.model':
            from weka.classifiers import Classifier
            model,data = Classifier.deserialize(weights_path)
            return model

        else:
            print("Unrecognized file type")
            return ""
        
        



    def __get_model_framework(self,loaded_model):
        """ get model framework whether (tf, sklearn, torch)"""

        self.model_details["file_type"] = "Empty"
        model_type = str(type(loaded_model))
        

        model_type = model_type[8:-2]
        print("model-type: ", model_type)
        if model_type == 'dict':
            self.model_details["file_type"] = 'dict'
            model_type = str(type(loaded_model['model object']))
            model_type = model_type[8:-2]
        elif model_type.startswith("weka"):
            model_type = str(loaded_model.classname)

            
        model_framework = list(model_type.split("."))
        model_import = list(model_type.rsplit(".",1))
        
        print('\nFramework : ', model_framework[0])
        print('Import statement : ', model_import[0])
        print('Algorithm : ', model_import[1])
        
        self.model_details["Framework"]= model_framework[0]
        self.model_details["Library"]=model_import[0]
        self.model_details["Algorithm"]=model_import[-1]

        return self.model_details

    def __create_model_dict(self,hyperparameters, parameters):
        model_data_dict = {}
        model_data_dict.update(hyperparameters)
        model_data_dict.update(parameters)

        return model_data_dict
