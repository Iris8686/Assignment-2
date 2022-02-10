"""
Add LabeledList and Table classes
"""
import csv

class LabeledList(object):
    def __init__(self, data=None, index=None):
        self.data = data
        if not index:
            self.index = [i for i in range(len(self.data))]
        else:
            self.index = index

    def values(self):
        return self.data

    def index(self):
        return self.index

    def __str__(self):
        if self.index:
            max_label_len = max([len(str(i)) for i in self.index])
            max_value_len = max([len(str(i)) for i in self.data])
            s = ""
            for index, value in zip(self.index, self.data):
                padding = '{:>' + str(max_label_len) + '}{:>' + str(max_value_len+1) + '}'
                temp = padding.format(str(index), str(value))
                s = s + temp + "\n"
        else:
            s= ""
        return s

    def __getitem__(self, key_list):
        if isinstance(key_list, LabeledList):
            temp = key_list.values()
            temp_index = []
            temp_value = []
            for i in range(len(self.index)):
                if self.index[i] in temp:
                    temp_index.append(self.index[i])
                    temp_value.append(self.data[i])
            return LabeledList(data=temp_value,index=temp_index)
        elif not isinstance(key_list[0],bool):
            temp_index = []
            temp_value = []
            for i in range(len(self.index)):
                if self.index[i] in key_list:
                    temp_index.append(self.index[i])
                    temp_value.append(self.data[i])
            if len(temp_value)>1 or len(temp_value)==0:
                return LabeledList(data=temp_value, index=temp_index)
            else:
                return temp_value[0]
        else:
            temp_index = []
            temp_value = []
            for i in range(len(key_list)):
                if key_list[i]:
                    temp_index.append(self.index[i])
                    temp_value.append(self.data[i])
            return LabeledList(data=temp_value, index=temp_index)

    def __iter__(self):
        return iter(self.data)

    def __eq__(self,scalar):
        temp_index = []
        temp_value = []
        for i in range(len(self.index)):
            if self.data[i]==scalar:
                temp_index.append(self.index[i])
                temp_value.append("True")
            else:
                temp_index.append(self.index[i])
                temp_value.append("False")
        return LabeledList(data=temp_value, index=temp_index)

    def __ne__(self,scalar):
        temp_index = []
        temp_value = []
        for i in range(len(self.index)):
            if self.data[i]!=scalar:
                temp_index.append(self.index[i])
                temp_value.append("True")
            else:
                temp_index.append(self.index[i])
                temp_value.append("False")
        return LabeledList(data=temp_value, index=temp_index)

    def __gt__(self,scalar):
        temp_index = []
        temp_value = []
        for i in range(len(self.index)):
            if self.data[i] and self.data[i]>scalar:
                temp_index.append(self.index[i])
                temp_value.append("True")
            else:
                temp_index.append(self.index[i])
                temp_value.append("False")
        return LabeledList(data=temp_value, index=temp_index)

    def __lt__(self,scalar):
        temp_index = []
        temp_value = []
        for i in range(len(self.index)):
            if self.data[i] and self.data[i]<scalar:
                temp_index.append(self.index[i])
                temp_value.append("True")
            else:
                temp_index.append(self.index[i])
                temp_value.append("False")
        return LabeledList(data=temp_value, index=temp_index)

    def map(self, f):
        temp_value = []
        for i in range(len(self.data)):
            temp_value.append(f(self.data[i]))
        return LabeledList(data=temp_value, index=self.index)



class Table(object):
    def __init__(self, data, index=None, columns=None):
        self.data = data
        if not index:
            self.index = [i for i in range(len(self.data))]
        else:
            self.index = index

        if not columns:
            self.columns = [i for i in range(len(self.data[0]))]
        else:
            self.columns = columns

    def values(self):
        return self.data

    def index(self):
        return self.index

    def columns(self):
        return self.columns

    def __str__(self):
        column = [""] + self.columns

        s = ""
        for i in column:
            s = s + '{0:{width}}'.format(str(i), width=35)
        s = s + "\n"
        for i in range(len(self.data)):
            temp = [self.index[i]] + self.data[i]
            for j in temp:
                s = s + '{0:{width}}'.format(str(j), width=35)
            s = s + "\n"

        return s

    def __getitem__(self, col_list):
        if isinstance(col_list, LabeledList):
            col_values = col_list.values()
            temp_col = []
            temp_data = []
            for j in range(len(self.data)):
                temp = []
                for i in range(len(self.columns)):
                    if self.columns[i] in col_values:
                        if j == 0:
                            temp_col.append(self.columns[i])
                        temp.append(self.data[j][i])
                temp_data.append(temp)
            return Table(data=temp_data,index=self.index,columns=temp_col)
        elif not isinstance(col_list[0],bool):
            temp_col = []
            temp_data = []
            for j in range(len(self.data)):
                temp = []
                for i in range(len(self.columns)):
                    if self.columns[i] in col_list:
                        if j == 0:
                            temp_col.append(self.columns[i])
                        temp.append(self.data[j][i])
                temp_data.append(temp)
            if len(temp_col)>1 or len(temp_col)==0:
                return Table(data=temp_data,index=self.index,columns=temp_col)
            else:
                temp_data = [i[0] for i in temp_data]
                return LabeledList(data=temp_data, index=self.index)
        else:
            temp_data = []
            temp_index = []
            for i in range(len(col_list)):
                if col_list[i]:
                    temp_data.append(self.data[i])
                    temp_index.append(self.index[i])

            return Table(data=temp_data,index=temp_index,columns=self.columns)

    def head(self,n):
        return Table(data=self.data[:n],index=self.index[:n],columns=self.columns)

    def tail(self,n):
        return Table(data=self.data[-n:],index=self.index[-n:],columns=self.columns)

    def shape(self):
        return (len(self.data),len(self.columns))


def read_csv(fn):
    with open(fn, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        data = []
        for row in my_reader:
            temp = []
            for i in row:
                try:
                    temp.append(float(i))
                except:
                    temp.append(i)
            if len(temp)>0:
                data.append(temp)
        index = [i for i in range(len(data)-1)]
    return Table(data=data[1:],index=index,columns=data[0])
