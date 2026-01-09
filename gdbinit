#set print address off
#set print null-stop
set breakpoint pending on
set height 100
set history remove-duplicates unlimited
set history save
set history size 2048
set print asm-demangle
set print object
set print static-members off
set print thread-events off
set print vtbl
#set print array
#set print pretty
handle SIGPIPE nostop
handle SIGUSR1 nostop noprint
handle SIGUSR2 nostop noprint
source gdbinit

# because there are rc, rn, and rs:
define rf
  reverse-finish
end

define record0u
  p/u ($arg0)->record[0][0] @ ($arg0)->s->reclength
end
document record0u
Print/u a record[0] of a TABLE
end

define pp
  printf "----------\n%s\n----------\n", $arg0
end
document pp
Print a string verbatim (no C escapes, no truncation)
end

define r-or-c
  if $_thread == 0
    r
  else
    c
  end
end

define ber
  if $argc == 0
    b my_message_sql
  else
    b my_message_sql if error == $arg0
  end
  r-or-c
end
document ber
Breakpoint on Error and Run.
Put a breakpoint on my_message_sql, optionally only for a specific error code,
and run.
Use: ./mtr --gdb='ber 1160'
end

define bir
  b $arg0
  if $argc > 1
    ign 1 $arg1
  end
  r-or-c
end
document bir
Breakpint with Ignore and Run.
Put a breakpoint, optionally with an ignore count, and run.
Use: ./mtr --gdb='bir mysql_parse 15'
end

define bque
  b parse_sql if $_streq(parser_state->m_lip->m_ptr,$arg0)
  comm
    pp parser_state->m_lip->m_buf
  end
  r-or-c
end
document bque
Breakpoint on a Query (and Run).
Use: ./mtr --gdb='bque "select 1 from t1"'
end

define qq
  if $_thread == 0
    quit
  end
end
document qq
Safe quit. Quits only if the program isn't running.
Use: ./mtr --gdb='r;qq'
end

source ~/.gdb.py
