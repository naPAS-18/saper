import numpy as np
import cryptocode # библиотека для зашифровки файла

def generatebomb(high,leng,cb): #генерирует случайным образом бомбы в матрице
    countbomb = 0
    a = [1,0]
    o = np.array([['+']*leng]*high)
    while cb!=countbomb:
	    for i in range(high):
		    for j in range(leng):
			    if cb==countbomb:
				    break
			    if np.random.choice(a, replace = True, p = [0.2 ,0.8]) and o[i][j] != '*':
				    o[i][j]='*'
				    countbomb+=1
    return o

def generate_open_array(high, leng, genbomb): # делает 'открытое' поле
    open_array=genbomb
    for line in range(leng):
        for column in range(high):
            if genbomb[column][line] == '+':
                open_array[column][line] = markup(column, line) 
    return open_array

def markup (column, line): # заполняет ячейки количеством мин-соседей
    left_top = [ column - 1,line - 1]  
    top = [column,line - 1 ]  
    right_top = [ column + 1, line - 1,]  
    left = [column - 1, line ]  
    right = [column + 1, line ]  
    left_bott = [column - 1,line + 1 ]  
    bott = [ column,line + 1]  
    right_bott = [ column + 1, line + 1]  
    res = 0
    for i in (left_top, top, right_top, left, right, left_bott, bott, right_bott):
        a, b = i
        if 0 <= a < high and 0 <= b < leng and genbomb[a][b] == '*':
            res += 1
    return str(res)

def save_match(): # кодирование данных и ввод в файл
    passkey = 'wow'
    str1 = str(high)+' '+str(leng)+' '+str(cb)+' '+str(count)
    str2 = ' '.join(close_array.ravel())
    str3 = ' '.join(open_array.ravel())
    str1 = cryptocode.encrypt(str1,passkey)
    str2 = cryptocode.encrypt(str2,passkey)
    str3 = cryptocode.encrypt(str3,passkey)
    with open('save_match.txt', 'w', encoding = "UTF-8") as inf:
        print(str1, file=inf)
        print(str2, file=inf)
        print(str3, file=inf)

def open_save(): # вывод из файла и декодирование данных
    with open('save_match.txt', 'r', encoding = "UTF-8") as ouf:
        str1 = ouf.readline()#.split()
        str1 = cryptocode.decrypt(str1, "wow").split()
        high, leng, cb, count = int(str1[0]), int(str1[1]), int(str1[2], int(str1[3]))
        str2 = ouf.readline()
        str2 = cryptocode.decrypt(str2, "wow").split()
        str3 = ouf.readline()
        str3 = cryptocode.decrypt(str3, "wow").split()
    return high, leng, cb, count, str2, str3
       
print("Open save(enter 1) or new game(enter 2)?")
m=int(input())
if m-1:
    high = int(input("High: ")) 
    leng = int(input("Length: ")) 
    cb = int(input("Enter the number of * "))
    genbomb = generatebomb(high,leng,cb)
    open_array = generate_open_array(high, leng, genbomb)
    close_array = np.array([['+']*leng]*high)
    count=0
else:
    high, leng, cb, count, close_array, open_array = open_save()
    close_array = np.reshape(close_array,(high,leng)) #hi, le
    open_array = np.reshape(open_array,(high,leng))
print(close_array)
while count!=high*leng-cb: # главный цикл игры
    s=input().split()
    s[0],s[1]=int(s[0]),int(s[1])
    if s[2]=='Open':
        if open_array[s[0]][s[1]]=='*':
            print("Game over!")
            print(open_array)
            break
        else:
            close_array[s[0]][s[1]] = open_array[s[0]][s[1]]
            count+=1
    elif s[2] == 'Flag':
        close_array[s[0]][s[1]] = 'F'
    elif s[2] == 'Unflag':
        close_array[s[0]][s[1]] = '+'
    elif s[2] == 'Save':
        save_match()
        print("The match was saved!")
        break
    print(close_array)
if count==high*leng-cb:
    print('You win!')
