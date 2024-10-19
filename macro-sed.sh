set -e
newname="$(echo $1 | sed 's/\./_processed./g')"
tmpname="${newname}.temp"
echo "Output: " $newname
cpp $1 $newname -C
sed -i '/#/d;s/__NL__/\n       /g;s/__TAB__/   /g' $newname
#remove meme gcc header

tail -n +42 $newname > $tmpname
mv $tmpname $newname
