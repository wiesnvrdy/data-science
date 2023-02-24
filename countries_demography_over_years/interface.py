from math import floor
import tkinter as tk

def ui(countries:list, ages:list = []) -> dict:
    var_country = []
    var_age = []
    
    select_country = []
    select_age = []

    win_country = tk.Tk()
    win_country.title(" Countries Input ")
    win_country.config(padx = 50, pady = 20)

    tk.Label(win_country, text = " Select Countries to Analyze ",
             font = ("Arial", 15)).grid(column = 0,
                                        row = 0,
                                        columnspan = 5)
    
    tk.Label(win_country, text = " - " * 40,
             font = ("Arial", 13)).grid(column = 0,
                                        row = 1,
                                        columnspan = 5)

    def submitCountry():
        for ix_country in range(len(var_country)):
            if var_country[ix_country].get():
                select_country.append(countries[ix_country])
        win_country.destroy()

        if len(ages) > 1:
            win_age = tk.Tk()
            win_age.title(" Ages Input ")
            win_age.config(padx = 50, pady = 20)

            tk.Label(win_age, text = " Select Ages to Analyze ",
                     font = ("Arial", 13)).grid(column = 0,
                                                row = 0,
                                                columnspan = 3)
            
            tk.Label(win_age, text = " - " * 40,
                     font = ("Arial", 13)).grid(column = 0,
                                                row = 1,
                                                columnspan = 5)
            
            def submitAge():
                for ix_age in range(len(var_age)):
                    if var_age[ix_age].get():
                        select_age.append(ages[ix_age])
                win_age.destroy()

            for i_age in range(len(ages)):
                var_age.append(tk.IntVar(win_age))
                tk.Checkbutton(win_age, text = ages[i_age], font = ("Arial", 10),
                               variable = var_age[i_age],
                               onvalue = 1, offvalue = 0).grid(column = (i_age % 3),
                                                               row = (floor(i_age / 3)) + 2)
            
            tk.Button(win_age, text = "Submit", font = ("Arial", 11, "bold"),
                      command = submitAge).grid(column = 0,
                                                row = (floor(len(ages) / 5) + 3),
                                                columnspan = 5)
                
            win_age.mainloop()
        
        elif len(ages) == 1:
            
            for age in ages:
                select_age.append(age)

    for i_country in range(len(countries)):
        var_country.append(tk.IntVar(win_country))
        tk.Checkbutton(win_country, text = countries[i_country], font = ("Arial", 10),
                       variable = var_country[i_country],
                       onvalue = 1, offvalue = 0).grid(column = (i_country % 5),
                                                       row = (floor(i_country / 5)) + 2)

    tk.Button(win_country, text = "Submit", font = ("Arial", 11, "bold"),
              command = submitCountry).grid(column = 0,
                                            row = (floor(len(countries) / 5) + 3),
                                            columnspan = 5)

    win_country.mainloop()

    inp_dict = {
        'countries' : select_country,
        'ages' : select_age
    }

    return inp_dict