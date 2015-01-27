#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
from initial import *


class Parser(object):
    
    def __init__(self):
        pass

    def checkPatern(self,patern):
        
        rest = patern.split()[::-1]
        command = rest.pop()

        if command in ['help', 'h']:
            return self.print_help(rest[::-1])
        elif command in ['set']:
            return self.set_option(rest[::-1])
        elif command in ['search', 's']:
            return self.search(rest[::-1])
        elif command in ['add','a']:
            return self.add_record()
        elif command in ['update', 'u']:
            return self.update_record(rest[::-1])
        elif command in ['type']:
            return self.print_type(rest[::-1])
        elif command in ['key']:
            return self.print_key(rest[::-1])
        elif command in ['news', 'n']:
            return self.news(rest[::-1])
        elif command.isdigit():
            return self.digit(int(command))

    def print_help(self, option):
        return "TO JEST HELP",' '.join(option)

    def set_option(self, option):
        
        if len(option) >= 2:
            if option[0] in options.options('lom'):
                options.set('lom', option[0], replace_colour(between(' '.join(option))[1]))
                with open('/home/alan/.lomrc', 'wb') as configfile:
                    options.write(configfile)
            else:
                return replace_colour('<red>\tThere is no option name \'' + option[0] + '\'<end>')
        elif len(option) == 1:
            regex = re.compile(option[0], re.IGNORECASE)
            for row  in options.items('lom'):
                if regex.search(row[0]):
                    print "{:10} =  {} ".format(row[0],re_replace_colour(row[1]))
        else:
            for row  in options.items('lom'):
                    print "{:10} =  {} ".format(row[0],re_replace_colour(row[1]))
        return ""

    def search(self, option):
        return "search", ' '.join(option)

    def add_record(self):
        window = MainWindow(check_all_paramiter_to_add)
        variables.types = databases.get('SELECT type FROM TYPES');
        window.add_type([ x[0] for x in variables.types])
        variables.keys = databases.get('SELECT key FROM KEYS');
        window.add_key([ x[0] for x in variables.keys])
        window.main_loop()
        return ""

    def update_record(self, option):
        return "set record", ' '.join(option)

    def print_type(self, option):
        
        if len(option) == 0:
            variables.types = databases.get('SELECT type FROM TYPES ORDER BY type;')
            for i,branch in enumerate(variables.types):
                print i+1,branch[0]
        elif option[0] == '-t':
            if len(option) == 1:
                return self.print_tree()
            else:
                return self.print_tree(option[1])
        elif option[0] == '-p':
            if len(option) == 1:
                return replace_colour('<red>Too few arguments<end>')
            else:
                if option[1].isdigit():
                    number = int(option[1])

                    if len(variables.types) >= number:
                        name_type = variables.types[(number - 1)][0]
                    else:
                        return replace_colour('\t<red>Please enter a number beetween <cyan><1,' + str(len(variables.types)) + '><end>\n')
                else:
                    name_type = option[1]

                variables.d_current = databases.get('select * from VIEW_LIBRARY where type=\'' + name_type + '\';')
            for i, row in enumerate(variables.d_current):
                print '\n\t---- ', i+1, '----\n'
                print self.print_data(row, options.get('lom', 's_print'))

        else:
            types = databases.get('SELECT type FROM TYPES ORDER BY type;')
            regex = re.compile(option[0], re.IGNORECASE)
            variables.types = []
            i = 0
            for branch in types:
                if regex.search(branch[0]):
                    variables.types.append(branch)
                    i += 1
                    print i,branch[0]

        return ""
    
    def print_key(self, option):
        
        print ""
        if len(option) == 0:
            variables.keys = databases.get('SELECT key, id_lib FROM KEYS;');
            for i, key in enumerate(variables.keys):
                print replace_colour('<green>{:<5}<end>{:15}<end>'.format(i+1, key[0]))
        elif option[0] == '-p':
            if len(option) == 1:
                return replace_colour('<red>Too few arguments<end>')
            else:
                if option[1].isdigit():
                    number = int(option[1])
                    if len(variables.keys) >= number:
                        name_type = variables.keys[(number - 1)][1]
                    else:
                        return replace_colour('\t<red>Please enter a number beetween <cyan><1,' + str(len(variables.keys)) + '><end>\n')
                        
                else:
                    for key in veriables.keys():
                        if key[0] == option[0]:
                            name_type = key[1]

                variables.d_current = []

                for key in name_type.split(','):
                    tmp = databases.get('SELECT * FROM VIEW_LIBRARY where id=' + str(key) + ';')[0]
                    variables.d_current.append(tmp)

                for i, row in enumerate(variables.d_current):
                    print '\n\t---- ', i+1, '----\n'
                    print self.print_data(row, options.get('lom', 's_print'))


        else:
            keys = databases.get('SELECT key, id_lib FROM KEYS');
            regex = re.compile(option[0], re.IGNORECASE)
            variables.keys = []
            i = 0
            for key in keys:
                if regex.search(key[0]):
                    variables.keys.append(key)
                    print replace_colour('<green>{:<5}<end>{:15}<red>{}<end>'.format(i+1, key[0], key[1]))
            
        return ""

    def digit(self, number):

        if len(variables.d_current) >= number:
            print '\n\t---- ', number, '----\n'
            print self.print_data(variables.d_current[number - 1])

        else:
            return replace_colour('\t<red>Too few argument\n\tPlease enter a number beetween <cyan><1,' + str(len(variables.d_current)) + '><end>\n')

        return ""


    def news(self, option):

        if len(option) == 0:
            variables.news_waiting = databases.get('select * from VIEW_WAITING w where w.data_a > \'' + variables.last_log + '\';')
            variables.news_added = databases.get('select * from VIEW_LIBRARY l where l.data_a > \'' + variables.last_log + '\';')

            print replace_colour('\n<green>\t\tWAITING TO ADDED<end>')
            for i, row in enumerate(variables.news_waiting):
                print '\n\t---- ', i+1, '----\n'
                print self.print_data(row, options.get('lom', 's_print'))

            print replace_colour('\n<green>\t\tRECORD ADDED TO LIBRARY<end>')
            for i, row in enumerate(variables.news_added):
                print '\n\t---- ', i+1, '----\n'
                print self.print_data(row, options.get('lom', 's_print'))

            variables.update_last_log()


        elif option[0] == '-a':
            variables.d_current = databases.get('select * from VIEW_WAITING;')
            print replace_colour('\n<green>\t\tALL RECORD WAITING TO ADDED<end>')
            for i, row in enumerate(variables.d_current):
                print '\n\t---- ', i+1, '----\n'
                print self.print_data(row, options.get('lom', 's_print'))

        return ""


    def print_tree(self, root='LOM'):
        variables.types = databases.get('SELECT type FROM TYPES;')

        if (root,) not in variables.types:
            return replace_colour("<red>\tThere is no type name'" + root + "'<end>")

        database_tree = databases.get('SELECT * FROM TYPE_TREE;')

        tree.add_node("LOM")
        for branch in database_tree:
            tree.add_node(branch[0], branch[1])

        tree.display(root)

        return ""

    def print_data(self, row, rule = None):
        
        if rule == None:
            rule = options.get('lom', 'l_print')

        rule = replace_colour(rule)

        rep = ['%I', '%N', '%T', '%D', '%K', '%A', '%d', '%M', '%m', '\\n']
        rep_to = ['{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '\n']

        rule = replace_list(rep, rep_to, rule)

        return (rule.format(row[0], row[1], row[2], '\n   ' + row[3], row[4], row[5], row[6], row[7], row[8])).replace('\\n', '\n   ')

        

def check_all_paramiter_to_add(window):
    
    record = window.get_data()
    all_name = databases.get('select name from WAITING;')[0]
    all_name += databases.get('select name from LIBRARY;')[0]

    for row in all_name:
        if record[0].lower() == row.lower():
            return window.print_error_message("Name alredy exist")

    b_add = True
    if record[2] != "":
        all_type = databases.get("select type from TYPES;")

        for row in all_type:
            if row[0].lower() == record[1].lower():
                b_add = False
                break

        if b_add == True:
            parent = databases.get("select id_type from TYPES where type='" + record[2] + "';")[0][0]
            databases.add("INSERT INTO TYPES(type, id_parent) VALUES ('" + record[1] + "',"+ str(parent) + ");")

    id_type = databases.get("select id_type from TYPES where type='" + record[1] + "';")[0][0]

    #delete ACCESS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    databases.add("INSERT INTO WAITING(name,id_type,id_access,description,key,name_a) VALUES ('" + record[0] + "', "+ str(id_type)+ ", 2, '" + record[3].replace("'",'"') + "', '" + record[4] + "', '" + getenv('USER') +"');")
    

    window.gtk_quit()
    window.destroy()
