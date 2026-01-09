import duel
from pretty_printer import PrettyPrinter

def print_string(val, length):
    if length <= 0:
        return '""'
    return str(val.dereference().cast(gdb.lookup_type('char').array(length - 1)))

def print_String(val):
    try:    cs=val['m_charset']          # 10.4+
    except: cs=val['str_charset']        # 10.3-
    try:    cs_name=cs['name']           # 10.5-
    except: cs_name=cs['cs_name']['str'] # 10.6+
    return '_' + cs_name.string() + ' ' + \
            print_string(val['Ptr'], val['str_length'])

@PrettyPrinter
def String(val):
    return print_String(val)

@PrettyPrinter('StringBuffer<>')
def StringBuffer(val):
    return print_String(val)

@PrettyPrinter
def Binary_string_pod(val):
    return print_string(val['Ptr'], val['str_length'])

@PrettyPrinter
def st_bitmap(val):
    s=''.join(reversed([format(int(val['bitmap'][i]),'064b')
                          for i in range(int(val['n_bits']+63)//64)]))
    return "b'" + s[-int(val['n_bits']):] + "'"

@PrettyPrinter('Bitmap<64u>')
def keymap64(val):
    return "b'" + format(long(val['map']),'b') + "'"


def print_flags(val, bits):
    return ','.join([s for n,s in enumerate(bits) if val & (1 << n)])

@PrettyPrinter
def sql_mode_t(val):
    return print_flags(val, ['REAL_AS_FLOAT', 'PIPES_AS_CONCAT', 'ANSI_QUOTES',
        'IGNORE_SPACE', 'IGNORE_BAD_TABLE_OPTIONS', 'ONLY_FULL_GROUP_BY',
        'NO_UNSIGNED_SUBTRACTION', 'NO_DIR_IN_CREATE', 'POSTGRESQL', 'ORACLE',
        'MSSQL', 'DB2', 'MAXDB', 'NO_KEY_OPTIONS', 'NO_TABLE_OPTIONS',
        'NO_FIELD_OPTIONS', 'MYSQL323', 'MYSQL40', 'ANSI',
        'NO_AUTO_VALUE_ON_ZERO', 'NO_BACKSLASH_ESCAPES', 'STRICT_TRANS_TABLES',
        'STRICT_ALL_TABLES', 'NO_ZERO_IN_DATE', 'NO_ZERO_DATE',
        'INVALID_DATES', 'ERROR_FOR_DIVISION_BY_ZERO', 'TRADITIONAL',
        'NO_AUTO_CREATE_USER', 'HIGH_NOT_PRECEDENCE', 'NO_ENGINE_SUBSTITUTION',
        'PAD_CHAR_TO_FULL_LENGTH', 'MODE_EMPTY_STRING_IS_NULL',
        'MODE_SIMULTANEOUS_ASSIGNMENT', 'MODE_TIME_ROUND_FRACTIONAL'])

@PrettyPrinter('Alter_inplace_info::HA_ALTER_FLAGS')
def HA_ALTER_FLAGS(val):
    return print_flags(val, ['ADD_INDEX', 'DROP_INDEX', 'ADD_UNIQUE_INDEX',
        'DROP_UNIQUE_INDEX', 'ADD_PK_INDEX', 'DROP_PK_INDEX',
        'ADD_VIRTUAL_COLUMN', 'ADD_STORED_BASE_COLUMN',
        'ADD_STORED_GENERATED_COLUMN', 'DROP_VIRTUAL_COLUMN',
        'DROP_STORED_COLUMN', 'ALTER_COLUMN_NAME', 'ALTER_VIRTUAL_COLUMN_TYPE',
        'ALTER_STORED_COLUMN_TYPE', 'ALTER_COLUMN_EQUAL_PACK_LENGTH',
        'ALTER_STORED_COLUMN_ORDER', 'ALTER_VIRTUAL_COLUMN_ORDER',
        'ALTER_COLUMN_NULLABLE', 'ALTER_COLUMN_NOT_NULLABLE',
        'ALTER_COLUMN_DEFAULT', 'ALTER_VIRTUAL_GCOL_EXPR',
        'ALTER_STORED_GCOL_EXPR', 'ADD_FOREIGN_KEY', 'DROP_FOREIGN_KEY',
        'CHANGE_CREATE_OPTION', 'ALTER_RENAME', 'ALTER_COLUMN_OPTION',
        'ALTER_COLUMN_COLUMN_FORMAT', 'ADD_PARTITION', 'DROP_PARTITION',
        'ALTER_PARTITION', 'COALESCE_PARTITION', 'REORGANIZE_PARTITION',
        'ALTER_TABLE_REORG', 'ALTER_REMOVE_PARTITIONING',
        'ALTER_ALL_PARTITION', 'RECREATE_TABLE', 'ALTER_COLUMN_VCOL',
        'ALTER_PARTITIONED', 'ALTER_ADD_CHECK_CONSTRAINT',
        'ALTER_DROP_CHECK_CONSTRAINT'])

@PrettyPrinter
def alter_table_operations(val):
    return print_flags(val, ['PARSER_ADD_COLUMN', 'PARSER_DROP_COLUMN',
        'CHANGE_COLUMN', 'ADD_INDEX', 'DROP_INDEX', 'RENAME', 'ORDER',
        'OPTIONS', 'CHANGE_COLUMN_DEFAULT', 'KEYS_ONOFF', 'RECREATE',
        'CONVERT_TO', 'RENAME_INDEX', '13', '14', '15', '16', '17', '18', '19',
        '20', 'ADD_FOREIGN_KEY', 'DROP_FOREIGN_KEY', 'CHANGE_INDEX_COMMENT',
        '24', 'COLUMN_ORDER', '26', 'ADD_CHECK_CONSTRAINT',
        'DROP_CHECK_CONSTRAINT', 'RENAME_COLUMN', 'COLUMN_UNVERSIONED',
        'ADD_SYSTEM_VERSIONING', 'DROP_SYSTEM_VERSIONING', 'ADD_PERIOD',
        'DROP_PERIOD', 'ADD_NON_UNIQUE_NON_PRIM_INDEX',
        'DROP_NON_UNIQUE_NON_PRIM_INDEX', 'ADD_UNIQUE_INDEX',
        'DROP_UNIQUE_INDEX', 'ADD_PK_INDEX', 'DROP_PK_INDEX',
        'ADD_VIRTUAL_COLUMN', 'ADD_STORED_BASE_COLUMN',
        'ADD_STORED_GENERATED_COLUMN', 'DROP_VIRTUAL_COLUMN',
        'DROP_STORED_COLUMN', 'COLUMN_NAME', 'VIRTUAL_COLUMN_TYPE',
        'STORED_COLUMN_TYPE', 'COLUMN_TYPE_CHANGE_BY_ENGINE',
        'STORED_COLUMN_ORDER', 'VIRTUAL_COLUMN_ORDER', 'COLUMN_NULLABLE',
        'COLUMN_NOT_NULLABLE', 'VIRTUAL_GCOL_EXPR', 'STORED_GCOL_EXPR',
        'COLUMN_OPTION', 'COLUMN_COLUMN_FORMAT', 'COLUMN_VCOL', 'PARTITIONED',
        'COLUMN_INDEX_LENGTH', 'INDEX_ORDER', 'INDEX_IGNORABILITY'])

def print_sockaddr(family,s):
    def u8(i): return int(s[i].cast(gdb.lookup_type('unsigned char')))
    def u16(i): return u8(i)*256+u8(i+1)
    if family == 0: return 'AF_UNSPEC'
    if family == 1: return 'AF_UNIX ???'
    if family == 2: # AF_INET
        return '{}.{}.{}.{}'.format(
                u8(2), u8(3), u8(4), u8(5)
                )
    if family == 10: # AF_INET6
        p = ':{:x}:{:x}:{:x}:{:x}:{:x}:{:x}:{:x}:{:x}:'.format(
                u16(2),u16(4),u16(6),u16(8),u16(10),u16(12),u16(14),u16(16)
                )
        for i in range(8,1,-1):
            if ':'+'0:'*i in p:
                return p.replace(':'+'0:'*i, ':'*(i+1), 1)[1:-1]
        return p[1:-1]
    return 'AF_???'

@PrettyPrinter
def sockaddr_storage(val):
    return print_sockaddr(val['ss_family'], val['__ss_padding'])

@PrettyPrinter
def sockaddr(val):
    return print_sockaddr(val['sa_family'], val['sa_data'])

@PrettyPrinter
def mysql_prlock_t(val):
    return '<mysql_prlock_t>'

@PrettyPrinter
def mysql_mutex_t(val):
    return '<mysql_mutex_t>'

@PrettyPrinter
def mysql_cond_t(val):
    return '<mysql_cond_t>'

@PrettyPrinter
def rw_lock_t(val):
    return '<rw_lock_t>'

@PrettyPrinter('std::mutex')
def std_mutex_t(val):
    return '<std::mutex_t>'

@PrettyPrinter
def pthread_mutex_t(val):
    return '<pthread_mutex_t>'

@PrettyPrinter
def pthread_cond_t(val):
    return '<pthread_cond_t>'

@PrettyPrinter
def pthread_rwlock_t(val):
    return '<pthread_rwlock_t>'

@PrettyPrinter('List<>')
def List_template(val):
    return "{} {}'s".format(val['elements'], val.type.template_argument(0).name)
