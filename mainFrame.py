import time, tkinter as tk, import_structure as s_B, convert_time as ct


class mainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=None)

        # csvからラウンドの情報取得プロパティ
        self.round = 1
        self.list_str = s_B.StructureBB()
        self.round_str = self.list_str.output(self.round)
        self.next_round_str = self.list_str.output(self.round + 1)
        self.max_round = self.list_str.ALLround()
        # instance.output(0) = "play" or "rest",(1) = ANTE,(2) = BB,(3) = SB,(4) = min

        # アンティプロパティ
        self.ante = self.round_str[1]
        self.next_ante = self.next_round_str[1]

        # ラウンド管理プロパティ
        self.next_round_flag = False  # 次のラウンドへの移行フラグ
        self.all_finish = False

        # タイマー関連プロパティ
        self.started = False  # カウンドダウン進行中フラグ
        self.start_time = 0
        self.all_start = False  # カウントアップ進行中フラグ
        self.all_start_time = 0
        self.all_time = 0
        self.round_time = self.round_str[4]
        self.now_rest_time = 0
        self.elapsed_time = 0

        self.player = 5

        # 画面レイアウト
        # 上段フレーム
        fr1 = tk.Frame(master, relief="ridge", padx=5, pady=5, bd=5)
        fr1.pack(anchor="n", fill="both", padx=10, pady=10, expand=True)

        # 下段フレーム
        fr2 = tk.Frame(master)
        fr2.pack()
        #下段フレーム左(Blind)
        fr2L = tk.Frame(fr2, relief = "ridge", bd =5, padx=5, pady=5)
        fr2L.pack(side= "left", fill="both", padx=10, pady=10, expand=True)
        #下段フレーム右(player)
        fr2R = tk.Frame(fr2)
        fr2R.pack(side = "right")

        #Blind widget
        self.BB_SB_lb = (tk.Label(fr2L, font=('Helvetica', '80'),
                                  text="{0} / {1}".format(self.round_str[2],
                                                          self.round_str[3])
                                  ))
        self.BB_SB_lb.pack(expand=True, fill="both")

        self.ante_lb = tk.Label(fr2L,
                                font=("Helvetica", "50"),
                                text="({0})".format(self.round_str[1]))
        self.ante_lb.pack()

        self.next_BB_SB_lb = tk.Label(fr2L,
                                      font=("Helvetica", "30"),
                                      text="next [{0} / {1}] : ({2})".format(self.next_round_str[2],
                                                                             self.next_round_str[3],
                                                                             self.next_round_str[1]))
        self.next_BB_SB_lb.pack(anchor="se")


        # プレイヤー人数フレーム
        player_frame = tk.Frame(fr2R, relief="ridge", padx=5, pady=5, bd=5)
        player_frame.pack(padx=100, pady=20)
        self.player_lb = tk.Label(player_frame, text="{:0=02}人".format(self.player), font=("Helvetica", "80"))
        self.player_lb.pack(fill="both")

        # タイマーフレーム
        time_frame = tk.Frame(fr1)
        time_frame.pack(fill="both")
        self.countdown_lb = tk.Label(time_frame, text=ct.Time_converter(self.round_str[4]).MS,
                                     font=("Helvetica", "150"))
        self.countdown_lb.pack(expand=True, fill="both")
        self.total_time_lb = tk.Label(time_frame, text="経過時間  [00:00:00]", font=("Helvetica", "10"))
        self.total_time_lb.pack(fill="both")

        # コントローラーフレーム
        fr3 = tk.Frame(fr2R)
        fr3.pack(side="right")
        self.start_bt = tk.Button(fr3, text="Start", width=10, height=2, command=self.start_switch)
        self.reset_bt = tk.Button(fr3, text="round reset", width=10, height=2, command=self.round_reset)
        self.all_reset_bt = tk.Button(fr3, text="all reset", width=10, height=2, command=self.all_reset)
        self.add_player_bt = tk.Button(fr3, text=" player: +1 ", width=10, height=2, command=self.add_player)
        self.sub_player_bt = tk.Button(fr3, text=" player: -1 ", width=10, height=2, command=self.sub_player)

        self.all_reset_bt.grid(row=1, column=2)
        self.reset_bt.grid(row=1, column=0)
        self.start_bt.grid(row=1, column=1)
        self.add_player_bt.grid(row=0, column=1)
        self.sub_player_bt.grid(row=2, column=1)

        # キーバインド
        self.bind_all("<KeyPress-h>", lambda event: self.start_switch())
        self.focus_set()

    def add_player(self):
        self.player += 1
        self.player_lb["text"] = "{:0=02}人".format(self.player)

    def sub_player(self):
        self.player -= 1
        self.player_lb["text"] = "{:0=02}人".format(self.player)

    def start_switch(self):
        if not self.all_finish:
            if not self.all_start:
                self.all_start = True
                self.all_start_time = time.time()
            if not self.started:
                self.started = True
                self.start_bt["text"] = "Stop"
                self.start_time = time.time()
                self.master.after(100, self.count_up)
                self.after(100, self.update_countdown)
            else:
                self.started = False
                self.start_bt["text"] = "Start"
                self.round_time = self.now_rest_time
        else:
            self.all_finish = False
            self.all_reset()

    def round_reset(self):
        self.started = False  # カウンドダウン進行中フラグ
        self.start_time = 0
        self.round_time = self.round_str[4]
        self.now_rest_time = 0
        self.elapsed_time = 0
        self.countdown_lb["text"] = ct.Time_converter(self.round_str[4]).MS
        self.start_bt["text"] = "Start"

    def all_reset(self):
        self.round = 1
        self.round_str = self.list_str.output(self.round)
        self.next_round_str = self.list_str.output(self.round + 1)
        self.next_round_flag = False  # 次のラウンドへの移行フラグ
        self.all_finish = False
        self.started = False  # カウンドダウン進行中フラグ
        self.start_time = 0
        self.all_start = False  # カウントアップ進行中フラグ
        self.all_start_time = 0
        self.all_time = 0
        self.round_time = self.round_str[4]
        self.now_rest_time = 0
        self.elapsed_time = 0
        self.start_bt["text"] = "Start"
        self.countdown_lb["text"] = ct.Time_converter(self.round_str[4]).MS
        self.total_time_lb["text"] = "経過時間  [00:00:00]"
        self.BB_SB_lb["text"] = "{0} / {1}".format(self.round_str[2],
                                                   self.round_str[3])
        self.ante_lb["text"] = "({0})".format(self.round_str[1])
        self.next_BB_SB_lb["text"] = "next {0} / {1}".format(self.next_round_str[2], self.next_round_str[3])

    def update_countdown(self):
        self.elapsed_time = time.time() - self.start_time
        self.now_rest_time = self.round_time - self.elapsed_time
        if self.started:
            if self.now_rest_time > 0:
                self.countdown_lb["text"] = ct.Time_converter(int(self.now_rest_time)).MS
                self.master.after(200, self.update_countdown)
            else:
                self.next_round_flag = True
                self.started = False
                self.start_bt["text"] = "Start"
                self.next_round()

    def count_up(self):
        if self.all_start:
            self.all_time = time.time() - self.all_start_time
            self.total_time_lb["text"] = "経過時間  [" + ct.Time_converter(int(self.all_time)).HMS + "]"
            self.master.after(200, self.count_up)

    def next_round(self):
        if self.next_round_flag:
            self.round += 1
            if self.round == self.max_round:
                self.BB_SB_lb["text"] = "finish!"
                self.all_start = False
                self.next_round_flag = False
                self.all_finish = True
                self.start_bt["text"] = "All reset"

            elif self.round == (self.max_round - 1):
                self.round_str = self.list_str.output(self.round)
                self.round_time = self.round_str[4]
                self.next_BB_SB_lb["text"] = "final round"
                self.BB_SB_lb["text"] = "{0} / {1}".format(self.round_str[2],
                                                           self.round_str[3])
                self.ante_lb["text"] = "({0})".format(self.round_str[1])
                self.next_round_flag = False

            else:
                self.round_str = self.list_str.output(self.round)
                self.next_round_str = self.list_str.output(self.round + 1)
                self.round_time = self.round_str[4]

                if self.next_round_str[2] == "rest":
                    self.next_BB_SB_lb["text"] = "next 休憩"
                else:
                    self.next_BB_SB_lb["text"] = "next [{0} / {1}]:[{2}]".format(self.next_round_str[2],
                                                                                 self.next_round_str[3],
                                                                                 self.next_round_str[1])

                if self.round_str[2] == "rest":
                    self.BB_SB_lb["text"] = "休憩"
                else:
                    self.BB_SB_lb["text"] = "{0} / {1}".format(self.round_str[2],
                                                               self.round_str[3])
                    self.ante_lb["text"] = "({0})".format(self.round_str[1])

                self.countdown_lb["text"] = ct.Time_converter(int(self.round_time)).MS
                self.next_round_flag = False


def main():
    root = tk.Tk()
    win = mainFrame(master=root)
    win.master.title = "Structure Timer"
    win.master.geometry("1300x650+1+1")
    win.mainloop()


if __name__ == "__main__":
    main()
