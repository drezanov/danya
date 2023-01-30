from ast import parse
import logging, keyboard, sql, asyncio, time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.handler import CancelHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageNotModified, BotBlocked
from aiogram.dispatcher.middlewares import BaseMiddleware
from mildwarres.antiflood import *
bot = Bot(token = '5847034694:AAHxuosN9dhfCdsW5ByoQmvYYO_tXxmnCb4')
dp = Dispatcher(bot, storage = MemoryStorage())
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

class GetLots(StatesGroup):
    photo = State()
    time = State()
    city = State()
    carName = State()
    mileage = State()
    vin = State()
    equipment = State()
    url = State()
    money = State()
    time = State()
    yearOfIssuse = State()
    pts = State()
    numberOfHost = State()
    autoStore = State()
    addAdmin = State()

class CallbackAntiFlood(BaseMiddleware):

    def __init__(self):
        super(CallbackAntiFlood, self).__init__()

    @staticmethod
    async def on_pre_process_callback_query(call: types.CallbackQuery, data: dict):
        if call.message:
            if call.message.from_user:
                dispatcher = Dispatcher.get_current()
                try:
                    await dispatcher.throttle('settings_callback', rate=3)
                except Throttled as throttled:
                    if throttled.exceeded_count <= 2:
                        await call.answer('Вы были заблокированы на 10 секунд из-за попытки спама', show_alert= True)
                        await asyncio.sleep(5)
                                    # Check lock status
                        thr = await dispatcher.check_key('settings_callback')
                        if thr.exceeded_count == throttled.exceeded_count:
                            await call.answer('Вы были разблокированы', show_alert= True)
                    raise CancelHandler()

@dp.message_handler(commands = 'start')
@rate_limit(5, 'start')
async def start(message: types.Message):
    if sql.checkIdUser(message.from_user.id) is None:
        await message.answer('Для продолжения необходимо ознакомиться с нашими правилами\nhttps://cloud.mail.ru/public/YyFu/bU8Nt4s63', reply_markup= keyboard.checkRules())
    else:
        await message.answer(f'Добро пожаловать, {message.from_user.username}\nСсылка на вступление в чат: https://t.me/+mO02r_mhR11hOTVi')

@dp.message_handler(commands='admin')
@rate_limit(5, 'admin')
async def admin(message: types.Message):
    if sql.takeIdAdmins(message.from_user.id):
        await message.answer(f'Добро пожаловать в админку {message.from_user.username}', reply_markup= keyboard.adminMenu)

@dp.callback_query_handler(state = '*')
@rate_limit(3, 'settings_callback')
async def some_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'addAdminInBd':
        await bot.send_message(callback_query.from_user.id, 'Введи id пользователя', reply_markup= keyboard.cancel)
        await GetLots.addAdmin.set()
    elif callback_query.data == 'accept':
        await bot.send_message(callback_query.from_user.id, f'Добро пожаловать, {callback_query.from_user.username}\nСсылка на вступление в чат: https://t.me/+mO02r_mhR11hOTVi')
        sql.add_user(int(callback_query.from_user.id), callback_query.from_user.full_name, callback_query.from_user.username)
    elif callback_query.data == 'decline':
        #Вывод сообщение об отказе
        await bot.send_message(callback_query.from_user.id, 'К сожалению вы отказались от правил. Для повторного прочтения правил, напишите /start')
    elif callback_query.data == 'createLot':
        await bot.send_message(callback_query.from_user.id, 'Отправь фото' , reply_markup= keyboard.cancel)
        await GetLots.photo.set()
    elif callback_query.data == 'cancel':
        await state.finish()
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, 'Отмена создания лота', reply_markup= keyboard.adminMenu)
    elif callback_query.data == 'addMoneyCar':
        data = callback_query.message.caption.split('\n')
        if callback_query.from_user.id != sql.reloadLot(data[6].split(' ')[1]):
            try:
                await asyncio.sleep(3)
                await bot.send_message(sql.reloadLot(data[6].split(' ')[1]), 'Вашу ставку перебили. Срочно вернитесь и перебейте ставку😄\nСсылка на чат: https://t.me/+mO02r_mhR11hOTVi')
            except BotBlocked:
                pass
            sql.updateMoney(callback_query.from_user.id, 3000, callback_query.from_user.username, data[6].split(' ')[1], callback_query.from_user.first_name)
            name = sql.selectFullName(data[6].split(' ')[1]) if sql.selectUserName(data[6].split(' ')[1]) == None else sql.selectUserName(data[6].split(' ')[1])
            await bot.send_message(-1001852442443, f'Пользователь {callback_query.from_user.id} | {callback_query.from_user.username} повысил цену на 3000 #{data[18].split(" ")[3]}')
            await asyncio.sleep(3)
            await bot.edit_message_caption(callback_query.message.chat.id, message_id= callback_query.message.message_id, caption= f''' {data[0]}
{data[1]}
{data[2]}
{data[3]}
{data[4]}
{data[5]}
{data[6]}
{data[7]}
{data[8]}
{data[9]}
{data[10]}
{data[11]}
{data[12]}
{data[13]}
{data[14]}
{data[15]}
{data[16]}
{data[17]}
{data[18]}
✅ Позиция держится за {name[:-2] + "**"}
💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(data[6].split(' ')[1])} RUB''', reply_markup= keyboard.lootAction)
        else:
            await callback_query.answer('Вы не можете перебить свою же ставку', show_alert= True)

    elif callback_query.data == 'addMoneyCar5000':
        data = callback_query.message.caption.split('\n')
        if callback_query.from_user.id != sql.reloadLot(data[6].split(' ')[1]):
            try:
                await asyncio.sleep(3)
                await bot.send_message(sql.reloadLot(data[6].split(' ')[1]), 'Вашу ставку перебили. Срочно вернитесь и перебейте ставку😄\nСсылка на чат: https://t.me/+mO02r_mhR11hOTVi')
            except BotBlocked:
                pass
            sql.updateMoney(callback_query.from_user.id, 5000, callback_query.from_user.username, data[6].split(' ')[1], callback_query.from_user.first_name)
            name = sql.selectFullName(data[6].split(' ')[1]) if sql.selectUserName(data[6].split(' ')[1]) == None else sql.selectUserName(data[6].split(' ')[1])
            await bot.send_message(-1001852442443, f'Пользователь {callback_query.from_user.id} | {callback_query.from_user.username} повысил цену на 5000 в лоте #{data[18].split(" ")[3]}')
            await asyncio.sleep(3)
            await bot.edit_message_caption(callback_query.message.chat.id, message_id= callback_query.message.message_id, caption= f''' {data[0]}
{data[1]}
{data[2]}
{data[3]}
{data[4]}
{data[5]}
{data[6]}
{data[7]}
{data[8]}
{data[9]}
{data[10]}
{data[11]}
{data[12]}
{data[13]}
{data[14]}
{data[15]}
{data[16]}
{data[17]}
{data[18]}
✅ Позиция держится за {name[:-2] + "**"}
💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(data[6].split(' ')[1])} RUB''', reply_markup= keyboard.lootAction)
        else:
            await callback_query.answer('Вы не можете перебить свою же ставку', show_alert= True)

    elif callback_query.data == 'addMoneyCar10000':
        data = callback_query.message.caption.split('\n')
        if callback_query.from_user.id != sql.reloadLot(data[6].split(' ')[1]):
            try:
                await asyncio.sleep(3)
                await bot.send_message(sql.reloadLot(data[6].split(' ')[1]), 'Вашу ставку перебили. Срочно вернитесь и перебейте ставку😄\nСсылка на чат: https://t.me/+mO02r_mhR11hOTVi')
            except BotBlocked:
                pass
            sql.updateMoney(callback_query.from_user.id, 10000, callback_query.from_user.username, data[6].split(' ')[1], callback_query.from_user.first_name)
            name = sql.selectFullName(data[6].split(' ')[1]) if sql.selectUserName(data[6].split(' ')[1]) == None else sql.selectUserName(data[6].split(' ')[1])
            await bot.send_message(-1001852442443, f'Пользователь {callback_query.from_user.id} | {callback_query.from_user.username} повысил цену на 10000 #{data[18].split(" ")[3]}')
            await asyncio.sleep(3)
            await bot.edit_message_caption(callback_query.message.chat.id, message_id= callback_query.message.message_id, caption= f''' {data[0]}
{data[1]}
{data[2]}
{data[3]}
{data[4]}
{data[5]}
{data[6]}
{data[7]}
{data[8]}
{data[9]}
{data[10]}
{data[11]}
{data[12]}
{data[13]}
{data[14]}
{data[15]}
{data[16]}
{data[17]}
{data[18]}
✅ Позиция держится за {name[:-2] + "**"}
💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(data[6].split(' ')[1])} RUB''', reply_markup= keyboard.lootAction)
        else:
            await callback_query.answer('Вы не можете перебить свою же ставку', show_alert= True)

@dp.message_handler(state= GetLots.addAdmin)
async def addAdm(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer('Успешно')
        sql.adduser(message.text)
        await state.finish()
    else:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')


@dp.message_handler(content_types='photo', state = GetLots.photo)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(photo = message.photo[-1].file_id)
    try:
        await message.answer('Отправь продолжительность аукциона: ', reply_markup= keyboard.cancel)
        await GetLots.time.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

@dp.message_handler(content_types='text', state = GetLots.time)
async def getPhoto(message: types.Message, state: FSMContext):
    try:
        await state.update_data(time = int(message.text))
        await message.answer('Введите город продажи: ', reply_markup= keyboard.cancel)
        await GetLots.city.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')
@dp.message_handler(content_types='text', state = GetLots.city)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(city = message.text)
    await message.answer('Введи название машины: ', reply_markup= keyboard.cancel)
    await GetLots.carName.set()

@dp.message_handler(content_types='text', state = GetLots.carName)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(NAME = message.text)
    await message.answer('Введи пробег авто: ', reply_markup= keyboard.cancel)
    await GetLots.mileage.set()

@dp.message_handler(content_types='text', state = GetLots.mileage)
async def getPhoto(message: types.Message, state: FSMContext):
    try:
        await state.update_data(mile = int(message.text))
        await message.answer('Введи VIN авто', reply_markup= keyboard.cancel)
        await GetLots.vin.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

@dp.message_handler(content_types='text', state = GetLots.vin)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(vin = message.text)
    await message.answer('Введи комплектацию авто: ', reply_markup= keyboard.cancel)
    await GetLots.equipment.set()

@dp.message_handler(content_types='text', state = GetLots.equipment)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(equipment = message.text)
    await message.answer('Отправь ссылку на информация об авто: ', reply_markup= keyboard.cancel)
    await GetLots.url.set()

@dp.message_handler(content_types='text', state = GetLots.url)
async def getPhoto(message: types.Message, state: FSMContext):
    await state.update_data(url = message.text)
    await message.answer('Напиши цену авто: ', reply_markup= keyboard.cancel)
    await GetLots.yearOfIssuse.set()

@dp.message_handler(content_types='text', state = GetLots.yearOfIssuse)
async def getYear(message: types.Message, state: FSMContext):
    try:
        await state.update_data(price = message.text)
        await message.answer('Напиши год выпуска авто: ', reply_markup= keyboard.cancel)
        await GetLots.pts.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

@dp.message_handler(content_types='text', state = GetLots.pts)
async def getPts(message: types.Message, state: FSMContext):
    try:
        await state.update_data(year = message.text)
        await message.answer('ПТС: ', reply_markup= keyboard.cancel)
        await GetLots.numberOfHost.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

@dp.message_handler(content_types='text', state = GetLots.numberOfHost)
async def get(message: types.Message, state: FSMContext):
    await state.update_data(pts = message.text)
    await message.answer('Введи количество хозяинов: ', reply_markup= keyboard.cancel)
    await GetLots.autoStore.set()

@dp.message_handler(content_types='text', state = GetLots.autoStore)
async def get(message: types.Message, state: FSMContext):
    try:
        await state.update_data(host = message.text)
        await message.answer('Отправь ссылку на автотеку: ', reply_markup= keyboard.cancel)
        await GetLots.money.set()
    except:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

@dp.message_handler(content_types='text', state = GetLots.money)
async def getPhoto(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        sql.addMoneyTime(data['price'], data['time'], data['vin'], message.from_user.id)
        numberLot = sql.selectLotNumber()
        new_message = await bot.send_photo(-1001549993039, data['photo'], caption = f''' ‼️Продолжительность аукциона - {data['time']} ч до {sql.takeTime(data['vin'])}.‼️
🔥СТАРТ {data['price']} ₽🔥
🌍{data['city']}
✅{data['NAME']}
✅Год выпуска: {data['year']}
✅Пробег: {data['mile']}
✅VIN: {data['vin']}
✅Комплектация: {data['equipment']}
✅ПТС: {data['pts']}
✅Кол-во хозяев: {data['host']}

📸 Подробная информация об авто и фото -
{data['url']}
📸 Cсылка на автотеку -
{message.text}
При возникновении проблем с просмотром информации обращайтесь к администратору
https://t.me/Airat_Khadiev

📌 Лот № {numberLot}
💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(data['vin'])} RUB''', reply_markup= keyboard.lootAction)
        loop = asyncio.get_event_loop()
        loop.create_task(scheduled(1, data['price'], data['city'], data['NAME'], data['mile'], data['vin'], data['equipment'], data['url'], data['time'], new_message.message_id, numberLot, data['year'], message.text, data['pts'], data['host']))
        await state.update_data(newMessage = new_message)
        await state.finish()
        sql.updateLotNumber(1)
        successSendMail = 0
        blockBotuser = 0
        text = f'Создан новый лот. Продолжительность аукциона {data["time"]} ч. Посмотри скорее что там выставили'
        info = sql.mess_admin()
        await bot.send_message(message.from_user.id, 'Рассылка начата!')
        for i in range(len(info)):
            try:
                time.sleep(1)
                await bot.send_message(info[i][0], str(text))
                successSendMail += 1
            except:
                sql.delete(info[i][0])
                blockBotuser += 1
                continue
        await bot.send_message(message.from_user.id, f'🟢Рассылка закончена\n✅Всего отправлено сообщений: {successSendMail}\n🔴Пользователи заблокировавшие бота: {blockBotuser}')
    except ValueError:
        await message.answer('Необходимо вводить только цифры. Введи ещё раз')

async def scheduled(wait_for, price, city, name, mile, vin, equip, url, timeSet, messageId, numberLot, year, autoStore, pts, host):
    while True:
        await asyncio.sleep(wait_for)
        if sql.takeTime(vin) < time.strftime('%H:%M:%S',time.localtime(time.time())):
            if sql.selectUserName(vin) is not None or sql.selectFullName(vin) is not None:
                nameUser = sql.selectFullName(vin) if sql.selectUserName(vin) == None else sql.selectUserName(vin)
                try:
                    await bot.edit_message_caption(-1001549993039, message_id=messageId, caption = f''' ‼️Продолжительность аукциона - {timeSet} ч.‼️
🔥СТАРТ {price} ₽🔥
🌍{city}
✅{name}
✅Год выпуска: {year}
✅Пробег: {mile}
✅VIN: {vin}
✅Комплектация: {equip}
✅ПТС: {pts}
✅Кол-во хозяев: {host}

📸 Подробная информация об авто и фото -
{url}
📸 Cсылка на автотеку -
{autoStore}
При возникновении проблем с просмотром информации обращайтесь к администратору
https://t.me/Airat_Khadiev

📌 Лот {numberLot}
{sql.selectBalance(vin)} RUB - {nameUser[:-2] + "**"}

💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(vin)} RUB''')
                    await bot.send_message(-1001852442443, f'Пользователь @{nameUser} победил в аукционе №{numberLot} с окончательной ценой {sql.selectBalance(vin)}')
                    text = f'Лот под номером {numberLot} окончен. Всем спасибо за участие!'
                    info = sql.mess_admin()
                    for i in range(len(info)):
                        try:
                            time.sleep(1)
                            await bot.send_message(info[i][0], str(text))
                        except:
                            continue
                    sql.deleteLot(vin)
                    break
                except MessageNotModified:
                    pass
            else:
                try:
                    await bot.edit_message_caption(-1001549993039, message_id=messageId, caption = f''' ‼️Продолжительность аукциона - {timeSet} ч.‼️
🔥СТАРТ {price} ₽🔥
🌍{city}
✅{name}
✅Год выпуска: {year}
✅Пробег: {mile}
✅VIN: {vin}
✅Комплектация: {equip}
✅ПТС: {pts}
✅Кол-во хозяев: {host}

📸 Подробная информация об авто и фото -
{url}
📸 Cсылка на автотеку -
{autoStore}
При возникновении проблем с просмотром информации обращайтесь к администратору
https://t.me/Airat_Khadiev

📌 Лот {numberLot}
🔴 Лот закрыт без покупателя
💰 ТЕКУЩАЯ ЦЕНА: {sql.selectBalance(vin)} RUB''')
                    await bot.send_message(-1001852442443, f'Лот под номером {sql.selectLotNumber()} закончился без покупателя!')
                    text = f'Лот под номером {numberLot} окончен. Всем спасибо за участие!'
                    info = sql.mess_admin()
                    for i in range(len(info)):
                        try:
                            time.sleep(1)
                            await bot.send_message(info[i][0], str(text))
                        except:
                            continue
                    sql.deleteLot(vin)
                    break
                except MessageNotModified:
                    pass
        else:
            pass
if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CallbackAntiFlood())
    executor.start_polling(dp, skip_updates = True)
