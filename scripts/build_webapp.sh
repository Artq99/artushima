#!/bin/sh

echo "================================================================================"
echo
echo " * * *   Building Script for the artushima-web   * * * "
echo
echo "================================================================================"
echo

echo "--------------------------------------------------------------------------------"
echo " Stage 1: building the Angular application."
echo "--------------------------------------------------------------------------------"
echo

cd ../webapp/artushima-web
ng build --prod=true --deploy-url=static/

echo "--------------------------------------------------------------------------------"
echo " Stage 2: cleaning up."
echo "--------------------------------------------------------------------------------"
echo

cd ../../
if [ -d "artushima/static" ]; then
    rm -R artushima/static
fi

if [ -d "artushima/templates" ]; then
    rm -R artushima/templates
fi

mkdir artushima/static
mkdir artushima/templates

echo "--------------------------------------------------------------------------------"
echo " Stage 3: copying files."
echo "--------------------------------------------------------------------------------"
echo

cp webapp/artushima-web/dist/artushima-web/* artushima/static/
mv artushima/static/index.html artushima/templates/index.html

echo "--------------------------------------------------------------------------------"
echo " artushima-web built."
echo "--------------------------------------------------------------------------------"
