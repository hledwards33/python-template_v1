1. for the logging we are using a singleton class design
   2. this design is also good for data base access and such cases where should only be one instance of the class
   3. to create out singleton we use the meta class method without eager loading

2. We should build our tools out using a dataset with standard names and the model framework should have an
   adapter (design pattern) class to convert client raw data into the correct format - mostly this would just be 
   renaming columns

3. Need to build out a model framework structure diagram that will show what the framework does in a graphical format
   this should also include the dependencies between classes.