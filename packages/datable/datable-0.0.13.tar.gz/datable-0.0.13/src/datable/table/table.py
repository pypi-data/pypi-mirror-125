import tkinter as tk
import tksheet
from win32api import GetSystemMetrics

class Datable:
    '''
    |||This Class is for displaying data with a dynamic data table, which work like the data grid in sql developer.
    |||INFO: Header is not valid. You are expected to send out a header list with {0} column(s), but we received {1}. Therefore, header would be generated automatically.
    |||INFO: Datable descriptions:\n      Header    : {0};\n      Data Count: [{1}][{2}];
    |||EROR: Cannot find key: {0};
    '''
    def _msg(self, key):
        return self.__doc__.split('|||')[key]

    def __init__(self, data=[], header=[]):
        
        if len(header) != len(data[0]):
            print(self._msg(2).format(len(data[0]), len(header)))
            header = [x + 1 for x in range(len(data[0]))]
        self.__data = data
        self.__header = header
        
        
        
    def __str__(self):
         return self._msg(3).format(self.__header, len(self.__data), len(self.__data[0]))
    
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
        return Datable(newData, self.__header)
    
    def __getitem__(self, keys):
        def _T(key):
            if key in self.__header:
                dex = int(filter(None, ['{}'.format(i) if x == key else '' for i, x in enumerate(self.__header)])[0])
                T = zip(*self.__data)
                return T, dex
            else:
                raise ValueError(self._msg(4).format(key))
        if type(keys) is str:
            T, dex = _T(keys)
            return zip(T[dex])
        elif type(keys) is tuple:
            matrix = []
            for key in keys:
                T, dex = _T(key)
                matrix.append(T[dex])
            return zip(*matrix)

    def __setitem__(self, keys, value):
        pass

    def __delitem__(self, keys):
        pass
    
    def show(self):
        self.top = tk.Tk()
        Width = GetSystemMetrics(0)
        Height = GetSystemMetrics(1)
        
        sheet = tksheet.Sheet(self.top, width=Width, height=Height, total_columns=len(self.__header))

        sheet.grid()
        sheet.headers(self.__header)
        sheet.set_sheet_data(self.__data)

        # table enable choices listed below:

        sheet.enable_bindings(("single_select",

                               "row_select",

                               "column_width_resize",

                               "arrowkeys",

                               "right_click_popup_menu",

                               "rc_select",

                               "rc_insert_row",

                               "rc_delete_row",

                               "copy",

                               "cut",

                               "paste",

                               "delete",

                               "undo",

                               "edit_cell"))
        windowW = Width if len(self.__header) * 120 + 23 > Width else len(self.__header) * 120 + 23
        windowH = Height if len(self.__header) * 23 + 50 > Height else len(self.__header) * 23 + 50
        self.top.geometry("{}x{}".format(windowW, windowH))
        self.top.mainloop()