import sqlite3

connect = sqlite3.connect('./bd.db', check_same_thread = False)
cursor = connect.cursor()

try:
    def add_user(user_id: int, user_name: str, loginUser: str):
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', [user_id])
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO users (user_id, userName, loginUser) VALUES(?, ?, ?);', [user_id, user_name, loginUser, ])
            connect.commit()
except sqlite3.ProgrammingError:
    pass

def addMoneyTime(balance, timeNow, vin, user_id):
    cursor.execute(f'INSERT INTO editLot(money, time, timeLeft, vin, user_id) VALUES(?, time("now", "3 hours"), time("now", "{timeNow + 3} hours"), ?, ?);', [int(balance), vin, user_id,])
    # cursor.execute(f'UPDATE editLot SET time = time("now", "3 hours"), timeLeft = time("now", "{timeNow + 3} hours");')
    connect.commit()

def updateMoney(user_id, balance, userName, vin, full_name):
    bal = cursor.execute('select money FROM editLot WHERE vin = ?;', [vin, ]).fetchone()[0]
    cursor.execute('UPDATE editLot SET user_id = ?, money = ?, nameUser = ?, userName = ? WHERE vin = ?;', [int(user_id), int(balance) + bal, userName, full_name, vin])
    connect.commit()

def selectBalance(vin):
    return cursor.execute('select money FROM editLot WHERE vin = ?;', [vin, ]).fetchone()[0]

def takeTime(vin):
    return cursor.execute('SELECT timeLeft From editLot WHERE vin = ?', [vin, ]).fetchone()[0]

def selectLotNumber():
    return cursor.execute('SELECT lotNumber FROM lot').fetchone()[0]

def updateLotNumber(number):
    numberLot = selectLotNumber()
    cursor.execute('UPDATE lot SET lotNumber = ?;', [int(number) + numberLot, ])
    connect.commit()

def selectUserName(vin):
    return cursor.execute('SELECT nameUser FROM editLot WHERE vin = ?', [vin, ]).fetchone()[0]

def takeIdAdmins(id):
    return cursor.execute('SELECT admins FROM adminsTeam WHERE admins = ?', (id, )).fetchall()

def reloadLot(id):
    try:
        return cursor.execute('SELECT user_id FROM editLot WHERE vin = ?',[id, ]).fetchone()[0]
    except TypeError:
        print(exceptions)

def mess_admin():
    return cursor.execute('SELECT user_id FROM users').fetchall()

def delete(user):
    cursor.execute('DELETE FROM users WHERE user_id = ?', [user])
    connect.commit()

def selectFullName(vin):
    return cursor.execute('SELECT userName FROM editLot WHERE vin = ?', [vin, ]).fetchone()[0]

def deleteLot(vin):
    cursor.execute('DELETE FROM editLot WHERE vin = ?', [vin])
    connect.commit()

def adduser(id):
    cursor.execute('INSERT INTO adminsTeam(admins) VALUES(?)', [id, ])
    connect.commit()

def deleteLoot(vin):
    cursor.execute('DELETE FROM editLot WHERE vin=?;', [vin, ])
    connect.commit()

def checkIdUser(id):
    return cursor.execute('SELECT user_id FROM users WHERE user_id = ?', [id]).fetchone()
