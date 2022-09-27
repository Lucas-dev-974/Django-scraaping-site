import sqlite3
from dotenv import load_dotenv
from os.path import exists
import os

# Here get the .env file config
load_dotenv()

# Création d'un singleton pour gerer la connexion à la base de données
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python3
class dtb(metaclass=Singleton):
    def __init__(self) -> None:
        db_path_location = os.getenv('SQLITE3_DATABASE_PATH')
        # Here check if SQlite3 database file path is specified
        if not db_path_location or db_path_location == '' or db_path_location == None:
            print('Erreur le chemin vers le fichier sqlite3 n\'est pas spécifié !\n')
            return False

        # Here we check if the file specified exist if not return false and print error 
        if not exists(db_path_location):
            print('Erreur: Le fichier ', db_path_location, ' n\'existe pas ! \n')
            return False
        
        self.con    = sqlite3.connect(db_path_location)
        self.cursor = self.con.cursor()
        self.query  = ''   # Will contain our query to be executed

        self.Types  = {
            'str'  : 'VARCHAR',
            'txt'  : 'TEXT',
            'int'  : 'INTEGER',
            'bool' : 'BOOLEAN',
            'float': 'FLOAT',
            'date' : 'DATETIME'
        }
        
        self.selections  = []
        self.foreignKeys = []

        self.SizeDefaultLen = '100'
        self.tables = self.getTables()
        pass

    # --- Private Functions --- 


    # Here we want to get the column fields and they field type, size, params....
    def __checkColumnFieldsType(self, col_name, value, arg, colunm_line_build):
        if arg == 'type':
            _value_and_size = self.__getTypeValueAndSize(value)
            type_ = _value_and_size[0]
            size  = _value_and_size[1]

            if(type_ == 'date'):
                 # self.Types refers to SQL type, for example str will be converted to VARVHAR
                colunm_line_build += ' ' + self.Types[type_] 
            else:
                colunm_line_build += ' ' + self.Types[type_] + '(' + size + ') '

        elif arg == 'nullable':
            if value == False:
                colunm_line_build += ' NOT NULL '
        
        elif arg == 'foreignKey':
            colunm_line_build += ' INT '
            self.foreignKeys.append({'cl_name': col_name, 'tbref': value['tbref'], 'tb_colref': value['tb_colref']})

        return colunm_line_build

    # BuildTable - Part build column    
    # Here we want to build query to create column when create table
    def __buildColunm(self, fields, colunm_line_build, have_next_col):
        # Lets check if json type Object is given for the fields
        # 
        col_name = colunm_line_build
        if isinstance(fields, (dict)) :
            # Boocle to get the arguments of column
            for arg, value in fields.items():
                # Here lets get the SQL column build in fonction of column args
                colunm_line_build = self.__checkColumnFieldsType(col_name, value, arg, colunm_line_build)
        
        elif isinstance(fields, (bool)):
            if colunm_line_build == 'id' and fields == True:
                colunm_line_build += ' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'
            elif colunm_line_build == 'nullable':
                if fields == True:
                    colunm_line_build += ' NOT NULL '

        if have_next_col:
            colunm_line_build += ','
        return colunm_line_build
    
    def __getTypeValueAndSize(self, value):
        _value = None
        size  = None

        if ':' in value:
            # get the type and size of column
            value_arg = value.split(':')

            # Print warning if more then 2arg splited by ':'
            if len(value_arg) > 2:
                print('Warning: Le typage d\'une colone ne peux contenir que 2 arguement, seul les 2 premier sont retenue')

            _value = value_arg[0]
            size   = value_arg[1]

            # Check if size given is int type
            try:
                size = int(size)
                size = str(size)
            except ValueError:
                size = self.SizeDefaultLen
                print('Warning: La taille par default du champ à été utiliser car la taille donnée n\'est pas de type int')                            
        else:
            size = self.SizeDefaultLen

        return _value or value, size

    def __parseExecutorResult(self, result):
        parsed_result = []
        for tb in result:
            parsed_result.append(tb[0])
        return parsed_result

    def __executorErrorManaged(self):
        try:
            return self.cursor.execute(self.query)
        except sqlite3.OperationalError as error:
            print('Error: ', error)

    def __parseWhere(self, whereClause):
        if not isinstance(whereClause, (dict)):
            print('Error: La clause where prend en parametre un Objet de type key-value comme {key: value}.\n')
            return False

        whereSQL = ' WHERE '
        blockage = len(whereClause) - 1
        iteration = 0

        for key, value in whereClause.items():
            whereSQL += key + "='" + value + "'"
            if(blockage != iteration):
                whereSQL += ' AND '
            iteration += 1
        return whereSQL


    # --- Public Functions ---
    def createTable(self, table_name, cols):
        
        self.query = 'CREATE TABLE IF NOT EXISTS '

        if not isinstance(table_name, (str)):
            print('Error: Une chaine de charactere dios être spécifier pour nomé la table')
            return False

        self.query += table_name +  '('
        if not isinstance(cols, (dict)):
            print('Error: Le parametre fields prend en parametre un Objet de type key-value comme {key: value}.\n')
            return False

        # ----------
        # Blockage to check if comma need to be set or not
        blockage  = len(cols) - 1
        iteration = 0

        # Boocle on column
        for col_name, fields in cols.items():
            have_next_col = False    # Here is boolean to define if comma need...
            if iteration < blockage: # Condition to determine if comma is needed or not
                have_next_col = True

            # Lets build the colunm in SQL 
            self.query += self.__buildColunm(fields, col_name, have_next_col)
            
            # Icrementation of iteration for blockage
            iteration += 1

        self.manageForeignKeys()
      
        self.query += ');'
        self.__executorErrorManaged()

    # Here we manage all foreignKey referenced
    def manageForeignKeys(self):
        
        blockage = len(self.foreignKeys) - 1
        iteration = 0
        if len(self.foreignKeys) > 0:
            self.query += ','
            for foreignKey in self.foreignKeys:
                self.query += ' FOREIGN KEY (' + foreignKey['cl_name'] + ') REFERENCES ' + foreignKey['tbref'] + ' (' + foreignKey['tb_colref'] + ')'  
                if iteration != blockage:
                    self.query += ', '
                iteration += 1


    # Todo retourner dans un array simple toute les table de la bdd
    def getTables(self):
        # self.select('name')._from('sqlite_master').where({'type': 'name'})
        self.query = 'SELECT name FROM sqlite_master WHERE type IN ("table","view") AND name NOT LIKE "sqlite_%" ORDER BY 1;'
        result = self.cursor.execute(self.query).fetchall()

        return self.__parseExecutorResult(result)

    # Todo Verifier si la table exist en bdd
    def existTable(self, table_name):
        print(table_name)
    
    def select(self, selections = ''):
        self.query   = ''
        StringSelect = "SELECT "

        if isinstance(selections, (list)):
            self.selections = selections
            
            endBoocle = len(selections) - 1
            iteration = 0

            while iteration != (endBoocle + 1):
                if(iteration == endBoocle):
                    StringSelect += selections[iteration] + ' '
                else:
                    StringSelect += selections[iteration] + ', '
                iteration += 1
        elif isinstance(selections, (str)):
            self.selections.append(selections)
            if selections == '':
                StringSelect += '*'
            else:
                StringSelect += selections

        self.query += StringSelect

        return self

    def insert(self, tb_name, values):
        self.query = ''
        if tb_name in self.tables:
            self.query = 'INSERT INTO ' + tb_name + ' '
            
            # blockage
            Blockage = len(values) - 1
            iteration = 0

            col_names = '('
            vals = '('

            for col_name, value in values.items():
                # print(col_name, ' ', value)
                col_names += col_name 
                vals      += "'" + str(value) + "'"
                if(Blockage != iteration):
                    col_names += ','
                    vals      += ','
                iteration += 1
                
            col_names += ')'
            vals += ')' 
            self.query += col_names + ' VALUES ' + vals + ';'

            result = self.__executorErrorManaged()
            self.con.commit()
            
            return result.lastrowid
        else: print('error la table n\'existe pas !')

    def _from(self, tb_name):
        self.query += ' FROM '
        if isinstance(tb_name, (str)):
            self.query += tb_name
        else:
            print('Error: Veuillez spécifié une chaine de charactère !\n')
            return False
    
        return self

    def where(self, whereClause):
        where = self.__parseWhere(whereClause)
        self.query += where + ';'
        return self

    def get(self):
        return self.__executorErrorManaged().fetchone()

    def all(self):
        results = self.__executorErrorManaged().fetchall()
        parsed_results = []

        for result in results:
            parsed_result = {}
            iteration = 0
            for field in self.selections:
                parsed_result[field] = result[iteration]
                iteration += 1
            parsed_results.append(parsed_result)
        return parsed_results

    def delete(self, tb_name, whereClause):
        self.query = 'DELETE FROM ' + tb_name + ' ' + self.__parseWhere(whereClause)
        self.__executorErrorManaged()
        self.con.commit()

    # getAllRelations({'tbname': 'user',})
    def OneToOne(self, table1, table2):
        if table1.table not in self.getTables():
            print("Error: la table ", table1.table, ' n\est pas enregistrer en bdd. Impossible ') 
        print(table1)


