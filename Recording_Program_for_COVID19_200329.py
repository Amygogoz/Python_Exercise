# @File:
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
    id_num = input("请输入您的身份证号或q退出：")
    if id_num == 'q':
        quit()
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
            print("您输入的身份证号码错误，请重新输入正确的身份证号码。")
            return check_id()
        else:
            print("您的身份证号码为： ", id_num)
            return id_num

def check_temp():
    temp = input("请输入您的体温或q退出：")
    if temp == 'q':
        quit()
    if check_type(temp):
        return float(temp)
    else:
        print("您输入的体温有误，请重新输入正确的体温。")
        return check_temp()

def main():
    id_num = check_id()
    temp = check_temp()
    if temp > 37.3 and id_num[0:4] == '4201':
        print("由于您是武汉籍且有发烧症状，请您尽快尽快到医院就诊")
        file = open("need_to_report.txt", "w+")
        message = "id: " + id_num + ', temperature: ' + str(temp)
        file.write(message)
        file.close()
    elif temp > 37.3 and id_num[0:4] != '4201':
        print("您有发烧症状，请您居家隔离")
        write2txt(id_num, temp)
    elif temp <= 37.3 and id_num[0:4] == '4201':
        print("由于您是武汉籍，请您居家隔离")
        write2txt(id_num, temp)
    else:
        print("您的体温一切正常，无须强制居家隔离")
    main()

if __name__ == '__main__':
    main()
