# @File:Recording_Program_for_COVID19_200412.py
class Person():

    def __init__(self,id_num,temp):
        self.id_num = id_num
        self.temp = temp

    def is_wuhan(self):
        if self.id_num[0:4] == '4021':
            return True
        else:
            return False

    def is_fever(self):
        if self.temp > 37.3:
            return True
        else:
            return False

    def is_report(self):
        if self.is_fever() and self.is_wuhan():
            return True
        else:
            return False

class Sorting():

    itemlist = []
    def reportedTemp(myfilepath):
        Sorting.itemlist = []
        file = open(myfilepath,"r")
        for line in file.readlines():
            info = {}
            info['id'] = line.split(', ')[0].split(' ')[1]
            info['temp'] = float(line.split(', ')[1].split(' ')[1])
            Sorting.itemlist.append(info)

    def quick_sort_temp():
        templist = []
        for info in Sorting.itemlist:
            templist.append(info['temp'])
        sorted_temp = Sorting.quick_sort(templist)
        highest_temp = sorted_temp[-1]

        ids_with_highest_temp = []
        for item in Sorting.itemlist:
            if item['temp'] == highest_temp:
                ids_with_highest_temp.append(item['id'])
        return ids_with_highest_temp, highest_temp

    def partition(nums):
        pivot = nums[0]
        left = [x for x in nums[1:] if x < pivot]
        right = [x for x in nums[1:] if x >= pivot]
        return left,pivot,right

    def quick_sort(nums):
        if len(nums)<=1:
            return nums
        new_left,new_pivot,new_right = Sorting.partition(nums)
        result_sort = Sorting.quick_sort(new_left)+[new_pivot]+Sorting.quick_sort(new_right)
        return result_sort

def write2txt(a, b):
    file = open("observation.txt", "w+")
    file.write("id: {i}, temperature: {t}".format(i=a, t=b))
    file.close()

def check_type(m):
    try:
        float(m)
    except ValueError:
        return False
    else:
        return True

def check_id():
    id_num = input("Please enter your ID number or 'q' to quit: ")
    if id_num == 'q':
        return
    else:
        valid_nums = True
        if len(id_num) != 18:
            valid_nums = False
        else:
            for a in range(17):
                if id_num[a] not in list('0123456789'):
                    valid_nums = False
            if id_num[17] not in list('0123456789Xx'):
                valid_nums = False

        if valid_nums == False:
            print("Your entered an invalid ID number. Please re-enter.")
            return check_id()
        else:
            print("Your ID number is ", id_num)
            return id_num

def check_temp():
    temp = input("Please enter your temperature or 'q' to quit: ")
    if temp == 'q':
        return
    elif check_type(temp):
        return float(temp)
    else:
        print("Your entered an invalid temperature. Please re-enter.")
        return check_temp()

def report():
    id_num = check_id()
    if id_num == None:
        return
    temp = check_temp()
    if temp == None:
        return
    p = Person(id_num, temp)
    if p.is_report():
        print("Since you are from Wuhan and have fever symptoms, please go to see a doctor as soon as possible.")
        file = open("need_to_report.txt", "a+")
        message = "id: " + id_num + ', temperature: ' + str(temp) + "\n"
        file.write(message)
        file.close()
    elif p.is_fever() and not p.is_wuhan():
        print("Since you have fever symptoms, please quarantine at home.")
        write2txt(id_num, temp)
    elif not p.is_fever() and p.is_wuhan():
        print("Since you are from Wuhan, please quarantine at home.")
        write2txt(id_num, temp)
    else:
        print("Your body temperature is within the normal range. No self-quarantine is required.")
    report()

def main():
    Sorting.reportedTemp('need_to_report.txt')
    a,b = Sorting.quick_sort_temp()
    print('Wuhan IDs with the highest body temperature: {}, with the body temperature of {}°C.'.format(a,b))

if __name__ == '__main__':
    report()
    main()
