#!/usr/bin/perl

# Program to filter Wikipedia XML dumps to "clean" text consisting only of lowercase
# letters (a-z, converted from A-Z), and spaces (never consecutive).  
# All other characters are converted to spaces.  Only text which normally appears 
# in the web browser is displayed.  Tables are removed.  Image captions are 
# preserved.  Links are converted to normal text.  Digits are spelled out.

# Written by Matt Mahoney, June 10, 2006.  This program is released to the public domain.

$/=">";                     # input record separator
while (<>) {
  if (/<text /) {$text=1;}  # remove all but between <text> ... </text>
  if (/#redirect/i) {$text=0;}  # remove #REDIRECT
  if ($text) {

    # Remove any text not normally visible
    if (/<\/text>/) {$text=0;}
    s/<.*>//;               # remove xml tags
    s/&amp;/&/g;            # decode URL encoded chars
    s/&lt;/</g;
    s/&gt;/>/g;
    s/<ref[^<]*<\/ref>//g;  # remove references <ref...> ... </ref>
    s/<[^>]*>//g;           # remove xhtml tags
    s/\[http:[^] ]*/[/g;    # remove normal url, preserve visible text
    s/\|thumb//ig;          # remove images links, preserve caption
    s/\|left//ig;
    s/\|right//ig;
    s/\|\d+px//ig;
    s/\[\[image:[^\[\]]*\|//ig;
#    s/\[\[category:([^|\]]*)[^]]*\]\]/[[$1]]/ig;  # show categories without markup
    s/\[\[category:([^|\]]*)[^]]*\]\]/[[$1]]./ig;  # kill categories
    s/\[\[[a-z\-]*:[^\]]*\]\]//g;  # remove links to other languages
    s/\[\[[^\|\]]*\|/[[/g;  # remove wiki url, preserve visible text
    s/{{[^}]*}}//g;         # remove {{icons}} and {tables}
    s/{[^}]*}//g;
    s/\[//g;                # remove [ and ]
    s/\]//g;
    s/&[^;]*;/ /g;          # remove URL encoded chars
		s/^\| .+//mg;           # remove trailing infobox terms

    # convert to lowercase letters and spaces, spell digits
    $_=" $_ ";
    tr/A-Z/a-z/;

		# Version that spells out numbers.
    # s/0/ zero /g;
    # s/1/ one /g;
    # s/2/ two /g;
    # s/3/ three /g;
    # s/4/ four /g;
    # s/5/ five /g;
    # s/6/ six /g;
    # s/7/ seven /g;
    # s/8/ eight /g;
    # s/9/ nine /g;
		
		# Remove numbers entirely.
		s/[0-9]//;

		# Add periods, which are needed for prosaic.
		# s/=+([^=]+)=+/$1./g;
    # tr/a-z\./ /cs;
		# s/\.\.+/\./g;
		# s/ . /. /g;
		# s/^\. //;
    #chop;
		# if (!/\.$/) {
		# 		print $_ . '.';
		# } else  {
		# 		print $_;
		# }

		# No periods
    tr/a-z/ /cs;
		s/=+([^=]+)=+/$1/g;
		s/\s\s+//g;

		# $_ should only be printed once.
		if (/\w/) {
		  print $_ . "\n";
		}
  }
}
