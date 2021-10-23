from tkinter import *
from PIL import Image, ImageTk
import convert_numbers
import random
from random import randint
from Shetab.shetab import validate_data
from PaymentGate.BanksNumberAndLogo import banks_number_to_logo
from captcha.captcha import captcha
import datetime

# defining captcha and bank logo and sec variables for using in main and changing them in some functions
captcha_image, label_captcha, captcha_var, bank_logo_image = [None for _ in range(4)]
sec = 15 * 60


def main(pay_amount):
    print('Your payment gate is up...')
    # create a window
    root = Tk()
    root.geometry('1080x700+200-50')
    root.resizable(width=0, height=0)
    root.configure(bg='#0098db')
    root.iconbitmap(r'PaymentGate/Assets/appicon.ico')
    root.title('درگاه پرداخت اینترنتی بانک مکتب شریف')

    # bank logo image
    logo_img_file = Image.open('PaymentGate/Assets/logov2.jpg')
    logo_img = ImageTk.PhotoImage(logo_img_file)

    # shaparak logo image
    shaparak_img_file = Image.open('PaymentGate/Assets/shaparak.png')
    shaparak_img = ImageTk.PhotoImage(shaparak_img_file)

    # top canvas
    canvas1 = Canvas(root, bd=0, bg='#0098db', height=150, width=1080, highlightthickness=2,
                     highlightbackground="white")
    canvas1.pack(fill='both', expand=True)

    # set position of logos
    canvas1.create_image(70, 28, anchor='nw', image=logo_img)
    canvas1.create_image(890, 30, anchor='nw', image=shaparak_img)

    # label of app
    label_dravaze_pardakht = Label(root, text='دروازه پـــرداخت ایـنتـرنتـی بـانک مـکتـب شـریـف ',
                                   font=('Sakkal Majalla', 30, 'bold'), bg='#0098db', fg='white')
    canvas1.create_window(280, 85, anchor='nw', window=label_dravaze_pardakht)

    # second canvas | time & money amount
    bg_info = '#b5e3f8'
    canvas2 = Canvas(root, bd=0, bg=bg_info, height=55, width=1080, highlightthickness=2, highlightbackground="white")
    canvas2.pack()

    # En to Fa function
    def entofa(text, farsi_check=True, punc=' '):
        if farsi_check:
            text = text.split(punc)
            for j in range(len(text)):
                text[j] = convert_numbers.english_to_persian(text[j])
            return punc.join(text)
        return text

    # timer function

    def countdown():
        global sec
        mins, secs = divmod(sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        zamane_baghimande_e['text'] = entofa(timeformat, punc=':')
        sec -= 1
        # Take advantage of the after method of the Label
        zamane_baghimande_e.after(1000, countdown)

    class EntryCard(Entry):
        banks = banks_number_to_logo
        bank_name_label = []

        def __init__(self, master=None, max_len=4, entry_index=None, font=('Far.Traffic', 15, 'bold'), init_text='',
                     farsi=True, **kwargs):
            self.var = StringVar()
            self.max_len = max_len
            self.entry_index = entry_index
            self.init_text = init_text
            self.farsi = farsi
            Entry.__init__(self, master, textvariable=self.var, **kwargs)
            self.insert(0, init_text)
            self.config(fg='#74c7ec', font=font, bg='white', justify='center', highlightthickness=1)
            self.old_value = ''
            self.var.trace('w', self.check)

        def check(self, *args):
            self.config(fg='#0c3445')
            # card_entry_1_2 is first six number of bank card
            card_entry_1_2 = f"{entries['.!entrycard'].get() + entries['.!entrycard2'].get()}"[:6]

            # check if len of card1 and card2 is equal to 6 to show bank name
            if card_entry_1_2 in self.banks:
                global bank_logo_image
                bank_logo_image = PhotoImage(file=self.banks[card_entry_1_2])
                label = Label(root, image=bank_logo_image, borderwidth=0)
                EntryCard.bank_name_label.append(label)
                canvas3.create_window(410, 75, window=label)
            else:
                try:
                    for label in EntryCard.bank_name_label:
                        label.destroy()
                    EntryCard.bank_name_label = []
                except IndexError:
                    pass

            if len(self.get()) <= self.max_len:
                self.old_value = entofa(self.get())  # accept change
                self.old_value = entofa(self.get(), farsi_check=self.farsi)

                if len(self.get()) == self.max_len:
                    if self.entry_index != 10:
                        tab()
            else:
                self.var.set(entofa(self.old_value, farsi_check=self.farsi))  # reject change

    # event func for delete month and year default text
    def delete_year_month_text(event):
        if event.widget.init_text == event.widget.get():
            event.widget.delete(0, END)

    # name pazirande name
    name_pazirande_l = Label(root, text=':' + 'نام پذیرنده', font=('A Iranian Sans', 11), bg=bg_info, fg='black')
    name_pazirande_e = Label(root, text='مکتب شریف', font=('A Iranian Sans', 12, 'bold'), bg=bg_info, fg='#155e7e')

    # mablaghe pardakhti
    # mablagh must pass by previous step
    price = entofa(format(pay_amount, ','), punc=',')

    mablaghe_pardakhti_l = Label(root, text=':' + 'مبلغ پرداختی (ریال)', font=('A Iranian Sans', 11),
                                 bg=bg_info, fg='black')
    mablaghe_pardakhti_e = Label(root, text=price, font=('A Iranian Sans', 12, 'bold'), bg=bg_info, fg='#155e7e')

    # remaining time
    zamane_baghimande_l = Label(root, text=':' + 'زمان باقیمانده', font=('A Iranian Sans', 11), bg=bg_info, fg='black')
    zamane_baghimande_e = Label(root, text='0:0', font=('A Iranian Sans', 14, 'bold'), bg=bg_info, fg='#155e7e')

    # start timer
    countdown()

    # put infos in window
    canvas2.create_window(950, 15, anchor='nw', window=name_pazirande_l)
    canvas2.create_window(840, 15, anchor='nw', window=name_pazirande_e)
    canvas2.create_window(560, 15, anchor='nw', window=mablaghe_pardakhti_l)
    canvas2.create_window(550 - len(price) * 10, 15, anchor='nw', window=mablaghe_pardakhti_e)
    canvas2.create_window(170, 15, anchor='nw', window=zamane_baghimande_l)
    canvas2.create_window(100, 13, anchor='nw', window=zamane_baghimande_e)

    # canvas 3 - card info
    color_bg = '#eaf6f8'
    color_fg = '#0c3445'
    canvas3 = Canvas(root, bd=0, bg=color_bg, height=425, width=1080, highlightthickness=2, highlightbackground="white")
    canvas3.pack()

    # card infos frame
    card_frame = Frame(canvas3, bg=color_bg)
    canvas3.create_window(1000, 220, window=card_frame)

    # card infos
    label_card = Label(card_frame, text='شماره کارت', font=('A Iranian Sans', 14), bg=color_bg, fg=color_fg)
    label_pass = Label(card_frame, text='رمز دوم', font=('A Iranian Sans', 14), bg=color_bg, fg=color_fg)
    label_cvv = Label(card_frame, text='CVV2', font=('Cambria', 14), bg=color_bg, fg=color_fg)
    label_exp = Label(card_frame, text='تاريخ انقضا', font=('A Iranian Sans', 14), bg=color_bg, fg=color_fg)
    label_safe = Label(card_frame, text='عبارت امنيتي', font=('A Iranian Sans', 14), bg=color_bg, fg=color_fg)
    label_email = Label(card_frame, text='ایمیل (اختیاری)', font=('A Iranian Sans', 14), bg=color_bg, fg=color_fg)
    label_stars = [Label(root, text='*', font=('Arial', 15), bg=color_bg, fg='red') for _ in range(5)]

    # put infos in window
    label_card.grid(row=0, column=1, pady=18, sticky='e')
    label_pass.grid(row=1, column=1, pady=18, sticky='e')
    label_cvv.grid(row=2, column=1, pady=18, sticky='e')
    label_exp.grid(row=3, column=1, pady=10, sticky='e')
    label_safe.grid(row=4, column=1, pady=18, sticky='e')
    label_email.grid(row=5, column=1, pady=15, sticky='e')

    # label_stars[0].grid(row=0, column=0, pady=15, sticky='e')
    # label_stars[1].grid(row=1, column=0, pady=15, sticky='e')
    # label_stars[2].grid(row=2, column=0, pady=15, sticky='e')
    # label_stars[3].grid(row=3, column=0, pady=15, sticky='e')
    # label_stars[4].grid(row=4, column=0, pady=15, sticky='e')
    canvas3.create_window(955, 70, window=label_stars[0])
    canvas3.create_window(990, 135, window=label_stars[1])
    canvas3.create_window(1015, 195, window=label_stars[2])
    canvas3.create_window(965, 250, window=label_stars[3])
    canvas3.create_window(950, 310, window=label_stars[4])

    # card info entry boxes
    entry_card1 = EntryCard(root, max_len=4, width=15, entry_index=1)
    entry_card2 = EntryCard(root, max_len=4, width=15, entry_index=2)
    entry_card3 = EntryCard(root, max_len=4, width=15, entry_index=3)
    entry_card4 = EntryCard(root, max_len=4, width=15, entry_index=4)
    entry_pass = EntryCard(root, max_len=7, width=26, entry_index=5, show='•')
    entry_cvv = EntryCard(root, width=26, entry_index=6, show='•')
    entry_exp_m = EntryCard(root, max_len=2, width=10, entry_index=7, init_text='ماه')
    entry_exp_y = EntryCard(root, max_len=2, width=10, entry_index=8, init_text='سال')
    entry_captcha = EntryCard(root, max_len=5, font=('Samim', 17, 'bold'),
                              width=11, entry_index=9, farsi=False)
    entry_email = EntryCard(root, max_len=50, width=30, entry_index=10, font=('Samim', 17, 'bold'))

    # delete month and year entries if they get selected
    for entry in [entry_exp_y, entry_exp_m]:
        entry.bind("<Button-1>", delete_year_month_text)
        entry.bind("<FocusIn>", delete_year_month_text)

    # slash label for separating exp month and year
    slash_label = Label(root, text='/', font=('Arial', 25), bg=color_bg, fg="#0279ad")

    # set cursor to first entry
    entry_card1.focus_set()

    # create captcha label

    def update_captcha():
        global captcha_image, label_captcha, captcha_var

        entry_captcha.delete(0, END)
        text_img = captcha(color_bg)
        captcha_image = ImageTk.PhotoImage(text_img[0].rotate(randint(-3, 3), fillcolor=color_bg, expand=True))
        label_captcha = Label(root, image=captcha_image, bg=color_bg)
        canvas3.create_window(575, 290, anchor='nw', window=label_captcha)
        captcha_var = text_img[-1]

    # call change func for set captcha for first time
    update_captcha()

    # create captcha image change button
    arrow_image = ImageTk.PhotoImage(Image.open('PaymentGate/Assets/new_arrow.png'))
    button_captcha = Button(root, width=30, image=arrow_image, borderwidth=0, bg=color_bg, activebackground=color_bg,
                            command=update_captcha)

    # list of entries
    entries_list = [entry_card1, entry_card2, entry_card3, entry_card4,
                    entry_pass, entry_cvv, entry_exp_m, entry_exp_y,
                    entry_captcha, entry_email]

    # set entries border color
    for entry in entries_list:
        entry.config(highlightbackground="#0098db", highlightcolor="green")

    # dict of entries
    entries = {'.!entrycard': entry_card1}
    for i in range(1, 10):
        entries[f'.!entrycard' + str(i + 1)] = entries_list[i]

    # put card infos in window
    canvas3.create_window(800, 55, anchor='nw', window=entry_card4)
    canvas3.create_window(691, 55, anchor='nw', window=entry_card3)
    canvas3.create_window(581, 55, anchor='nw', window=entry_card2)
    canvas3.create_window(471, 55, anchor='nw', window=entry_card1)
    canvas3.create_window(735, 115, anchor='nw', window=entry_pass)
    canvas3.create_window(735, 175, anchor='nw', window=entry_cvv)
    canvas3.create_window(830, 235, anchor='nw', window=entry_exp_m)
    canvas3.create_window(807, 235, anchor='nw', window=slash_label)
    canvas3.create_window(735, 235, anchor='nw', window=entry_exp_y)
    # canvas3.create_window(740, 295, anchor='nw', window=captcha_canvas)
    canvas3.create_window(735, 295, anchor='nw', window=entry_captcha)
    canvas3.create_window(540, 295, anchor='nw', window=button_captcha)
    canvas3.create_window(469, 355, anchor='nw', window=entry_email)

    # virtual numpad
    numpad = Frame(root, bg='#0098db')
    canvas3.create_window(130, 100, anchor='nw', window=numpad)
    butt_bg = '#619fbb'
    numpad_label = Label(numpad, text='صفحه کلید ایمن', width=21, height=2, font=('A Iranian Sans', 12), bg='#92c1d6')

    # write in entries function
    def write(num):
        try:
            if errors_list:
                errors_list[-1].destroy()
            current_entry = entries[str(root.focus_get())]
            if len(current_entry.get()) == current_entry.max_len:
                current_entry.delete(0, END)
            current_entry.insert(current_entry.index(INSERT), num)
        except KeyError:
            update_captcha()
            pop_up('لطفا یکی از ورودی ها را انتخاب کنید')

    # delete entries text
    def delete():
        current_entry = entries[str(root.focus_get())]
        current_entry.delete(current_entry.index(INSERT) - 1)

    # tab in entries
    def tab():
        current_entry = str(root.focus_get())
        entries_keys = list(entries.keys())
        if entries_keys.index(current_entry) == len(entries_keys) - 1:
            entries[entries_keys[0]].focus_set()
            entries[entries_keys[0]].select_range(0, END)
        else:
            index = entries_keys.index(current_entry)
            entries[entries_keys[index + 1]].focus_set()
            entries[entries_keys[index + 1]].select_range(0, END)

    # buttons
    numpad_buttons = [
        Button(numpad, text=entofa(str(i)), font=('A Iranian Sans', 12), width=5, height=1, bg=butt_bg, bd=5,
               command=lambda k=i: write(k)) for i in range(10)]

    button_back = Button(numpad, text='Back', font=('A Iranian Sans', 12), width=5, height=1, bg=butt_bg, bd=5,
                         command=delete)
    button_tab = Button(numpad, text='Tab', font=('A Iranian Sans', 12), width=5, height=1, bg=butt_bg, bd=5,
                        command=tab)

    numpad_buttons += [button_back, button_tab]

    # config buttons color in clicked mode
    for button in numpad_buttons:
        button.config(activebackground='#5db5dd')

    # random places for numpad buttons
    tuples_list = []
    while len(tuples_list) != 9:
        my_tuple = (random.randint(1, 3), random.randint(0, 2))
        if my_tuple not in tuples_list:
            tuples_list.append(my_tuple)

    # placing buttons
    for i in range(9):
        numpad_buttons[i + 1].grid(row=tuples_list[i][0], column=tuples_list[i][1], sticky='nesw')
    numpad_buttons[10].grid(row=4, column=0, sticky='nesw')
    numpad_buttons[11].grid(row=4, column=1, sticky='nesw')
    numpad_buttons[0].grid(row=4, column=2, sticky='nesw')
    numpad_label.grid(row=5, column=0, columnspan=3, sticky='nesw')

    # error pop-up message
    # errors lists
    errors_list = []

    # error generator
    def pop_up(text, color='red'):
        text_len = len(text)
        label = Label(root, text=text, bg=color, fg=color_bg, font=('A Iranian Sans', 15))
        canvas3.create_window(753 - text_len, 35, window=label)
        errors_list.append(label)

    # canvas 4 | confirm & clear button
    canvas4 = Canvas(root, bd=0, bg=bg_info, height=70, width=1080, highlightthickness=2, highlightbackground="white")
    canvas4.pack()

    # confirm function for get all entries
    def confirm():
        card_data = {}
        if errors_list:
            for error in errors_list:
                error.destroy()
        for entry_ in entries:
            temp = entries[entry_].get()
            if len(temp) == 0 and entry_ != '.!entrycard10':
                update_captcha()
                return pop_up('ورودی ها نمیتوانند خالی باشند')
            else:
                card_data[entry_] = entries[entry_].get()
        if captcha_var.lower() != card_data['.!entrycard9'].lower():
            update_captcha()
            return pop_up('عبارت امنیتی وارد شده صحیح نمیباشد')
        pay_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        card_data['date-time'] = pay_time
        result = validate_data(card_data, pay_amount)  # call shetab database for checking data
        update_captcha()
        return pop_up(result[0], result[1])

    # Confirm and cancel button
    button_confirm = Button(root, text='پرداخت', font=('A Iranian Sans', 15), width=20, height=1, bg='#3ca817',
                            fg='white', cursor="hand2",
                            command=confirm, activebackground='#1b8012', activeforeground='white')
    button_cancel = Button(root, text='انصراف', font=('A Iranian Sans', 15), width=20, height=1, bg='#db1c1c',
                           fg='white', cursor="hand2",
                           command=lambda: root.destroy(), activebackground='#7e1c1c', activeforeground='white')

    canvas4.create_window(660, 30, window=button_confirm)
    canvas4.create_window(420, 30, window=button_cancel)
    root.mainloop()


if __name__ == '__main__':
    main(20000)
