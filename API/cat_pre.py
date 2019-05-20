import numpy as np
import pandas as pd
class CatPre(object):
    def __init__(self, dataset = './data/easy_dataset_12.csv', dataset1 = './data/easy_dataset_11.csv'):
        self.dataset, self.dataset1 = self.__load_dataset(dataset, dataset1)
        self.administered_items = []
        self.response_vector = []
        self.parts = []
        self.MAX_PROFILE = 0.8
        self.MAX_QUESTIONS = 20
    def __load_dataset(self, path1, path2):
        assert path1
        assert path2
        df1 = pd.read_csv(path1, index_col = 0)
        df2 = pd.read_csv(path2, index_col = 0)
        
        #print("################## Columns #############")
        #print(type(df.columns))
        return df1, df2
    
    def __part(self, part = 1.0):
        part = float(part)
        assert type(part) == float
        return self.dataset[self.dataset.Parte == part]
    
    def next_item(self, n_item = None, n_response = None):
        if n_item is None or n_response is None:
            return self.__candidate(1, False)
        self.__set_last_value(n_item, n_response)
        cur_p, cur_r = self.__get_last_asked()
        return self.__candidate(cur_p, cur_r)
    def __calculate_percentage(self, part):
        result = 0.0
        cnt = 0
        for i in range(len(self.administered_items)):
            if int(self.parts[i]) == part and self.response_vector[i]:
                result += 1
            if int(self.parts[i]) == int(part):
                cnt += 1
        return 0 if cnt == 0 else result / float(cnt)
    
    def set_current_test_status(self, ai, rv, ps):
        self.administered_items = ai
        self.response_vector = rv
        self.parts = ps
    
    def get_current_test_status(self):
        return self.administered_items, self.response_vector, self.parts
    
    def __ask_next_item(self, part):
        avail = self.__get_avaliable_items_per_part(part)
        rng = np.random.randint(len(avail))
        return avail[rng]
    
    def __get_elements_by_part(self, part):
        return np.array(self.administered_items)[np.array(self.parts) == part]
    
    def __get_avaliable_items_per_part(self, part):
        all_items = self.__part(part).index.values
        curr_items = np.array(self.__get_elements_by_part(part))
        all_items = all_items // 3
        return all_items[np.logical_not(np.isin(all_items, np.array([])))].tolist()
    
    def __get_last_asked(self):
        last = len(self.administered_items) - 1
        if last < 0:
            return None, None
        return self.parts[last], self.response_vector[last]
    
    def __set_last_value(self, n_item, n_response):
        self.administered_items.append(n_item)
        self.parts.append(self.__get_cur_question_part(n_item))
        self.response_vector.append(self.__check_correct_cur_question(n_item, n_response))
    def get_options(self, n_item):
        return [self.dataset1['OPCION_CORRECTA'][n_item * 3 + i] for i in range(0, 3)]
        
    def __get_cur_question(self, n_item):
        return self.dataset1['PREGUNTA'][n_item * 3]
    
    def __get_cur_responses(self, n_item):
        return [self.dataset1['TEXTO'][n_item * 3 + i] for i in range(0, 3)]
    
    def __check_correct_cur_question(self, n_item, n_response):
        return True if str(self.dataset1['OPCION_CORRECTA'][n_item * 3 + n_response]) == "S" else False
    
    def __get_cur_question_part(self, n_item):
        return int(self.dataset1['Parte'][n_item * 3])
    def get_cur_question_part(self, n_item):
        return int(self.dataset1['Parte'][n_item * 3])
    def __get_items_asked_per_part(self, part):
        return np.array(self.administered_items)[np.array(self.parts) == part].tolist()
    
    def __candidate(self, cur_p, cur_r):
        p_part_p = self.__calculate_percentage(cur_p)
        print(f"\nParte: %d\n" % cur_p)
        print("############################ Administered #############################")
        print(self.administered_items)
        print("############################ Response Vec #############################")
        print(self.response_vector)
        print("############################ Parts Evalua #############################")
        print(self.parts)
        print("############################ Probabilityf #############################")
        print((cur_p, p_part_p))      
        part, tru = self.__get_last_asked()
        n_item = 0
        lky = len(self.__get_items_asked_per_part(cur_p))
        if (lky > 2 and p_part_p > self.MAX_PROFILE):
            n_item = self.__ask_next_item(min(3, cur_p + 1))
        elif self.MAX_PROFILE - .1 < p_part_p:
            n_item = self.__ask_next_item(cur_p)
        else:
            n_item = self.__ask_next_item(max(1, cur_p - 1))
        print(f"n_item %d\n" % n_item)
        quest = self.__get_cur_question(n_item)
        responses = self.__get_cur_responses(n_item)
        return (
                self.administered_items,
                self.response_vector,
                self.parts,
                quest,
                responses,
                n_item
        )
if __name__ == "__main__":
    cat_pre = CatPre()
    i = 0
    ai, rv, ps, q, r, ni = None, None, None, None, None, None
    n_response = -1
    while i < 20:
        if i == 0:
            ai, rv, ps, q, r, ni = cat_pre.next_item()
        else:
            ai, rv, ps, q, r, ni = cat_pre.next_item(ni, n_response)
        print(q)
        print(r)
        options = cat_pre.get_options(ni)
        print(options)
        n_response = int(input("Ingrese la respuesta: "))
        cat_pre.set_current_test_status(ai, rv, ps)
        i += 1