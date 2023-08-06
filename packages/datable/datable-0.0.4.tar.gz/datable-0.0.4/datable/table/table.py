class Datable:
    '''
    @|@This Class is for displaying data with a dynamic data table, which work like the data grid in sql developer.
    @|@INFO: Header is not valid. You are expected to send out a header list with {0} column(s), but we received {1}. Therefore, header would be generated automatically.
    @|@INFO: Datable descriptions:\n      Header    : {0};\n      Data Count: [{1}][{2}];
    '''
    def __init__(self, data=[], header=[]):
        
        if len(header) != len(data[0]):
            print(self.__doc__.split('@|@')[2].format(len(data[0]), len(header)))
            header = [x + 1 for x in range(len(data[0]))]
        self.__data = data
        self.__header = header
        
    def __str__(self):
         return self.__doc__.split('@|@')[3].format(self.__header, len(self.__data), len(self.__data[0]))
    
    def __add__(self,other):
        newData = self.__data + other.__data
        return Datable(newData, self.__header)
    
    def __sub__(self,other):
        newData = list(filter(lambda x: x not in other.__data, self.__data))
        return Datable(newData, self.__header)
     
    def __and__(self,other):
        newData = list(filter(lambda x: x in other.__data, self.__data))
        return Datable(newData, self.__header)
    
    def __or__(self,other):
        x = self + other
        newData = []
        for each in x.__data:
            if each not in newData:
                newData.append(each)
        print(newData)
        return Datable(newData, self.__header)