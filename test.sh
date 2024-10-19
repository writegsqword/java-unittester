export JAVA_HOME=/usr/lib/jvm/java-11-openjdk/bin
newname="${1}.java"
bash macro-sed.sh $1
java $newname