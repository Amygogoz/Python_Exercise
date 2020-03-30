# @File:
id_num = input("请输入您的身份证号码：")
if len(id_num) != 18:
    print("您输入的身份证号码错误，请重新输入正确的身份证号码。")
    quit()
for a in range(17):
    if id_num[a] not in list('0123456789'):
        print("您输入的身份证号码错误，请重新输入正确的身份证号码。")
        quit()
if id_num[17] not in list('0123456789Xx'):
    print("您输入的身份证号码错误，请重新输入正确的身份证号码。")
else:
    print("您的身份证号码为： ", id_num)

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

temp = input("请输入您的体温：")
if check_type(temp):
    temp = float(temp)
    if  temp > 37.3 and id_num[0:4] == '4201':
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
else:
    print("您输入的体温有误，请重新输入正确的体温。")
