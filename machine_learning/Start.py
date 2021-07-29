import tkinter
import Get_Account
from multiprocessing import Process
def main():
    def nowload():
        if (not startpage_info.get().isdigit) or (not endpage_info.get().isdigit()):
            msg.insert(tkinter.END,"请输入正确的页号")
            show_text_label.config(text='获取失败', fg='black', width=10, height=2)
            return
        show_text_label.config(text='正在获取账号信息', fg='black', width=20, height=2)
        work_process = Process(target = Get_Account.startload,args = (startpage_info.get(),endpage_info.get()))
        work_process.start()
        work_process.join()
        show_text_label.config(text='获取成功', fg='black', width=10, height=2)

    top = tkinter.Tk()
    top.title = '率土之滨账号获取'
    top.geometry('400x300')

    show_text_label = tkinter.Label(top, text='', fg='white', width=10, height=2)
    show_text_label.pack(side=tkinter.BOTTOM)

    # 输入起始页面
    startpage_Frame = tkinter.Frame(top)
    startpage_text = tkinter.Label(startpage_Frame, text='请输入要获取的起始页面', width=40, height=2)
    startpage_text.pack()
    startpage_info = tkinter.StringVar()
    startpage_entry = tkinter.Entry(startpage_Frame, textvariable=startpage_info)
    startpage_entry.pack()
    startpage_Frame.pack()
    # 输入中止页面
    endpage_Frame = tkinter.Frame(top)
    endpage_text = tkinter.Label(endpage_Frame, text='请输入要获取的终止页面', width=40, height=2)
    endpage_text.pack()
    endpage_info = tkinter.StringVar()
    endpage_entry = tkinter.Entry(endpage_Frame, textvariable=endpage_info)
    endpage_entry.pack()
    endpage_Frame.pack()
    msg = tkinter.Text(top)
    workbutton = tkinter.Button(top, text='点击获取起始页面到中止页面的账号信息', command=nowload)
    workbutton.pack()
    msg.pack()
    top.mainloop()

if __name__ == "__main__":
    main()
