DELETE FROM help_list;
delimiter //


INSERT INTO help_list(name, s_name, description) VALUES("ALL","","<tt>Usage:
  <span>s</span>   |  <span>search</span>  -- <span>show row  by pattern</span>
  <span>t</span>   |  <span>type</span>    -- <span>show types by pattern</span>
  <span>k</span>   |  <span>key</span>     -- <span>show keys  by pattern</span>
  <span>a</span>   |  <span>add</span>     -- <span>add row</span>
  <span>u</span>   |  <span>update</span>  -- <span>update row</span>
  <span>n</span>   |  <span>news</span>    -- <span>new row since the last use</span>
  <span>bye</span> |  <span>exit</span>    -- <span>exit WINDOW</span>
  <span>set</span> |  <span>set</span>     -- <span>show/set env</span>
  <span>h</span>   |  <span>help</span>    -- <span>this message</span>
  <span>his</span> |  <span>history</span> -- <span>show history</span>

  <span>More about command use help &lt;command&gt;</span></tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("set","","<tt>Usage:
  <span>set</span>                - show all variable
  <span>set variable value</span> - set variable

Example:
  <span>set history 2000</span>   - change length of stored history
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("search","s","<tt>Usage:
  <span>s[earch]</span>                      - show all row
  <span>s [-i,-n,-t,-d,-k,-a] [pattern]</span> - show row by pattern
Options:
  -i[d]            - regex pattern by id
  -n[ame]          - regex pattern by name
  -t[ype]          - regex pattern by type
  -d[esc[ription]] - regex pattern by description
  -k[ey]           - regex pattern by key
  -a[utor]         - regex pattern by autor

Double clik or select and press enter - show more info about row

Example:
  <span>s -i [1-10] -k python</span>   - between options is 'OR'
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("add","a","<tt>Usage:
  <span>a[dd]</span>              - add new row (open new window)
  <span>a[dd] -t [pattern]</span> - add new type (select root type)

  </tt>
Markup:
\<b><b>Bold</b>\<b>
\<i><i>Italic</i>\</i>
\<u><u>Underline</u>\</u>
\<small><small>Small</small>\</small>
\<big><big>Big</big>\</big>
\<tt><tt>Monospace font</tt>\</tt>
\<span color='red'><span color='red'>Red color</span>\</span>
\<a href='url'><a href='url'>URL</a>\</a>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("update","u", "<tt>Usage:
  <span>u[pdate] [pattern]</span>              - show row to update by pattern

Double clik or select and press enter - update selected row
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("type","t","<tt>Usage:
  <span>t[ype]</span>             - show all tree type
  <span>t[ype] [pattern]</span>      - show tree by pattern

Double clik or select and press enter - show all row by this type

Example:
  <span>t language</span>         - show tree language type
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("key","k","<tt>Usage:
  <span>k[ey]</span>             - show all keys
  <span>k[ey] [pattern]</span>      - show keys by pattern

Double clik or select and press enter - show all row by this key

Example:
  <span>k python</span>          - show python key
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("news","n","<tt>Usage:
  <span>n[ews]</span>             - show new rows that
                       have been added since your last login
  </tt>
");
//


delimiter ;
