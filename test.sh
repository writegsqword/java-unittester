export JAVA_HOME=/usr/lib/jvm/java-11-openjdk/bin
newname="$(echo $1 | sed 's/\./_processed./g')"
bash macro-sed.sh $1
java $newname
mkdir -p out
mv $newname out
mv out/$newname out/$1