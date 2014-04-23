Date: 2012-11-27
Title: Play Framework i18n Messages Hunter
Tags: Java, Play!, Shell
Category: Blog
Slug: play-framework-i18n-messages-hunter
Author: Eldelshell


Here's a little bash script to help you out hunting the different translatable labels your Play application has:

~~~bash
#!/bin/bash
 
tmp_file=$(mktemp)
 
repository_path="${1}"
file_path="${repository_path}/conf/messages."
docroot_path="${repository_path}/public"
langs=( "en" "es" )
 
echo "Searching for translatable strings"
find ${repository_path}/app/views -name '*.html' -exec grep -oE "@Messages\(\".+\"\)" {} \; | awk -F\" '{ print $2 }' >> ${tmp_file}
find ${repository_path} -name '*.java' -exec grep -oE "\(message=\".+\"\)" {} \; | awk -F\" '{ print $2 }' >> ${tmp_file}
find ${repository_path} -name '*.java' -exec grep -oE "Messages\.get\(\".+\"" {} \; | awk -F\" '{ print $2 }' >> ${tmp_file}
find ${docroot_path} -name '*.js' -exec grep -oE "i18n\.prop\(\".+\"" {} \; | awk -F\" '{ print $2 }' >> ${tmp_file}
find ${docroot_path} -name '*.js' -exec grep -oE "i18n\.prop\(\'.+\'" {} \; | awk -F\" '{ print $2 }' >> ${tmp_file}
 
# In tmp_file we should have all translatable string
# now we iterate over the file and the translation files
# and echo if the translation doesn't exists
 
output_tmp=$(mktemp)
flag_fail=0
 
echo "Matching found translatable strings with the different languages"
while read line; do
	for lang in ${langs[@]}; do
		grep -q ${line} ${file_path}${lang}
		if [ $? -eq 1 ]; then
			echo "Translation ${line} missing in ${lang}" >> ${output_tmp}
			flag_fail=1
		elif [ $? -eq 2 ]; then
			exit "Failed to read file ${file_path}${lang}"
		fi
	done
done < ${tmp_file}
 
echo "Sorting matches"
sort ${output_tmp} | uniq
 
 
for lang in ${langs[@]}; do
	echo "Looking for duplicated translations in file ${file_path}${lang}"
	awk -F\= '{ print $2 }' ${file_path}${lang} | sort | uniq -dc
done
 
rm "${tmp_file}"
rm "${output_tmp}"
 
exit ${flag_fail}
~~~

The script will search all Java, HTML and JavaScript files for the following candidates:

	@Messages("label.my.label")
	Messages.get("label.my.label")
	@Required(message="label.my.label")

AFAIK this are all possible combinations for a Play application. But wait, if you're 
using the _jquery-i18n-properties_ jQuery plugin the script will also detect all 
`i18n.prop("label.my.label')` entries in your JavaScript files.

The final result should be something like:

	Searching for translatable strings
	Matching found translatable strings with the different languages
	Sorting matches
	Translation label.are.you.sure missing in en
	Translation label.are.you.sure missing in es
	Translation label.my.label missing in en
	Translation label.my.label missing in es
	Looking for duplicated translations in file play/conf/messages.en
	Looking for duplicated translations in file play/conf/messages.es

Finally, the script will also output the number of duplicated translations.
