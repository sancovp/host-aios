# HOW TO READ — Read reads, Write and Edit change, Bash finds; a file the work needs is read, never peeked at

TRIGGER:[about to look inside a file · about to search for a file or a line · about to change a file · entering a folder
to work in it]

DO:[
- use Bash and the search tools to find which files matter and how a folder is laid out, and Read to read a file's
  contents — a folder's CLAUDE.md, rules and skills load only when Read, Write or Edit touches a file in it
- change a file with Write or Edit
- when you enter a folder to work in it, first learn its layout — what it holds, and the rules and skills its .claude
  carries — to the depth its size allows, since the layout shows how the logic there is meant to work; when what that
  folder states covers what you came to do, follow it
- peek at a file only while searching, when you do not yet know whether it matters
- when the work needs a file that is not already in context — the design you work under, the code you will change — read
  all of it with Read: in one call when it fits, else in consecutive chunks, each starting where the last ended
  (offset_next = offset_prev + limit_prev), through its end; the more complex the file, the smaller the chunks, and for
  the most complex, the mental model written in your reply as you go
- take a search hit as a location only: a hit in a file the work needs is read by the whole chain above, and a search
  re-jumps only to lines already read
]

NOT:[read a file the work needs through Bash (cat · head · tail · sed -n · a script's open()) · write a document or a code
file through Bash (a heredoc · sed -i · a redirect) · read the first lines of a file the work needs to decide whether to
read the rest · jump to a line a search found before the lines above it are read · conclude from a file read in part]
