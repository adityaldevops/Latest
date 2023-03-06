import inspect
import importlib
import os


class SklearnAdapter:

    def __init__(self) -> None:
        pass

    """ Weights, hyperparameters, attribute from the sklearn model """
    def get_architecture_from_sklearn(self,loaded_model):

        return self.__parameters(loaded_model), self.__hyperparameters(loaded_model)
    
    def export_to_sklearn(self,model_train_dict, model_details, output_format, modelfile_path):

        model = self.__import_model_objects(model_details)

        model.__dict__=model_train_dict
        #model.__dict__['multi_class'] = "ovr"

        file_name = self.__create_serialized_object(model , output_format, modelfile_path)

        print("Model exported to {} in {} format".format(model_details["Framework"], output_format))

        return file_name

    


    #########################
    ''' Private Functions '''
    #########################
        
    def __parameters(self,model):
        weights = {i: model.__dict__[i] for i in model.__dict__ if i.endswith('_') and not i.startswith('_')}

        data1 = set(model.__dict__.keys())-set(model.get_params().keys())
        attributes={}
        for i in data1:
            if not i.endswith('_') or i.startswith('_'):
                attributes[i]=model.__dict__[i]
        
        weights.update(attributes)
        return weights
        
    def __methods(self,loaded_model):
        model_schema = inspect.unwrap(loaded_model)
        print("Algorithm : ",model_schema,"\n")
        model_attributes = [x for x in dir(model_schema) if not x.startswith('__')]
        #print("There are {} Model Attributes ".format(len(model_attributes)),"\n")
        
        return model_attributes
        
    def __hyperparameters(self,model):
        hyperparameters_names, hyperparameters_values = [], []


        for i in list(model.get_params().keys()):
            #temp = i.title()
            #hyperparameters_names.append(temp)
            hyperparameters_names.append(i)

        for i in list(model.get_params().values()):
            hyperparameters_values.append(i)

        hyperparameters = dict(zip(hyperparameters_names, hyperparameters_values))
        return hyperparameters

    def __import_model_objects(self,model_details):
        module_framework = importlib.import_module(model_details["Library"])
        loader = getattr(module_framework, model_details["Algorithm"])
        
        return loader(multi_class="multinomial",solver="liblinear")

    def __create_serialized_object(self,model , output_format, modelfile_name):
        
        if output_format == 'pickle':
            import pickle
            modelfile_name = modelfile_name+".pkl"
            pickle.dump(model, open(modelfile_name, 'wb'))
        elif output_format == 'joblib':
            import joblib
            modelfile_name = modelfile_name+".joblib"
            joblib.dump(model, open(modelfile_name, 'wb'))
        
        return modelfile_name