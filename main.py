import gspread
import telegram
import jdatetime
import os
import json
import requests
import asyncio
import logging
import datetime
from datetime import datetime
from asyncio import *
from asyncio import sleep
from telegram import __version__, __version_info__, InputFile
from oauth2client.service_account import ServiceAccountCredentials
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters, Updater)
from userPro import userPRo
from userMAIL import userMAIL
from userNormal import userNormal
from allData import allData
import random

bot = telegram.Bot("7276392721:AAFHezJjyCMSY51Y7zr-TLvbAVlgRBK217Y")
update_queue: "asyncio.Queue"
tax = range(1)


binance_api = '5VRI7ZYJ545MTUBVT2EVPXGJG7SGAX24J9'


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


reply_keyboard = [["My Account Config"], [
    "How To Pay Monthly Rental"], ["Paid"]]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


# def inline_keyboard():
#     buttons = [[InlineKeyboardButton(text="Long Data",callback_data="ling"),
#                     InlineKeyboardButton(text="Short Data",callback_data="short"),]]

#     return InlineKeyboardMarkup(buttons)

buttons1 = [[InlineKeyboardButton(text="Login", callback_data="Login1"), InlineKeyboardButton(text="User", callback_data="user1"),
            InlineKeyboardButton(text="User + Mail", callback_data="Mail1"),
            InlineKeyboardButton(text="Pro", callback_data="pro1"), InlineKeyboardButton(text="All Data", callback_data="all1"),]]
inline1 = InlineKeyboardMarkup(buttons1)

buttons2 = [[InlineKeyboardButton(text="Login", callback_data="Login2"), InlineKeyboardButton(text="User", callback_data="user2"),
            InlineKeyboardButton(text="User + Mail", callback_data="Mail2"), InlineKeyboardButton(text="Pro", callback_data="pro2"),
            InlineKeyboardButton(text="All Data", callback_data="all2"),]]
inline2 = InlineKeyboardMarkup(buttons2)

buttons3 = [[InlineKeyboardButton(text="Login", callback_data="Login3"), InlineKeyboardButton(text="User", callback_data="user3"),
            InlineKeyboardButton(text="User + Mail", callback_data="Mail3"), InlineKeyboardButton(text="Pro", callback_data="pro3"),
            InlineKeyboardButton(text="Reserved", callback_data="Reserved"),]]
inline3 = InlineKeyboardMarkup(buttons3)


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
clientsheet = gspread.authorize(creds)
sheet = clientsheet.open("Smart Sheet").sheet1

usersearchlist = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.chat.username
    behnam_chatID = 7547338574
    users_chat_id = update.message.chat.id
    print(f'{username} Pressed Start Button')
    greeting = [f'👋 Hello @{username}\nWhat Are You Looking For?',
                f'Hi @{username}\nHow You Doing Today', f'Heeey @{username}\nLets Do This']
    index = random.randint(0, 2)
    await update.message.reply_text(text=greeting[index], reply_markup=markup, parse_mode="html")
    await bot.send_message(chat_id=behnam_chatID, text=f"Started Bot\n@{username}\n{users_chat_id}")
    if users_chat_id == behnam_chatID:
        await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')
    return tax


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.chat.username
    users_chat_id = update.message.chat.id

    behnam_chatID = 7547338574
    print(f'{username} Pressed Help Button')
    if users_chat_id == behnam_chatID:
        await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')
        return tax
    else:
        await update.message.reply_text("You dont have access to this section", reply_markup=markup, parse_mode="html")


async def taxID(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dict = {}
    username = update.message.chat.username
    text = update.message.text
    print(text)
    exceldata = sheet.get_all_records()
    users_chat_id = update.message.chat.id
    behnam_chatID = 7547338574
    transactoion_Status = ''
    # if 'Bep' in text:
    link = "https://bscscan.com/tx"
    taxID = text.rsplit('-', 1)[1]
    print(taxID)
    try:
        addressTrack = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={taxID}&apikey={binance_api}"
        status_check = f"https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash={taxID}&apikey={binance_api}"

        resp_adress = requests.post(addressTrack)
        result_address = json.loads(resp_adress.content)
        print(result_address)
        resp_status = requests.get(status_check)
        result_status = json.loads(resp_status.content)
        sender = str(result_address['result']['from'])
        reciever = str(result_address['result']['to'])
        transactionHash = str(result_address['result']['hash'])
        status_number = int(result_status['result']['status'])
        if status_number == 1:
            transactoion_Status = '✅ Payment Successful'
        if status_number == 0:
            transactoion_Status = '❌ Payment Failed'
        



        await bot.send_message(chat_id=behnam_chatID, text=f"From = {sender}\nTo = {reciever}\nStatus = {transactoion_Status}")
        await bot.send_message(chat_id=behnam_chatID, text=f"{link}/{transactionHash}", disable_web_page_preview=True)

        # for i in exceldata:
        #     dict.update(i)
        #     if transactionHash == str(dict['taxID']):
        #         await bot.send_message(chat_id=behnam_chatID, text="❌ This TaxID is Duplicate")
        #     else:
        #         await bot.send_message(chat_id=behnam_chatID, text="✅ This TaxID is Unique")





    except:
        await update.message.reply_text("❌ Wrong Transaction Hash\nSend It Again")

    if users_chat_id == behnam_chatID:
        await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')


async def userGmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    behnam_chatID = 7547338574
    users_chat_id = update.callback_query.from_user.id
    response = update.callback_query.data
    dict = {}
    exceldata = sheet.get_all_records()
    try:
        element = usersearchlist.pop(0)
    except:
        pass
    if users_chat_id == 7547338574:
        if response == "all2":
            for i in exceldata:
                dict.update(i)
                if element == dict['Renter Mail'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    allData(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{allData(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()



        if response == "pro2":
            for i in exceldata:
                dict.update(i)
                if element == dict['Renter Mail'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    userPRo(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userPRo(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()

        if response == "user2":
            for i in exceldata:
                dict.update(i)
                if element == dict['Renter Mail'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    userNormal(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userNormal(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()



        if response == "Mail2":
            for i in exceldata:
                dict.update(i)
                if element == dict['Renter Mail'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    userMAIL(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userMAIL(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()



        if response == "Login2":
            for i in exceldata:
                dict.update(i)
                if element == dict['Telegram User Name'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    try:
                        if dict['Owner Name'] != "":
                            ownerName = str(dict['Owner Name'])
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{ownerName}`", parse_mode="MarkDown")

                    except:
                        pass

                    try:
                        if dict['Mail'] != "":
                            mail = str(dict['Mail'])
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{mail}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork Pass'] != "":
                            upworkPAss = dict['Upwork Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkPAss}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork SecQ'] != "":
                            upworkSecQ = dict['Upwork SecQ']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkSecQ}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote IP'] != "":
                            remoteIP = dict['Remote IP']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteIP}`", parse_mode="MarkDown")

                    except:
                        pass

                    try:
                        if dict['Remote UserName'] != "":
                            remoteUserName = dict['Remote UserName']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteUserName}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote Pass'] != "":
                            remotePass = dict['Remote Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remotePass}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:    
                        if dict['anyDesk'] != "":
                            anyDeskAddress = dict['anyDesk']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskAddress}`", parse_mode="MarkDown")
                    except:
                        pass
                    
                    try:
                        if dict['anyDesk Password'] != "":
                            anyDeskPass = dict['anyDesk Password']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskPass}`", parse_mode="MarkDown")
                    except:
                        pass

        if users_chat_id == behnam_chatID:
            await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')


# Search For User By Telegram ID
async def userSearch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today_str = datetime.now().strftime('%d/%m/%Y')
    today_date = datetime.strptime(today_str, '%d/%m/%Y')
    username = update.message.chat.username
    behnam_chatID = 7547338574
    users_chat_id = update.message.chat.id
    dict = {}
    paidCOUNTER = 0
    notPAIDCOUNTER = 0
    counter = 0
    uaeCountry = 0
    ukCountry = 0
    canadaCountry = 0
    text = update.message.text

    await bot.send_message(chat_id=behnam_chatID, text=f"@{username}\n{users_chat_id}\nIs Looking For {text}", disable_web_page_preview=True)
    data = sheet.get_all_records()
    result = ""
    total_payment = 0

    if "Pay" in text:
        user_exist = False
        configli = ""
        file = "hash.jpg"
        photo_path = os.path.join(os.getcwd(), file)
        # photo_path = os.path.join("C:\\Users\\Behnam\\Desktop\\python for ever\\Elnaz Project\\hash.jpg")
        username = update.message.chat.username
        for i in data:
            dict.update(i)
            if users_chat_id == dict['Telegram userID']:
                try:
                    if dict['Account Region'] != "":
                        region = dict['Account Region']
                        configli += f"Account Region = {region}\n"

                        if dict['Mail'] != "":
                            mail = dict['Mail']
                            configli += f"Mail = {mail}\n"

                        try:
                            if dict['Price Amount'] != "":
                                priceAmount = int(dict['Price Amount'])
                                configli += f"Monthly Rental Price = {priceAmount}\n"
                        except:
                            pass

                        if dict['Wallet Address'] != "":
                            walletAddress = dict['Wallet Address']

                        await update.message.reply_text(text=f"<pre><code class='language-python'>{configli}</code></pre>", parse_mode='html')
                        user_exist = True
                        configli = ""
                        if users_chat_id == behnam_chatID:
                            await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')

                except:
                    pass

        if not user_exist:
            await update.message.reply_text(text="<pre><code class='language-python'>Your Telegram User Name Isn't In Our List</code></pre>", parse_mode="html")

        if user_exist == True:
            await update.message.reply_text(text="Tether USDT Bep20 (Binance) Wallet Adress ⬇️")
            await update.message.reply_text(text=f"`0x709b04943354ED44020cAd7340B11d7683A74239`", parse_mode="MarkDown")
            await update.message.reply_text(text="Tether USDT Trc20 (Tron) Wallet Adress ⬇️")
            await update.message.reply_text(text=f"`TSUM9gzPoBRkzNwcxKtgL3oDuQyJDbhgT4`", parse_mode="MarkDown")
            await update.message.reply_text(text="Tether USDT Erc20 (Ethereum) Wallet Adress ⬇️")
            await update.message.reply_text(text=f"`0xf4d13e70527265490e85d5ccc50331e14889b5f2`", parse_mode="MarkDown")
            await update.message.reply_text(text='Send Your Transaction Hash by\n⏺ /Paid button')
            await bot.send_photo(chat_id=users_chat_id, photo=open(photo_path, 'rb'), caption="Transaction Hash Sample")
        await update.message.reply_text(text="If You Have Any Question Contact Me @CreativePurple", reply_markup=markup)

    # Check if User Paid
    if "Paid" in text:
        behnam_chatID = 7547338574
        await update.message.reply_text(text="If you have paid your rental payment\nType your Transaction Hash", reply_markup=markup)
        if users_chat_id == behnam_chatID:
            await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')
        return tax

    # Show User Credentials
    if "Config" in text:
        behnam_chatID = 7547338574
        dict = {}
        user_exist = False
        text = update.message.text
        users_chat_id = update.message.chat.id
        # data = sheet.get_all_records()
        configList = ""
        for i in data:
            dict.update(i)
            if users_chat_id == dict['Telegram userID']:
                try:
                    if dict['Payment Start Date'] != "":
                        start = str(dict['Payment Start Date'])
                        end = str(dict['Payment Expire Date'])
                        date_format = "%d/%m/%Y"
                        endDATE = datetime.strptime(end, date_format)
                        date_difference = endDATE - today_date
                        days_difference = date_difference.days
                        paymentExpire = dict['Payment Expire Date']
                        if today_date >= endDATE:
                            configList += f"Subscription Started At {start}\n"
                            configList += f"Subscription Expired {days_difference} Days Before \n"
                        else:
                            configList += f"Next Monthly Rental Payment in {paymentExpire}\n"
                            configList += f"Subscription Remaining Days = {days_difference}\n"
                except:
                    pass

                if dict['Account Region'] != "":
                    upworkREGION = dict['Account Region']
                    configList += f"Upwork Account Region = {upworkREGION}\n"

                if dict['Discount'] != "":
                    discount = dict['Discount']
                    configList += f"Discount = {discount}\n"

                if dict['Price Amount'] != "":
                    priceAMOUNT = dict['Price Amount']
                    configList += f"Monthly Rental Price = {priceAMOUNT}\n"

                if dict['Mail'] != "":
                    mail = dict['Mail']
                    configList += f"Mail = {mail}\n"

                if dict['Upwork Pass'] != "":
                    upworkPASS = dict['Upwork Pass']
                    configList += f"Upwork Password = {upworkPASS}\n"

                if dict['Upwork SecQ'] != "":
                    upworkSecQ = dict['Upwork SecQ']
                    configList += f"Upwork Security Question = {upworkSecQ}\n"

                if dict['Payment Mail'] != "":
                    paymentMAIL = dict['Payment Mail']
                    result += f"{paymentMAIL}\n"

                if dict['Payment Pass'] != "":
                    paymentPass = dict['Payment Pass']
                    result += f"{paymentPass}\n"

                if dict['Birthday'] != "":
                    accountBirth = dict['Birthday']
                    configList += f"Birthday = {accountBirth}\n"

                if dict['Freelancer Mail'] != "":
                    freelancerMail = dict['Freelancer Mail']
                    configList += f"Freelancer Mail = {freelancerMail}\n"

                if dict['Freelancer Pass'] != "":
                    freelancerPass = dict['Freelancer Pass']
                    configList += f"Freelancer Pass = {freelancerPass}\n"

                if dict['Phone Number'] != "":
                    phoneNUMBER = dict['Phone Number']
                    configList += f"Phone Number = {phoneNUMBER}\n"

                if dict['Phone Website'] != "":
                    phoneWEBSITe = dict['Phone Website']
                    configList += f"Phone Website = {phoneWEBSITe}\n"

                if dict['Phone Mail'] != "":
                    phoneMail = dict['Phone Mail']
                    configList += f"Phone Login Mail Address = {phoneMail}\n"

                if dict['Phone Pass'] != "":
                    phonePassword = dict['Phone Pass']
                    configList += f"Phone Login Password = {phonePassword}\n"

                if dict['Remote IP'] != "":
                    remoteIP = dict['Remote IP']
                    configList += f"Remote Ip = {remoteIP}\n"

                if dict['Remote UserName'] != "":
                    remoteUserName = dict['Remote UserName']
                    configList += f"Remote User Name = {remoteUserName}\n"

                if dict['Remote Pass'] != "":
                    remotePass = dict['Remote Pass']
                    configList += f"Remote Password = {remotePass}\n"

                if dict['anyDesk'] != "":
                    anyDeskAddress = dict['anyDesk']
                    configList += f"AnyDesk Address = {anyDeskAddress}\n"

                if dict['anyDesk Password'] != "":
                    anyDeskPass = dict['anyDesk Password']
                    configList += f"AnyDesk Password = {anyDeskPass}\n"

                await update.message.reply_text(text=f"<pre><code class='language-python'>{configList}</code></pre>", parse_mode='html')
                configList = ""
                user_exist = True


        if not user_exist:
            await update.message.reply_text(text="<pre><code class='language-python'>Your Telegram User Name Isn't In Our List</code></pre>", parse_mode="html")

        if user_exist == True:
            await update.message.reply_text(text="""⚠️ Please Read Rules Carefully, if you do any mistakes i wont help you:\n\n1️⃣ Never Change Mail And Passwords\nUpwork will ask for visual verification again and i dont help you\n\n2️⃣ Only Use Account with the browser we provide and dont change it\n\n3️⃣ Dont Install Any Extensions on browser\n\n4️⃣ Only Use your Payment for Upwork and not personal usage and start earning with little amount of money\n\n5️⃣ Dont Use Fake Review (dont cheat Upwork cuz it will ban account)\n\n6️⃣ Dont ask money out of Upwork system\n\n7️⃣ Dont share your information with Upwork Client""")

    await update.message.reply_text(text="📥 Contact Me @CreativePurple", reply_markup=markup)

    if users_chat_id == 7547338574:
        if "Vps" in text:
            result = ""
            vpsStatus = False
            for i in data:
                dict.update(i)
                if dict['VPS Expire Date'] != "":
                    try:
                        end = str(dict['VPS Expire Date'])
                        date_format = "%d/%m/%Y"
                        endDATE = datetime.strptime(end, date_format)
                        date_difference = endDATE - today_date
                        days_difference = date_difference.days

                        if days_difference < 7:

                            if days_difference == 0:
                                result += f"TodaYYYY = {days_difference}\n"
                            if days_difference > 0:
                                result += f"Vps Remaining Days = {days_difference}\n"
                            if days_difference < 0:
                                result += f"Vps Expired {days_difference} Days Before \n"

                            if dict['Telegram User Name'] != "":
                                telegramUserName = dict['Telegram User Name']
                                result += f"{telegramUserName}\n"

                            if dict['Account Name'] != "":
                                accountName = dict['Account Name']
                                result += f"Account Name = {accountName}\n"

                            if dict['Mail'] != "":
                                mail = dict['Mail']
                                result += f"Upwork Mail = {mail}\n"

                            if dict['VPS Website'] != "":
                                vpsWebsite = dict['VPS Website']
                                result += f"VPS Website = {vpsWebsite}\n"

                            if dict['VPS Mail'] != "":
                                vpsMail = dict['VPS Mail']
                                result += f"Vps Mail Address = {vpsMail}\n"

                            if dict['VPS Mail Password'] != "":
                                vpsPass = dict['VPS Mail Password']
                                result += f"Vps Mail Password = {vpsPass}\n"

                            if dict['Remote IP'] != "":
                                remoteIP = dict['Remote IP']
                                result += f"Remote Ip = {remoteIP}\n"

                            if dict['Remote UserName'] != "":
                                remoteUserName = dict['Remote UserName']
                                result += f"Remote User Name = {remoteUserName}\n"

                            if dict['Remote Pass'] != "":
                                remotePass = dict['Remote Pass']
                                result += f"Remote Password = {remotePass}\n"

                            try:
                                await update.message.reply_text(text=f"{telegramUserName}", disable_web_page_preview=True)
                            except:
                                pass
                            await update.message.reply_text(text=f"<pre><code class='language-python'>{result}</code></pre>", parse_mode='html')
                            vpsStatus = True
                            result = ""
                    except:
                        pass
            if not vpsStatus:
                await update.message.reply_text(text='All VPS Are Paid !')

        if "Aa" in text:
            result = ""
            for i in data:
                dict.update(i)

                if dict['Status'] == "Verified" or dict['Status'] == "Upload":

                    if dict['Mail'] != "":
                        mail = dict['Mail']
                        await update.message.reply_text(text=f"`{mail}`", parse_mode="MarkDown")
                    else:
                        pass

                    try:
                        start = str(dict['Payment Start Date'])
                        end = str(dict['Payment Expire Date'])
                        date_format = "%d/%m/%Y"
                        endDATE = datetime.strptime(end, date_format)
                        date_difference = endDATE - today_date
                        days_difference = date_difference.days
                        result += f"Next Payment in {days_difference} Days\n"
                    except:
                        pass

                    if dict['Telegram Name'] != "":
                        telegramusername = dict['Telegram Name']
                        result += f"Renter Name = {telegramusername}\n"

                    if dict['Owner Name'] != "":
                        ownerName = dict['Owner Name']
                        result += f"Owner = {ownerName}\n"

                    if dict['Note'] != "":
                        note = dict['Note']
                        result += f"Note = {note}\n"

                    if dict['Status'] != "":
                        status = dict['Status']
                        if dict['Status'] == "Verified":
                            result += f"Status = ✅ {status}\n"

                        elif status == "Upload":
                            result += f"Status = 🛂 {status}\n"
                        else:
                            result += f"Status = {status}\n"

                    if dict['Remote IP'] != "":
                        remoteIP = dict['Remote IP']
                        result += f"Remote Ip = {remoteIP}\n"

                    if dict['Remote UserName'] != "":
                        remoteUserName = dict['Remote UserName']
                        result += f"Remote User Name = {remoteUserName}\n"

                    if dict['Remote Pass'] != "":
                        remotePass = dict['Remote Pass']
                        result += f"Remote Password = {remotePass}\n"

                    await update.message.reply_text(text=f"<pre><code class='language-python'>{result}</code></pre>", parse_mode='html', disable_web_page_preview=True)
                    result = ""


        if "Upload" in text:
            for i in data:
                dict.update(i)
                if dict['Status'] == "Upload":

                    try:
                        if dict['Owner Name'] != "":
                            ownerName = dict['Owner Name']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{ownerName}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Mail'] != "":
                            mail = str(dict['Mail'])
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{mail}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork Pass'] != "":
                            upworkPAss = dict['Upwork Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkPAss}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork SecQ'] != "":
                            upworkSecQ = dict['Upwork SecQ']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkSecQ}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote IP'] != "":
                            remoteIP = dict['Remote IP']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteIP}`", parse_mode="MarkDown")

                    except:
                        pass

                    try:
                        if dict['Remote UserName'] != "":
                            remoteUserName = dict['Remote UserName']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteUserName}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote Pass'] != "":
                            remotePass = dict['Remote Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remotePass}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:    
                        if dict['anyDesk'] != "":
                            anyDeskAddress = dict['anyDesk']
                            await bot.send_message(chat_id=behnam_chatID, text=anyDeskAddress, reply_markup=markup, parse_mode='html')
                    except:
                        pass
                    
                    try:
                        if dict['anyDesk Password'] != "":
                            anyDeskPass = dict['anyDesk Password']
                            await bot.send_message(chat_id=behnam_chatID, text=anyDeskPass, reply_markup=markup, parse_mode='html')
                    except:
                        pass
                            
                    await bot.send_message(chat_id=behnam_chatID, text="❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️", reply_markup=markup, parse_mode='html')

        # Show Analize of monthly report
        if "Az" in text:
            result = ""
            result_list = []
            total_payment = 0
            paidCOUNTER = 0
            notPAIDCOUNTER = 0
            uaeCountry = 0
            ukCountry = 0
            canadaCountry = 0

            for i in data:
                dict.update(i)
                if "Paid" == dict['Payment Status']:
                    if "Verified" == dict['Status']:
                        totalEarning = int(dict['Price Amount'])
                        total_payment += totalEarning
                        paidCOUNTER += 1

                        if "UAE" == dict['Account Region']:
                            uaeCountry += 1

                        if "UK" == dict['Account Region']:
                            ukCountry += 1

                        elif "Canada" == dict['Account Region']:
                            canadaCountry += 1

                    elif "Not Paid" == dict['Payment Status']:
                        notPAIDCOUNTER += 1
                    else:
                        pass

                if dict['Payment Status'] == 'Paid':
                    notestatus = False
                    if "Verified" == dict['Status']:
                        try:
                            start = str(dict['Payment Start Date'])
                            end = str(dict['Payment Expire Date'])
                            date_format = "%d/%m/%Y"
                            endDATE = datetime.strptime(end, date_format)
                            date_difference = endDATE - today_date
                            days_difference = date_difference.days
                            date_obj = datetime.strptime(end, "%d/%m/%Y")
                            day = date_obj.day
                            month = date_obj.month
                            year = date_obj.year
                            jalali_date = str(jdatetime.date.fromgregorian(day=day, month=month, year=year))
                            timeres += f'End time = {jalali_date}\n'
                            result += f"Next Payment in {days_difference} Days\n"
                        except:
                            pass

                        if dict['Price Amount'] != "":
                            priceAmount = int(dict['Price Amount'])
                            result += f"Price = {priceAmount}$\n"

                        if dict['Telegram Name'] != "":
                            telegramUser = dict["Telegram Name"]
                            result += telegramUser

                        if dict['Note'] != "":
                            notestatus = True
                            note = dict["Note"]
                            result += note
                        else:
                            note = ""

                        if notestatus:
                            result_list.append((jalali_date, telegramUser, priceAmount, note))
                        else:
                            result_list.append((jalali_date, telegramUser, priceAmount, ""))

            result_list.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
            result = "\n".join([f"{date} = {username} : {price}$" + (f" / {note}" if note else "") for date, username, price, note in result_list])

            await update.message.reply_text(text=f"<pre><code class='language-python'>Income = {total_payment}$\nUAE = {uaeCountry}\nUK = {ukCountry}\nCanada = {canadaCountry}\n{paidCOUNTER} Developers Paid\n{notPAIDCOUNTER} Developers Not Paid</code></pre>", parse_mode='html')
            await update.message.reply_text(text=f"<pre><code class='language-python'>{result}</code></pre>", parse_mode='html', disable_web_page_preview=True)
            result_list = []
            result_list.clear()


        
        # Show who not paid yet
        if "Nn" in text:
            for i in data:
                dict.update(i)
                if "Not Paid" == dict['Payment Status']:
                    counter += 1
                    mail = dict['Mail']
                    outlookPass = dict['Outlook Pass']
                    paymentExpire = dict['Payment Expire Date']
                    telegramUserName = dict['Telegram User Name']
                    total_payment = int(dict['Price Amount'])
                    end = str(dict['Payment Expire Date'])
                    date_format = "%d/%m/%Y"
                    endDATE = datetime.strptime(end, date_format)
                    date_difference = endDATE - today_date
                    days_difference = date_difference.days
                    result += f"Payment Expired Date = {paymentExpire}\nSubscription expired {days_difference} Days Before\nMail = {mail}\nOutlook Password ={outlookPass}\nRental Price = {total_payment}"
                    await update.message.reply_text(text=f"{telegramUserName}", disable_web_page_preview=True)
                    await update.message.reply_text(text=f"<pre><code class='language-python'>{result}</code></pre>", parse_mode='html')

                    result = ""
            await update.message.reply_text(text=f"<pre><code class='language-python'>There Are {counter} Developers Not Paid Yet</code></pre>", parse_mode='html')


        if "t.me" in text or "https://t.me/" in text:
            usersearchlist.append(text)
            await update.message.reply_text(text="Which Data Type Do You Want?", reply_markup=inline1)
            return userTelegram

        if "@" in text:
            usersearchlist.append(text)
            await update.message.reply_text(text="Which Data Type Do You Want?", reply_markup=inline2)
            return userGmail

        # Warning number 1 for those who not paid yet
        if "W1" in text:
            result = ""
            behnam_chatID = 7547338574
            usersIdList = []
            for i in data:
                dict.update(i)
                if "Not Paid" != dict['Payment Status']:
                    continue
                telegramUserId = dict['Telegram userID']
                usersIdList.append(telegramUserId)
                end = str(dict['Payment Expire Date'])
                date_format = "%d/%m/%Y"
                endDATE = datetime.strptime(end, date_format)
                date_difference = endDATE - today_date
                days_difference = date_difference.days
                telegramUserName = dict['Telegram UserName']
                telegramName = dict['Telegram Name']
                for chatid in usersIdList:
                    await bot.send_message(chat_id=chatid, text=f'👋 Hey {telegramName}\nHope You Are Doing Well\nYou Didnt Pay Your Rental Yet\nPlease Send it ASAP\nThanks')
                    usersIdList.clear()
                    result = ""
                    usersearchlist.append(telegramUserName)
                await bot.send_message(chat_id=behnam_chatID, text=telegramUserName, disable_web_page_preview=True, reply_markup=inline2)
                return freeOfUser

        # Warning number 2 for those who not paid yet
        if "W2" in text:
            behnam_chatID = 7547338574
            usersIdList = []
            for i in data:
                dict.update(i)
                if "Not Paid" != dict['Payment Status']:
                    continue
                telegramUserId = dict['Telegram userID']
                usersIdList.append(telegramUserId)
                end = str(dict['Payment Expire Date'])
                date_format = "%d/%m/%Y"
                endDATE = datetime.strptime(end, date_format)
                date_difference = endDATE - today_date
                days_difference = date_difference.days
                telegramUserName = dict['Telegram UserName']
                telegramName = dict['Telegram Name']
                for chatid in usersIdList:
                    await bot.send_message(chat_id=chatid, text=f'👋 Hey {telegramName}\n❗️ This Is Last Warningt\nIF You Dont Want To Lose Your Account Please Send Your Rental\nThanks')
                    usersIdList.clear()
                    result = ""
                    usersearchlist.append(telegramUserName)
                await bot.send_message(chat_id=behnam_chatID, text=telegramUserName, disable_web_page_preview=True, reply_markup=inline2)
                return freeOfUser

        # Send message to checkput latest channel post
        if "Ll" in text:
            usersIdList = []
            for i in data:
                dict.update(i)
                telegramUserId = dict['Telegram userID']
                usersIdList.append(telegramUserId)
            for i in usersIdList:
                try:
                    await bot.send_message(chat_id=i, text='👋 Hello Mate\nThere Is a New Post On Our Channel\n➡️ https://t.me/upworkrforrent')
                except:
                    pass
            usersIdList.clear()

        # Remind to Those Who should pay soon
        if "Rr" in text:
            usersIdList = []
            behnam_chatID = 7547338574
            result = ""
            for i in data:
                dict.update(i)
                try:
                    end = str(dict['Payment Expire Date'])
                    date_format = "%d/%m/%Y"
                    endDATE = datetime.strptime(end, date_format)
                    date_difference = endDATE - today_date
                    days_difference = date_difference.days
                    if days_difference < 7 or days_difference >= 0:
                        telegramUserName = dict['Telegram UserName']
                        telegramUserId = dict['Telegram userID']
                        usersIdList.append(telegramUserId)
                        for i in usersIdList:
                            await bot.send_message(chat_id=i, text=F'👋 Hello {telegramusername}\n\n⏰ This Is Reminder That Your Monthly Rental Is Getting Close\nRegards')
                            await bot.send_message(chat_id=behnam_chatID, text=f"Message Sent To Message {telegramUserName}", disable_web_page_preview=True)

                        usersIdList.clear()
                except:
                    pass

        # Account Ready To Rent with Short Data
        if "Ff" in text:
            await update.message.reply_text(text="Which Data Type Do You Want?", reply_markup=inline3)
            return freeOfUser

        if "Mm" in text:
            result = ""
            timeres = ""
            for i in data:
                dict.update(i)
                if dict['Telegram User Name'] != "":
                    if "Verified" == dict['Status']:
                        if dict['Payment Status'] == 'Paid' or dict['Payment Status'] == 'Not Paid':
                            try:
                                start = str(dict['Payment Start Date'])
                                end = str(dict['Payment Expire Date'])
                                date_format = "%d/%m/%Y"
                                endDATE = datetime.strptime(end, date_format)
                                date_difference = endDATE - today_date
                                days_difference = date_difference.days
                                date_obj = datetime.strptime(end, "%d/%m/%Y")
                                day = date_obj.day
                                month = date_obj.month
                                year = date_obj.year
                                jalali_date =str(jdatetime.date.fromgregorian (day = day, month = month, year = year))
                                timeres += f'End time = {end}\n'
                                timeres += f'End time Shamsi = {jalali_date}\n'
                                result += f"Next Payment in {days_difference} Days\n"

                            except:
                                pass

                            if dict['Telegram User Name'] != "":
                                username = dict['Telegram User Name']
                                result += f"{username}\n"

                            if dict['Telegram Name'] != "":
                                telegramname = dict['Telegram Name']
                                result += f"Telegram name = {telegramname}\n"

                            if dict['Owner Name'] != "":
                                ownerName = dict['Owner Name']
                                result += f"Owner = {ownerName}\n"

                            if dict['Note'] != "":
                                note = dict['Note']
                                result += f"Note = {note}\n"

                            if dict['Discount'] != "":
                                Discount = dict['Discount']
                                result += f"Discount = {Discount}\n"

                            if dict['Price Amount'] != "" and dict['Price Amount'] != "":
                                priceAmount = int(dict['Price Amount'])
                                result += f"Price = {priceAmount}$\n"
                        
                            # await update.message.reply_text(text=f'{timeres}{result}', disable_web_page_preview=True)
                            await update.message.reply_text(text=f"<pre><code class='language-python'>{timeres}{result}</code></pre>", parse_mode='html', disable_web_page_preview=True)
                            timeres = ""
                            result = ""

    if users_chat_id == behnam_chatID:
        await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')


async def freeOfUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    behnam_chatID = 7547338574
    users_chat_id = update.callback_query.from_user.id
    user_exist = False
    response = update.callback_query.data
    result = ""
    dict = {}
    data = sheet.get_all_records()

    if response == "Reserved":

        for i in data:
            dict.update(i)
            if dict['Note'] == "Reserved":

                telegram_userNAME = dict['Telegram User Name']

                if dict['Status'] != "":
                    status = dict['Status']
                    result += f"Status = {status}\n"

                if dict['Mail'] != "":
                    mail = dict['Mail']
                    result += f"Mail = {mail}\n"

                if dict['Upwork Pass'] != "":
                    upworkPASS = dict['Upwork Pass']
                    result += f"Upwork Pass = {upworkPASS}\n"

                if dict['Upwork SecQ'] != "":
                    upworkSECQ = dict['Upwork SecQ']
                    result += f"Upwork Security Question = {upworkSECQ}\n"

                if dict['Payment Pass'] != "":
                    paymentPass = dict['Payment Pass']
                    result += f"{paymentPass}\n"

                if dict['Freelancer Mail'] != "":
                    freelancerMail = dict['Freelancer Mail']
                    result += f"Freelancer Mail = {freelancerMail}\n"

                if dict['Freelancer Pass'] != "":
                    freelancerPass = dict['Freelancer Pass']
                    result += f"Freelancer Pass = {freelancerPass}\n"

                if dict['Phone Mail'] != "":
                    Phone = dict['Phone Mail']
                    result += f"Phone Mail = {Phone}\n"

                if dict['Phone Number'] != "":
                    phoneNUMBER = dict['Phone Number']
                    result += f"Phone Number = {phoneNUMBER}\n"

                if dict['Account Region'] != "":
                    upworkREGION = dict['Account Region']
                    result += f"Upwork Account Region = {upworkREGION}\n"

                if dict['Price Amount'] != "":
                    priceAMOUNT = dict['Price Amount']
                    result += f"Monthly Rental Price = {priceAMOUNT}\n"
                user_exist = True
                await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{result}</code></pre>", reply_markup=markup, parse_mode='html')
                result = ""

                try:
                    await bot.send_message(chat_id=behnam_chatID, text=f"{telegram_userNAME}")
                except:
                    pass

        if not user_exist:
            await update.message.reply_text(text="<pre><code class='language-python'>Make New One Bruh !</code></pre>", parse_mode="html")

    if response == "pro3":
        for i in data:
            dict.update(i)
            if dict['Telegram User Name'] == '' and dict['Mail'] != "":
                element = dict['Mail']
                userPRo(element)
                await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userPRo(element)}</code></pre>", reply_markup=markup, parse_mode='html')
                result = ""

    if response == "user3":

        for i in data:
            dict.update(i)
            if dict['Telegram User Name'] == '' and dict['Mail'] != "":
                element = dict['Mail']
                print(element)
                userNormal(element)
                await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userNormal(element)}</code></pre>", reply_markup=markup, parse_mode='html')
                result = ""
                usersearchlist.clear()

    if response == "Mail3":
        for i in data:
            dict.update(i)
            if dict['Telegram User Name'] == '' and dict['Mail'] != "":
                element = dict['Mail']
                userMAIL(element)
                await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userMAIL(element)}</code></pre>", reply_markup=markup, parse_mode='html')
                result = ""

    if response == "Login3":
        for i in data:
            dict.update(i)
            if element == dict['Telegram User Name'] or element == dict['Mail'] or element == dict['Telegram UserName']:

                try:
                    if dict['Owner Name'] != "":
                        ownerName = str(dict['Owner Name'])
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{ownerName}`", parse_mode="MarkDown")

                except:
                    pass

                try:
                    if dict['Mail'] != "":
                        mail = str(dict['Mail'])
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{mail}`", parse_mode="MarkDown")
                except:
                    pass

                try:
                    if dict['Upwork Pass'] != "":
                        upworkPAss = dict['Upwork Pass']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkPAss}`", parse_mode="MarkDown")
                except:
                    pass

                try:
                    if dict['Upwork SecQ'] != "":
                        upworkSecQ = dict['Upwork SecQ']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkSecQ}`", parse_mode="MarkDown")
                except:
                    pass

                try:
                    if dict['Remote IP'] != "":
                        remoteIP = dict['Remote IP']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteIP}`", parse_mode="MarkDown")

                except:
                    pass

                try:
                    if dict['Remote UserName'] != "":
                        remoteUserName = dict['Remote UserName']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteUserName}`", parse_mode="MarkDown")
                except:
                    pass

                try:
                    if dict['Remote Pass'] != "":
                        remotePass = dict['Remote Pass']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{remotePass}`", parse_mode="MarkDown")
                except:
                    pass

                try:    
                    if dict['anyDesk'] != "":
                        anyDeskAddress = dict['anyDesk']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskAddress}`", parse_mode="MarkDown")
                except:
                    pass
                
                try:
                    if dict['anyDesk Password'] != "":
                        anyDeskPass = dict['anyDesk Password']
                        await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskPass}`", parse_mode="MarkDown")
                except:
                    pass

async def userTelegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    behnam_chatID = 7547338574
    users_chat_id = update.callback_query.from_user.id
    response = update.callback_query.data
    result = ""
    dict = {}
    data = sheet.get_all_records()
    element = usersearchlist.pop(0)
    if users_chat_id == 7547338574:
        if response == "all1":
            for i in data:
                dict.update(i)
                if element == dict['Telegram User Name']:
                    allData(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{allData(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()

        if response == "pro1":
            for i in data:
                dict.update(i)
                if element == dict['Telegram User Name']:
                    userPRo(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userPRo(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()

        if response == "user1":

            for i in data:
                dict.update(i)

                if element == dict['Telegram User Name']:
                    userNormal(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userNormal(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()


        if response == "Mail1":
            for i in data:
                dict.update(i)
                if element == dict['Telegram User Name']:
                    userMAIL(element)
            await bot.send_message(chat_id=behnam_chatID, text=f"<pre><code class='language-python'>{userMAIL(element)}</code></pre>", reply_markup=markup, parse_mode='html')
            result = ""
            usersearchlist.clear()
                    

        if response == "Login1":
            for i in data:
                dict.update(i)
                if element == dict['Telegram User Name'] or element == dict['Mail'] or element == dict['Telegram UserName']:
                    try:
                        if dict['Owner Name'] != "":
                            ownerName = str(dict['Owner Name'])
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{ownerName}`", parse_mode="MarkDown")

                    except:
                        pass

                    try:
                        if dict['Mail'] != "":
                            mail = str(dict['Mail'])
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{mail}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork Pass'] != "":
                            upworkPAss = dict['Upwork Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkPAss}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Upwork SecQ'] != "":
                            upworkSecQ = dict['Upwork SecQ']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{upworkSecQ}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote IP'] != "":
                            remoteIP = dict['Remote IP']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteIP}`", parse_mode="MarkDown")

                    except:
                        pass

                    try:
                        if dict['Remote UserName'] != "":
                            remoteUserName = dict['Remote UserName']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remoteUserName}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:
                        if dict['Remote Pass'] != "":
                            remotePass = dict['Remote Pass']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{remotePass}`", parse_mode="MarkDown")
                    except:
                        pass

                    try:    
                        if dict['anyDesk'] != "":
                            anyDeskAddress = dict['anyDesk']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskAddress}`", parse_mode="MarkDown")
                    except:
                        pass
                    
                    try:
                        if dict['anyDesk Password'] != "":
                            anyDeskPass = dict['anyDesk Password']
                            await bot.send_message(chat_id=behnam_chatID, text=f"`{anyDeskPass}`", parse_mode="MarkDown")
                    except:
                        pass

        if users_chat_id == behnam_chatID:
            await bot.send_message(chat_id=behnam_chatID, text="/Aa : All Users\n/Mm : Money!\n/Az : Analyze Users\n/Vps : Vps Expire\n/Nn : Accounts doesnt Pay\n/Ff : Show Accounts are ready to rent\n/Rr : Remind to those who should pay\n/Ll : Send message to check channel\n/W1 : Reminder to those not paid\n/W2 : Reminder to those not paid so BAD\n/Upload : Do Verification", parse_mode='html')


def main():
    application = Application.builder().token("7276392721:AAFHezJjyCMSY51Y7zr-TLvbAVlgRBK217Y").build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            'tax': [MessageHandler(filters.Regex("^0x|Bep|Trc|Tax"), taxID)],
            'userSearch': [MessageHandler(filters.Regex("https://t.me/|t.me/|@|Nn|W1|W2|Ll|Rr|Aa|Az|Pay|Paid|Config|Fv|Ff|Cc|Mm|Vps|Upload"), userSearch)],
            'userGmail': [CallbackQueryHandler(userGmail, pattern='all2|pro2|user2|Mail2|Login2')],
            'userTelegram': [CallbackQueryHandler(userTelegram, pattern='all1|pro1|user1|Mail1|Login1')],
            'freeOfUser': [CallbackQueryHandler(freeOfUser, pattern='Reserved|pro3|user3|Mail3|Login3')],
            # Add any other states and their handlers here
        },
        fallbacks=[MessageHandler(filters.Regex("https://t.me/|t.me/|@|Nn|W1|W2|Ll|Rr|Aa|Az|Pay|Paid|Config|Fv|Ff|Cc|Mm|Vps|Upload"), userSearch)]
    )
    
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("help", help)],
        states={},
        fallbacks=[MessageHandler(filters.Regex("help"), help)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(CallbackQueryHandler(userTelegram, pattern='all1|pro1|user1|Mail1|Login1', block=False))
    application.add_handler(CallbackQueryHandler(userGmail, pattern='all2|pro2|user2|Mail2|Login2', block=False))
    application.add_handler(CallbackQueryHandler(freeOfUser, pattern='Reserved|pro3|user3|Mail3|Login3', block=False))
    
    application.run_polling()

if __name__ == '__main__':
    main()


# transaction check
# for i in exceldata:
#     dict.update(i)
            # walletAddress = str(dict['Wallet Address'])
            # customerAddress1 = str(dict['Customer Wallet Address 1'])
            # customerAddress2 = str(dict['Customer Wallet Address 2'])
            # link = "https://bscscan.com/tx"
            # timestamp = get_transaction_timestamp(transactionHash)
            # print(timestamp)

            # if sender.lower() == customerAddress1.lower() or sender.lower() == customerAddress2.lower():
            #     if reciever.lower() == walletAddress.lower():
            #         await update.message.reply_text("✅ Thanks For Your Payment")
            #     else:
            #         await update.message.reply_text("You Didnt Pay To Our Wallet Address\nSend Your Payment To The Wallet Address Below\nAnd Try Again")
            #         await update.message.reply_text(text=f"`{walletAddress}`", reply_markup=markup, parse_mode="MarkDown")
            # else:
            #     pass
            #     await update.message.reply_text("Your Wallet Address Doesn't Match To Your Profile")
            #     await update.message.reply_text(text="📥 Contact Me @CreativePurple", reply_markup=markup)
