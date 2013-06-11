####################################################################
#!/usr/bin/perl -w
#script from : http://pointelement.blogspot.com/2012/05/perl-script-for-brute-force-cracking.html


# This script was largely based on this Python script: http://www.rbgrn.net/content/25-how-to-write-brute-force-password-cracker

# Author: Tom

# Blog: kaabel.net/blog/

# IRC: irc.malvager.com #perlbar



use strict;

use GnuPG;



my $gpg = new GnuPG(); # Create GnuPG handle

my $found;

my @range = ('0' .. '9'); # Edit your charset here (Numbers, in this case) ('A'..'Z') for caps

my $maxlength = 5; # Max length of the password

my $minlength = 1;

my $time = time();



sub recurse($$) {

    my ($width, $position, $basestring) = @_; # Get the arguments supplied in the function's arguments.

    foreach my $char (@range) {

	if ($position < $width - 1) { # If the position needs to be shifted

	    &recurse ($width, $position+1, ("$basestring" . "$char")); # Guess why it's called recurse :p

	    next;

	}

# You must enter the file name of your encrypted file after ciphertext => and optionally a name for the output as well

	eval { $gpg->decrypt(ciphertext => 'example.txt.gpg', output => 'example_d.txt', passphrase => $basestring . $char, symmetric => 'true') }; # Eval is needed here, otherwise the program will end after an error.

	$found = $basestring . $char if !$@; # If there were no errors, make $found equal the password

	if (($time + 60) < time()) { # If 60 seconds have passed (1 minute),

	    print "Trying: " . $basestring . $char . "\n"; # print the current 'try'

	    $time = time(); # Reset the time

	}



	if ($found) { # If the password was found,

	    print "Found: $found\n";

	    exit;

	}

    }

}



foreach my $basewidth ($minlength .. $maxlength) { # Loop through the possible lengths of the password

    print "Checking paswords with length $basewidth\n";

    &recurse($basewidth, 0, ""); # Call the cracking sub

} 
