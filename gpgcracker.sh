#!/bin/bash
#

output="/tmp/decrypted_file";

if [ -e ${output} ]
then
    echo "the output file ${output} all ready exists, deleting!!!!"
    rm ${output}
fi
# try all word in words.txt
for word in $(cat words.txt); do 

  # try to decrypt with word
#//  echo "${word}" | gpg --passphrase-fd 0 --no-tty --decrypt /home/arch-nicky/BB/Configfiles/thinkbank.gpg --output somegpgfile;
    echo "trying: ${word}"
    echo "${word}" | gpg --passphrase-fd 0 -q --batch --allow-multiple-messages --no-tty  --output ${output} -d /home/arch-nicky/BB/ConfigFiles/thinkbank.gpg;


  # if decrypt is successfull; stop
  if [ $? -eq 0 ]; then

    echo "GPG passphrase is: ${word}";
    exit 0;

  fi

if [ -e ${output} ]
then
    echo "$word was teh passphrase";
    exit 0;
fi

done;

exit 1;
